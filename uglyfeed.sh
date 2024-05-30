#!/bin/bash

# Script configuration (easily maintainable)
scripts=(
    "main.py"
    "llm_processor.py"
    "json2rss.py"
    "serve.py"
)
logfile="uglyfeed.log"
port=8000 # Adjust to the port that serve.py uses

# Function to log messages with timestamps
log_message() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$logfile"
}

# Function to check if a port is in use
is_port_in_use() {
    lsof -i:$1 > /dev/null
    return $?
}

# Function to kill process using a specific port
kill_process_on_port() {
    fuser -k $1/tcp
}

# Create or truncate the log file at the start of execution
: > "$logfile"

# Start execution
log_message "Script execution started"

for script in "${scripts[@]}"; do
    log_message "Running $script..."

    if [ "$script" == "serve.py" ]; then
        # Check if the port is already in use
        if is_port_in_use $port; then
            log_message "Port $port is in use. Attempting to kill the existing process."
            kill_process_on_port $port
            sleep 2  # Wait a bit to ensure the process is terminated
        fi
        
        # Run serve.py in the background and capture its output
        python "$script" > >(tee -a "$logfile") 2>&1 &
        pid=$!
        log_message "$script started as background process with PID $pid"
        log_message "Waiting for $script to initialize..."
        sleep 5  # Adjust sleep time if needed to ensure serve.py has enough time to start
        if ps -p $pid > /dev/null; then
            log_message "$script is running"
        else
            log_message "ERROR: $script failed to start"
        fi
    else
        # Run other scripts and redirect output/errors to log
        python "$script" > >(tee -a "$logfile") 2>&1
        exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            log_message "$script completed successfully"
        else
            log_message "ERROR: $script failed with exit code $exit_code"
        fi
    fi
done

log_message "Script execution finished"
