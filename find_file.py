import boto3
import re

s3 = boto3.client('s3')

bucket_name = 'ubhack-interview'  

def find_latest_index_and_create_file(bucket_name, prefix='text_'):
    try:
        continuation_token = None
        latest_index = 0  
        
        file_names = []

        while True:
            if continuation_token:
                response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
            else:
                response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

          
            if 'Contents' in response:
                for obj in response['Contents']:
                    file_name = obj['Key']
                    file_names.append(file_name)
                    print(file_name)
                    # Use regex to find numeric index in file name (e.g., 'file_1')
                    match = re.search(r'(\d+)', file_name)
                    if match:
                        index = int(match.group(1))
                        if index > latest_index:
                            latest_index = index

            if response.get('IsTruncated'):  
                continuation_token = response.get('NextContinuationToken')
            else:
                break
        
        file_key = f"{prefix}{latest_index}"
        curr_response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        curr_file_content = curr_response['Body'].read().decode('utf-8')
        
        print(curr_file_content)

        next_index = latest_index + 1

        new_file_name = f"{prefix}{next_index}"

        s3.put_object(Bucket=bucket_name, Key=new_file_name)

        print(f"Created and uploaded new file: {new_file_name}")

        return curr_file_content

    except Exception as e:
        print(f"Error: {str(e)}")

find_latest_index_and_create_file(bucket_name)
