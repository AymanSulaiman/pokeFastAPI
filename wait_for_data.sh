#!/bin/bash

# Path to the file that signals the data is ready
DATA_READY_SIGNAL="/app/data/pokemon_from_mage.parquet"

# Maximum amount of time to wait (in seconds) before giving up
MAX_WAIT_TIME=600 # 10 minutes

# Interval (in seconds) to check for the data ready signal
CHECK_INTERVAL=10

# Start the timer
start_time=$(date +%s)

# Wait loop
while : ; do
  # If the data ready signal exists...
  if [ -f "$DATA_READY_SIGNAL" ]; then
    echo "Data is ready. Starting FastAPI service..."
    # Start the FastAPI service
    uvicorn app.main:app --host "0.0.0.0" --port "8000"
    break
  else
    # Calculate how much time has elapsed
    current_time=$(date +%s)
    elapsed_time=$(( current_time - start_time ))

    # Check if the maximum wait time has been exceeded
    if [ $elapsed_time -ge $MAX_WAIT_TIME ]; then
      echo "Waited $MAX_WAIT_TIME seconds for the data to be ready, but it's not. Exiting."
      exit 1
    fi

    # Wait for the specified check interval before checking again
    echo "Data not ready yet. Waiting for $CHECK_INTERVAL seconds..."
    sleep $CHECK_INTERVAL
  fi
done
