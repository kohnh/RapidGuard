from flask import Flask, request, jsonify
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv
from context_information import cctv_locations, manpower_available, layout_of_mall, fire_alarm_stations, fire_management_SOP

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route('/ask', methods=['POST'])
def ask():
    # Expecting a JSON payload with 'conversation' (list of messages) and 'question' (string)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    conversation = data.get("conversation")
    question = data.get("question")
    initial_solution = data.get("initial_solution")
    
    if conversation is None or question is None:
        return jsonify({"error": "Please provide both 'conversation' and 'question' fields."}), 400

    # Ensure the conversation is a list
    if not isinstance(conversation, list):
        return jsonify({"error": "'conversation' must be a list of message objects."}), 400

    # Define a default system prompt
    default_system_prompt = f"""
        You are an AI assistant helping with dealing with a fire incident at a shopping mall.
        The user is a security officer seeking guidance on managing the situation and has been provided with a preliminary solution.
        The user might ask follow-up questions or seek clarification on the provided solution.
        Please provide detailed and informative responses to assist the user effectively.

        If the user asks a question or provides context that challenges the newest provided solution, please modify the solution accordingly and inform the user.
        This could be a new development in the situation, a change in the manpower available, blockage of certain exits, or any other relevant information.

        If the user asks for a new solution, generate a new solution based on the updated context and provide it to the user. Do not mention the previous solution in the new response, rather, provide the updated solution as if it is the first time.

        This is a dynamic conversation, and you should adapt your responses based on the user's queries and the context of the conversation.

        Here is the initial solution provided to the user: {initial_solution}
        The original manpower available is as follows: {manpower_available}
        The original layout of the mall is as follows: {layout_of_mall}
        The original fire alarm stations are as follows: {fire_alarm_stations}
        The fire management SOP is as follows: {fire_management_SOP}
    """

    # Prepend the system prompt if it's not already the first message
    if len(conversation) == 0 or conversation[0].get("role") != "system":
        conversation.insert(0, {"role": "system", "content": default_system_prompt})

    # Append the new question as a user message
    conversation.append({"role": "user", "content": question})
    
    try:
        # Call the OpenAI Chat Completions API with the full conversation
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation
        )
        # Get the assistant's response and append it to the conversation
        response_message = completion.choices[0].message.content
        conversation.append({"role": "assistant", "content": response_message})
        
        # Return the updated conversation thread
        return jsonify({"conversation": conversation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
