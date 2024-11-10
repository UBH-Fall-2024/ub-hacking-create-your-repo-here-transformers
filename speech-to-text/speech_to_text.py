from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
import boto3

# Initialize boto3 S3 client
s3_client = boto3.client("s3")

# Bucket name
bucket_name = "ubhack-interview"

def get_latest_file_number():
    """Retrieve the highest numbered file in the S3 bucket."""
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="text_")
    if "Contents" not in response:
        return 0  # No files exist yet

    # Find the latest file based on the number suffix
    file_numbers = [
        int(obj["Key"].split("_")[-1]) for obj in response["Contents"]
        if obj["Key"].startswith("text_") and obj["Key"].split("_")[-1].isdigit()
    ]
    print(file_numbers)
    return max(file_numbers) if file_numbers else 0

def send_to_s3(text):
    """Append text to the latest file or create a new one on S3."""
    print("Uploading conversation: ",text)
    latest_number = get_latest_file_number()
    latest_file_key = f"text_{latest_number}"

    # Check if file exists to append content
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=latest_file_key)
        existing_text = response["Body"].read().decode("utf-8")
    except s3_client.exceptions.NoSuchKey:
        existing_text = ""

    # Combine existing text with new text and upload
    new_content = existing_text + '\n'+ text
    s3_client.put_object(Bucket=bucket_name, Key=latest_file_key, Body=new_content)
    print(f"Uploaded to {latest_file_key}.")

# Load the Vosk model (replace with your actual path)
model = Model("vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

# Initialize PyAudio
audio = pyaudio.PyAudio()
device_index = None

res = ""
# Find the index of the MacBook microphone device
for i in range(audio.get_device_count()):
    dev_info = audio.get_device_info_by_index(i)
    if "mic" in dev_info['name'].lower() or "microphone" in dev_info['name'].lower():
        device_index = i
        print(f"Using device {device_index}: {dev_info['name']}")
        break

if device_index is None:
    print("Microphone device not found.")
else:
    # Open the audio stream using the MacBook microphone device
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,  # Mono input for the microphone
        rate=16000,
        input=True,
        frames_per_buffer=4096,
        input_device_index=device_index
    )

    print("Listening to microphone audio... Press Ctrl+C to stop.")

    try:
        last_upload_time = time.time()
        # Continuous listening loop
        while True:
            try:
                data = stream.read(4096, exception_on_overflow=False)
            except IOError as e:
                print(f"Buffer overflow detected: {e}")
                continue  # Skip to the next loop iteration
            if recognizer.AcceptWaveform(data):  # Process if a phrase is recognized
                result = json.loads(recognizer.Result())
                print("Recognized Text:", result.get("text", ""))  # Display the recognized text
                res += result.get("text", "")
            else:
                # Print partial results for real-time feedback
                partial_result = json.loads(recognizer.PartialResult())
                # print("Partial Text:", partial_result.get("partial", ""))

            # Check if 30 seconds have passed to send to S3
            if time.time() - last_upload_time >= 30:
                send_to_s3(res)
                res = ""  # Reset `res` after sending
                last_upload_time = time.time()

    except KeyboardInterrupt:
        print("\nStopping audio capture...")
        if res:
            send_to_s3(res)  # Final send to ensure no text is lost

    finally:
        # Clean up on exit
        stream.stop_stream()
        stream.close()
        audio.terminate()
