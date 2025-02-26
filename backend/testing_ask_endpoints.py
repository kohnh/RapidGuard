import requests

# Ask a followup question
url_ask = "http://54.161.142.111:5000/ask"
payload = {
    "conversation": [
        {"role": "user", "content": "Where is the fire?"}, 
        {"role": "assistant", "content": "The fire has been detected on Level 1 (East Wing) of the shopping mall, near the escalator leading to Level 2, close to the 'Coffee Bean' cafe and 'Cosmetics Corner.'"}
    ]
}

response_ask_question = requests.post(url_ask, json=payload)

print("Response to Question:", "Sarah is sick today.\n")
print(response_ask_question.json().get('conversation')[-1].get('content'))