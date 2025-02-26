import os
import time
import base64
from openai import OpenAI
from dotenv import load_dotenv
from context_information import cctv_locations
import asyncio


# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

STATE_FILE = "last_triggered_count.txt"

def get_last_triggered_count():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    return None

def update_last_triggered_count(count):
    with open(STATE_FILE, "w") as f:
        f.write(str(count))

def reset_last_triggered_count():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)


def encode_image_file(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_and_convert_images():
    slist = []
    folder_path = "media/history"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            with open(file_path, "rb") as img_file:
                encoded_image = encode_image_file(img_file)
            CCTV_Num = "4"
            timestamp = time.ctime(os.stat(file_path).st_mtime)
            snapshot = [encoded_image, CCTV_Num, timestamp]
            slist.append(snapshot)
    return slist

def check_no_of_files_in_history():
    folder_path = "media/history/"
    imageList = [files for files in os.listdir(folder_path) if ".jpg" in files]
    return len(imageList)

############################################################
# --- Helper functions for snapshot to context pipeline ---
############################################################

def process_snapshot_sync(snapshot: list) -> str:
    """
    Process a single snapshot using the logic from the /image_context endpoint.
    Expects snapshot to be a list: [base64_image, cctv_number, timestamp].
    Uses the provided timestamp instead of the current datetime.
    """
    base64_image, cctv_number, timestamp = snapshot

    # Validate CCTV number
    if cctv_number not in cctv_locations:
        raise Exception(f"Invalid CCTV number: {cctv_number}")

    location_of_fire = cctv_locations[cctv_number]

    # Build the messages payload similar to /image_context but using the provided timestamp
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
                {
                    "type": "text",
                    "text": f"""
                            This is a snapshot of a shopping mall from the CCTV. A machine learning model has deemed that there is a fire present in the image. You are to verify if there is indeed a fire. 

                            If there is a fire detected in the image, describe and elaborate what is happening in the image strictly using the format below:

                            1) Size of fire
                            - There is a <small/medium/large> fire detected at {location_of_fire} on {timestamp}. It is about <insert size of fire> square metres in size.  
                            2) Nature of fire
                            - The fire is likely to be of <nature> (e.g. electrical, chemical, etc.) nature.
                            3) Location of the fire
                            - The fire is located at <location>.
                            4) General situation
                            - <Describe the general situation>.

                            If there is no fire or smoke detected, strictly only return "There is no fire or smoke detected."

                            Strictly adhere to the format above, do not include any headers, introduction or conclusion.
                            """
                }
            ]
        }
    ]

    # Call the OpenAI Chat Completions API
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    response_content = completion.choices[0].message.content
    return response_content

def summarize_contexts(contexts : list) -> str:
    """
    Summarize a list of image contexts (already in chronological order) into one summary.
    """
    combined_contexts = "\n".join(contexts)
    print("Combined contexts:", combined_contexts)
    print("\n")
    prompt = f"Based on the following chronological snapshots (based on timestamp, might not be in order) of a fire incident, summarise what has happened over time in a concise manner:\n{combined_contexts}"
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    summary = completion.choices[0].message.content


    print("Summary of the situation based on the provided snapshots:", summary)
    print("\n")
    return summary

async def process_snapshots(snapshots : list) -> None:
    """
    Asynchronously process all snapshots:
      - Process each image snapshot concurrently.
      - If more than one snapshot, summarise the chronological contexts.
      - Create fire_context.txt with the context of the first snapshot if there is only one snapshot.
      - Update fire_context.txt with the summarised context if there are more than one snapshot.
    """
    # Process each snapshot concurrently (using asyncio.to_thread to run the blocking API calls)
    tasks = [asyncio.to_thread(process_snapshot_sync, snapshot) for snapshot in snapshots]
    contexts = await asyncio.gather(*tasks)

    # If more than one image, summarise the overall situation; else use the single context.
    if len(contexts) > 1:
        summary = await asyncio.to_thread(summarize_contexts, contexts)
        summary += "\n"

        # Append to the fire_context.txt file with the summarised context
        with open("fire_context.txt", "a") as f:
            f.write(summary)

    else:
        summary = contexts[0] + "\n"

        # If there is only one snapshot, overwrite any existing fire_context.txt;
        with open("fire_context.txt", "w") as f:
            f.write(summary)


def snapshot_to_context_pipeline():
    """
    Main function to run the snapshot to context pipeline.
    Runs only once per triggering event (1 or 5 files).
    """
    current_count = check_no_of_files_in_history()
    
    # If current count is 1 or 5, check if we've already processed this state.
    if current_count in (1, 5):
        last_triggered = get_last_triggered_count()
        if last_triggered == current_count:
            print(f"Pipeline already run for count {current_count}.")
        else:
            snapshots = get_and_convert_images()
            asyncio.run(process_snapshots(snapshots))
            update_last_triggered_count(current_count)
    else:
        print(f"There are {current_count} files in the history folder, we will only process 1 or 5.")
        # Reset the state so that when the folder goes back to 1 or 5, the pipeline will run.
        reset_last_triggered_count()


if __name__ == "__main__":
    print("Running snapshot to context pipeline...")
    snapshot_to_context_pipeline()