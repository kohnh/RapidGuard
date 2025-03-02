#!/bin/bash

HISTORY_FOLDER=~/media/history
LAST_TIMESTAMP_FILE=~/nxhackathon/last_triggered_timestamp.txt

for ((i=1; i<=60; i++)); do
    # Find the latest modified file's timestamp in the history folder
    LATEST_TIMESTAMP=$(ls -lt --time-style=+%s "$HISTORY_FOLDER" | awk 'NR==2 {print $6}')

    # Read the last recorded timestamp (if exists), otherwise set to 0
    if [[ -f "$LAST_TIMESTAMP_FILE" ]]; then
        LAST_TIMESTAMP=$(cat "$LAST_TIMESTAMP_FILE")
    else
        LAST_TIMESTAMP=0
    fi

    # Run the script only if a newer file exists
    if [[ "$LATEST_TIMESTAMP" -gt "$LAST_TIMESTAMP" ]]; then
        echo "$LATEST_TIMESTAMP" > "$LAST_TIMESTAMP_FILE"  # Update the last timestamp
        python3 ~/nxhackathon/snapshot_to_context.py
    fi

    # Ensure only 5 latest files remain in media/history
    cd "$HISTORY_FOLDER" || exit 1
    ls -t | tail -n +6 | xargs rm -f 2>/dev/null

    sleep 1  # Wait for 1 second before the next iteration
done