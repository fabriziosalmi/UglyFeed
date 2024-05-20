#!/bin/bash

# replace llm_processor.py with llm_processor_openai.py to use OpenAI models

# Script configuration (easily maintainable)
scripts=(
    "main.py"
    "llm_processor.py"
    "json2rss.py"
    "serve.py"
)
logfile="uglyfeed.log"

# Function to log messages with timestamps
log_message() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$logfile"
}

# Start execution
log_message "Script execution started"

for script in "${scripts[@]}"; do
    log_message "Running $script..."

    # Run script and redirect output/errors to log
    python "$script" > >(tee -a "$logfile") 2>&1
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log_message "$script completed successfully"
    else
        log_message "ERROR: $script failed with exit code $exit_code"
    fi
done

log_message "Script execution finished"
