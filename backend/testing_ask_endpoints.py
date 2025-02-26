import requests

# Understand the context of the image
# url_image_context = "http://127.0.0.1:5000/image_context"
url_image_context = "http://54.161.142.111:5000/image_context"
files = {"image": open("fire_tampines_mall.jpeg", "rb")}
data = {"cctv_number": "5"}
response_image_context = requests.post(url_image_context, files=files, data=data)
image_context_result = response_image_context.json().get("response")
print("Image Context:\n", image_context_result)
print("\n")

# Generate a solution based on the context
url_generate_solution = "http://54.161.142.111:5000/generate_solution"
payload = {"context": image_context_result}
response_generate_solution = requests.post(url_generate_solution, json=payload)

print("Generated Solution:\n", response_generate_solution.json().get("response"))

# Ask a question based on the context
url_ask = "http://54.161.142.111:5000/ask"
payload = {
    "conversation": [
        # {"role": "user", "content": "Where is the fire?"}, 
        # {"role": "assistant", "content": "I am an AI assistant here to help you."}
    ],
    "question": "Where is the fire?",
    "initial_solution" : response_generate_solution.json().get("response")
}

response_ask_question = requests.post(url_ask, json=payload)

print("Response to Question:", "Where is the fire?\n")
print(response_ask_question.json().get('conversation')[-1].get('content'))
print("\n")


# Ask a followup question
url_ask = "http://54.161.142.111:5000/ask"
payload = {
    "conversation": [
        {"role": "user", "content": "Where is the fire?"}, 
        {"role": "assistant", "content": "The fire has been detected on Level 1 (East Wing) of the shopping mall, near the escalator leading to Level 2, close to the 'Coffee Bean' cafe and 'Cosmetics Corner.'"}
    ],
    "question": "Sarah is sick today.",
    "initial_solution" : response_generate_solution.json().get("response")
}

response_ask_question = requests.post(url_ask, json=payload)

print("Response to Question:", "Sarah is sick today.\n")
print(response_ask_question.json().get('conversation')[-1].get('content'))