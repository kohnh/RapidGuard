from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
from question_or_context import is_question_or_context
from answer_question import answer_question
from user_query_to_context import get_context_from_user_query
from generate_solution import generate_solution

# For file watching
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_socketio import SocketIO

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS on all routes
app.config['SECRET_KEY'] = "mysecretkey"  # required for SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# List of filenames to monitor
files_to_watch = ["fire_context.txt", "user_context.txt"]

# Define a file system event handler that emits a SocketIO event on file creation or modification
class FileChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        # When a file is created, check if it's one we care about
        if any(event.src_path.endswith(filename) for filename in files_to_watch):
            filename = os.path.basename(event.src_path)
            print(f"File created: {filename}. Emitting event via SocketIO.")
            socketio.emit("file_changed", {"message": f"{filename} created"})

    def on_modified(self, event):
        # When a file is modified, check if it's one we care about
        if any(event.src_path.endswith(filename) for filename in files_to_watch):
            filename = os.path.basename(event.src_path)
            print(f"File modified: {filename}. Emitting event via SocketIO.")
            socketio.emit("file_changed", {"message": f"{filename} modified"})

# Set up and start the observer to watch the current directory (adjust path as needed)
observer = Observer()
observer.schedule(FileChangeHandler(), path=".", recursive=False)
observer.start()

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
        # print("Type of the last message in the chat thread:", is_question_or_context)
        
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
            new_solution = "I have updated the solution based on the latest fire situation and the context that you have provided. \n " + new_solution
            updated_conversation = conversation + [{"role": "assistant", "content": new_solution}]

            return jsonify({"conversation": updated_conversation})
        
        else:
            return jsonify({"error": "Could not determine the type of the last message in the conversation."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/context_update', methods=['POST'])
def context_update():
    """
    :return: An updated message thread containing the old message thread plus the new solution generated based on the updated fire situation and user context
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
        # generate new solution based on the latest fire situation and updated user context
        new_solution = generate_solution()
        new_solution = "I have updated the solution based on the latest fire situation and your context. \n" + new_solution
        updated_conversation = conversation + [{"role": "assistant", "content": new_solution}]
        print("New Solution Generated")
        return jsonify({"conversation": updated_conversation})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    # Run the app using SocketIO's run method to enable real-time communication.
    # socketio.run(app, debug=True)

    socketio.run(app, host="host_url", port=5000, debug=True)
