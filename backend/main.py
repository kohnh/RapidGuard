import eventlet
eventlet.monkey_patch()
import time

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
host_url = os.getenv("HOST_IP_ADDRESS")

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# List of filenames to monitor
files_to_watch = ["fire_context.txt", "user_context.txt"]

# Define a file system event handler that debounces events for the same file
class FileChangeHandler(FileSystemEventHandler):
    # Dictionary to store timer objects for each file
    timers = {}

    def schedule_emit(self, event):
        filename = os.path.basename(event.src_path)
        # If a timer already exists for this file, cancel it.
        if filename in self.timers:
            self.timers[filename].cancel()
        # Schedule a new timer to emit the event after 3 seconds of no further changes.
        self.timers[filename] = eventlet.spawn_after(3, self.emit_event, filename)

    def emit_event(self, filename):
        # Remove the timer entry as it's now firing.
        if filename in self.timers:
            del self.timers[filename]
        # Emit a generic event for the file that has changed.
        print(f"File changed: {filename}. Emitting event via SocketIO.")
        socketio.emit("file_changed", {"message": f"{filename} changed"})

    def on_created(self, event):
        # When a file is created, check if it's one we care about
        if any(event.src_path.endswith(f) for f in files_to_watch):
            self.schedule_emit(event)

    def on_modified(self, event):
        # When a file is modified, check if it's one we care about
        if any(event.src_path.endswith(f) for f in files_to_watch):
            self.schedule_emit(event)

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

    socketio.run(app, host=host_url, port=5000, debug=True)
