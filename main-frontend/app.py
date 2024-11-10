import streamlit as st
import time
import requests

base_url = "http://localhost:8000"

def stick_header():
    # Make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    background-color: #2D3748;
                    z-index: 999;
                }
                .fixed-header {
                    border-bottom: 2px solid white;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

container = st.container()

with container:
    st.markdown("# Interview AI")
    stick_header()

# Initialize chat history
if "interviewmsg" not in st.session_state:
    st.session_state.interviewmsg = []

# Display chat messages from history on app rerun
for message in st.session_state.interviewmsg:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Loop to generate continuous responses
while True:
    question = "Next query in sequence"  # Set up a base query or dynamically update

    with st.spinner("Generating response..."):
        try:
            response = requests.get(f"{base_url}/ask")
            response.raise_for_status()  # Raise an error if the request failed
            answer = response.text
            formatted_text = answer.replace("\\n", "\n")

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

    
    # Display assistant response in chat message container
    with st.chat_message("ai"):
        response = st.markdown(formatted_text)
    
    # Add assistant response to chat history
    st.session_state.interviewmsg.append({"role": "ai", "content": response})

    # Wait a few seconds before the next query
    time.sleep(100)
