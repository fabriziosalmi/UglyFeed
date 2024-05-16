#!/bin/bash

# Define directories
output_dir="output"
rewritten_dir="rewritten"

# Function to delete json files in a directory
delete_json_files() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo "Deleting JSON files in $dir..."
        # Find and delete json files, while being verbose about it
        find "$dir" -name '*.json' -print -exec rm {} \;
        echo "Deletion complete."
    else
        echo "Directory $dir does not exist, skipping..."
    fi
}

# Confirmation before deletion
read -p "Are you sure you want to delete all JSON files in $output_dir and $rewritten_dir? (y/n) " -n 1 -r
echo    # Move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    delete_json_files $output_dir
    delete_json_files $rewritten_dir
else
    echo "Operation cancelled."
fi
