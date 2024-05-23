import requests
import streamlit as st

def main():
    st.title('Regulatory Relevance of Product Changes - RegHub x Roche - Alpha')

    # Creating four text boxes for user input
    input1 = st.text_area('Enter "Title (English)" in box 1', height=50)
    input2 = st.text_area('Enter "State before Planned Event (English)" in box 2', height=50)
    input3 = st.text_area('Enter "State after Planned Event (English)" in box 3', height=50)
    input4 = st.text_input('Enter "Molecule Type" in box 4')
    input5 = st.selectbox("Select which regulation to check (Canada will be added soon)", ["EU"])

    # Button to process the input
    if st.button('Run Classification'):
        # Combining all the strings
        combined_text = input1 + "\n" + input2 + "\n" + input3 + "\n" + input4

        # Only EU at the moment
        if input5 == "EU":
            ema_output = ema_classifier(combined_text)
            if len(ema_output) == 1:
                if ema_output[0] == '1':
                    st.write("The entered product change is relevant with respect to EMA Regulation")
                elif ema_output[0] == '0':
                    st.write("The entered product change is not relevant with respect to EMA Regulation")
            else:
                st.write(f"MODEL ERROR: {ema_output[0]} - {ema_output[1]}")

        # Count words and display if too many
        word_count = len(combined_text.split())
        if word_count > 350:
            st.write("Please note that the entered product change includes more than 350 words, which makes the results unstable.")

def ema_classifier(text):
    # Define the URL
    url = "https://reghub-ema-app-v5-4tvjzri7aq-uc.a.run.app/predict"

    # Define the payload (data)
    payload = {
        "text": text
        }

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Store the response text in a variable
        response_text = response.text
        return [response_text[-3]]
    else:
        return [response.status_code, response.reason]

if __name__ == "__main__":
    main()