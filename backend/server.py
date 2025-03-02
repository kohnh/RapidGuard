import os
import time
import requests
import urllib3
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

# Ensure directories exist
os.makedirs("media/current", exist_ok=True)
os.makedirs("media/history", exist_ok=True)

# Image URL
IMAGE_URL = "https://10.0.2.15:7001/rest/v3/devices/e3e9a385-7fe0-3ba5-5482-a86cde7faf48/image?timestampMs=-1&rotation=10"

HEADERS = {
    "accept": "*/*",
    "x-runtime-guid": "vms-e98688d4e32d008117aeb0859c988bfa-Lc0djNhSu8"
}

# Remote server details
REMOTE_USER = "ubuntu"
REMOTE_IP = "54.159.85.234"
SSH_KEY = os.path.expanduser("~/nx/nxhackathon-keypair.pem")

def sync_to_server():
    """Syncs local folders with the remote server."""
    try:
        subprocess.run(
            f"rsync -avz -e 'ssh -i {SSH_KEY}' media/current/ {REMOTE_USER}@{REMOTE_IP}:~/media/current/",
            shell=True, check=True
        )
        subprocess.run(
            f"rsync -avz -e 'ssh -i {SSH_KEY}' media/history/ {REMOTE_USER}@{REMOTE_IP}:~/media/history/",
            shell=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during sync: {e}")

def manage_history_folder():
    """Keep only the 5 most recent images in the local 'history' folder."""
    history_folder = "media/history"
    images = sorted(
        [f for f in os.listdir(history_folder) if f.startswith("init_snapshot") or f.startswith("additional_snapshot_")],
        key=lambda x: os.path.getctime(os.path.join(history_folder, x))
    )
    while len(images) > 5:
        os.remove(os.path.join(history_folder, images.pop(0)))

@app.route('/upload', methods=['POST'])
def download_image():
    # If final lock exists, no further snapshots are allowed.
    if os.path.exists("final_snapshot.lock"):
        return jsonify({"message": "Snapshots completed. No more snapshots allowed."}), 200

    # If initial snapshot has not been taken, do it now.
    if not os.path.exists("initial_snapshot.lock"):
        try:
            response = requests.get(IMAGE_URL, headers=HEADERS, verify=False)
            if response.status_code == 200:
                # Save the initial snapshot
                current_path = os.path.join("media/current", "latest.jpg")
                with open(current_path, "wb") as f:
                    f.write(response.content)
                init_history_path = os.path.join("media/history", "init_snapshot.jpg")
                with open(init_history_path, "wb") as f:
                    f.write(response.content)
                manage_history_folder()
                sync_to_server()
                # Atomically create the initial snapshot lock file.
                try:
                    time.sleep(20)
                    fd = os.open("initial_snapshot.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.close(fd)
                except FileExistsError:
                    pass
                return jsonify({
                    "message": "Initial snapshot taken",
                    "current": current_path,
                    "history": init_history_path
                }), 200
            else:
                return jsonify({"error": "Failed to download image", "status_code": response.status_code}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Now that the initial snapshot exists, process additional snapshots.
    # Use an additional lock to ensure only one additional snapshot is processed at a time.
    try:
        fd = os.open("additional_snapshot.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        return jsonify({"message": "Another snapshot is in progress, skipping this request."}), 200

    try:
        # Ensure at least 10 seconds have passed since the initial snapshot.
        init_ctime = os.path.getctime("initial_snapshot.lock")
        if time.time() - init_ctime < 10:
            os.remove("additional_snapshot.lock")
            return jsonify({"message": "Waiting for 10 seconds after the initial snapshot."}), 200

        # Count the additional snapshots taken by checking files in the history folder.
        additional_files = [f for f in os.listdir("media/history") if f.startswith("additional_snapshot_")]
        if len(additional_files) >= 5:
            # Create final lock so that no more snapshots occur.
            if not os.path.exists("final_snapshot.lock"):
                try:
                    fd = os.open("final_snapshot.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.close(fd)
                except FileExistsError:
                    pass
            os.remove("additional_snapshot.lock")
            return jsonify({"message": "Maximum additional snapshots taken. No more snapshots."}), 200

        # Take an additional snapshot.
        response = requests.get(IMAGE_URL, headers=HEADERS, verify=False)
        if response.status_code == 200:
            current_path = os.path.join("media/current", "latest.jpg")
            with open(current_path, "wb") as f:
                f.write(response.content)
            snapshot_number = len(additional_files) + 1
            add_history_path = os.path.join("media/history", f"additional_snapshot_{snapshot_number}.jpg")
            with open(add_history_path, "wb") as f:
                f.write(response.content)
            manage_history_folder()
            sync_to_server()
            message = f"Additional snapshot {snapshot_number} taken."
        else:
            message = "Failed to download image"
        os.remove("additional_snapshot.lock")
        return jsonify({"message": message, "current": current_path}), 200
    except Exception as e:
        if os.path.exists("additional_snapshot.lock"):
            os.remove("additional_snapshot.lock")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
