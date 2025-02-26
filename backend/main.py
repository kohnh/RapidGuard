from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from question_or_context import is_question_or_context
from answer_question import answer_question
from user_query_to_context import get_context_from_user_query
from generate_solution import generate_solution


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route('/ask', methods=['POST'])
def ask() -> str:
    """
    :return: The new solution generated based on the updated fire situation and user context
    :rtype: str
    """

    # Expecting a JSON payload with 'conversation' (list of messages)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    conversation = data.get("conversation")

    # Ensure the conversation is a list
    if not isinstance(conversation, list):
        return jsonify({"error": "'conversation' must be a list of message objects."}), 400
    
    try:
        # Feed the whole chat into question_or_context to check if the last message in the conversation is a question or a context update
        type_of_user_response = is_question_or_context(conversation)
        print("Type of the last message in the chat thread:", is_question_or_context)
        
        # If the last message is a question, just answer it
        if type_of_user_response == "question":
            updated_conversation = answer_question(conversation)
            return jsonify({"conversation": updated_conversation})

        # If the last message is a context update, update the context and answer the user's question
        elif type_of_user_response == "context":
            # extract the additional context from the user's latest message
            get_context_from_user_query(conversation)

            # generate new solution based on the latest fire situation and updated user context
            new_solution = generate_solution()
            updated_conversation = conversation + [{"role": "assistant", "content": new_solution}]

            return jsonify({"conversation": updated_conversation})
        
        else:
            return jsonify({"error": "Could not determine the type of the last message in the conversation."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
