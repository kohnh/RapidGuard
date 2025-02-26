import requests
import base64

# Utility function to encode an image file in base64
def encode_image_file(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Understand the context of the image
url_image_context = "http://127.0.0.1:5000/snapshot_to_solution"
# url_image_context = "http://54.161.142.111:5000/snapshot_to_solution"

###########################
## Initial image context ##
###########################

# Encode the image file in base64
with open("fire_over_time_test/initial.png", "rb") as image_file:
    base64_image = encode_image_file(image_file)

# Prepare the payload
snapshots = {
    "snapshots": [
        [base64_image, "1", "2024-02-25 12:00:00"]
    ]
}

# Send the POST request
response = requests.post(url_image_context, json=snapshots)

# Print the response
print("Testing situation with just 1 image:\n")
print(response.json().get("solution"))
print("\n")


############################
## Multiple image context ##
############################

# Encode the image files in base64
with open("fire_over_time_test/initial.png", "rb") as image_file:
    base64_image_1 = encode_image_file(image_file)

with open("fire_over_time_test/fleeing.png", "rb") as image_file:
    base64_image_2 = encode_image_file(image_file)

with open("fire_over_time_test/big_fire.png", "rb") as image_file:
    base64_image_3 = encode_image_file(image_file)

with open("fire_over_time_test/extinguished.png", "rb") as image_file:
    base64_image_4 = encode_image_file(image_file)

# Prepare the payload
snapshots = {
    "snapshots": [
        [base64_image_1, "5", "2024-02-25 12:00:00"],
        [base64_image_2, "5", "2024-02-25 12:02:00"],
        [base64_image_3, "5", "2024-02-25 12:04:00"],
        [base64_image_4, "5", "2024-02-25 12:06:00"]
    ]
}

# Send the POST request
response = requests.post(url_image_context, json=snapshots)

# Print the response
print("Testing situation with multiple images:\n")
print(response.json().get("solution"))
print("\n")