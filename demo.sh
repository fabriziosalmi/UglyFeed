#!/bin/bash

# Function to prompt for user input
prompt() {
  read -p "$1: " REPLY
  echo "$REPLY"
}

# Function to prompt for API selection
select_api() {
  echo "Select model API:"
  echo "1) Ollama"
  echo "2) OpenAI"
  read -p "Enter the number corresponding to your choice: " api_choice
  case $api_choice in
    1)
      api="Ollama"
      ;;
    2)
      api="OpenAI"
      ;;
    *)
      echo "Invalid selection. Please enter 1 or 2."
      select_api
      ;;
  esac
}

# Function to prompt for LLM_MODEL selection
select_llm_model() {
  if [[ "$api" == "Ollama" ]]; then
    echo "Select LLM_MODEL:"
    echo "1) phi3"
    echo "2) llama3"
    read -p "Enter the number corresponding to your choice: " model_choice
    case $model_choice in
      1)
        llm_model="phi3"
        ;;
      2)
        llm_model="llama3"
        ;;
      *)
        echo "Invalid selection. Please enter 1 or 2."
        select_llm_model
        ;;
    esac
  elif [[ "$api" == "OpenAI" ]]; then
    echo "Select LLM_MODEL:"
    echo "1) gpt-3.5-turbo"
    echo "2) gpt4"
    echo "3) gpt4o"
    read -p "Enter the number corresponding to your choice: " model_choice
    case $model_choice in
      1)
        llm_model="gpt-3.5-turbo"
        ;;
      2)
        llm_model="gpt4"
        ;;
      3)
        llm_model="gpt4o"
        ;;
      *)
        echo "Invalid selection. Please enter 1, 2, or 3."
        select_llm_model
        ;;
    esac
  fi
}

# Step 1: Specify one or more RSS feeds
echo "Please enter up to 100 RSS feeds, either separated by spaces or one per line. Enter an empty line to finish:"
rss_feeds=()
while IFS= read -r line; do
  [[ -z "$line" ]] && break
  rss_feeds+=("$line")
done

# Check if rss_feeds is empty, if so prompt for space-separated input
if [ ${#rss_feeds[@]} -eq 0 ]; then
  echo "No RSS feeds entered. Please enter space-separated RSS feeds:"
  read -a rss_feeds
fi

# Save RSS feeds to input/feeds.txt
mkdir -p input
feeds_file="input/feeds.txt"
> "$feeds_file"  # Clear the file if it already exists
for feed in "${rss_feeds[@]}"; do
  echo "$feed" >> "$feeds_file"
done

# Step 2: Specify model API
select_api

if [[ "$api" == "OpenAI" ]]; then
  api_key=$(prompt "Specify API_KEY for OpenAI API")
elif [[ "$api" == "Ollama" ]]; then
  ollama_url=$(prompt "Specify OLLAMA_URL for Ollama API (default: http://localhost:11434/api/chat): ")
  ollama_url=${ollama_url:-http://localhost:11434/api/chat}
fi

# Step 3: Specify LLM_MODEL
select_llm_model

# Inform the user that the process is starting
echo "Starting the process with API: $api and Model: $llm_model..."

# Step 4: Execute main.py script
python3 main.py

# Step 5a: Execute llm_processor.py or llm_processor_openai.py based on selected API and model
if [[ "$api" == "Ollama" ]]; then
  if [[ "$llm_model" == "phi3" ]]; then
    python3 llm_processor.py --model phi3 --api_url "$ollama_url"
  elif [[ "$llm_model" == "llama3" ]]; then
    python3 llm_processor.py --model llama3 --api_url "$ollama_url"
  else
    echo "Invalid LLM_MODEL for Ollama API"
    exit 1
  fi
elif [[ "$api" == "OpenAI" ]]; then
  if [[ "$llm_model" == "gpt-3.5-turbo" ]]; then
    python3 llm_processor_openai.py --model gpt-3.5-turbo --api_key "$api_key"
  elif [[ "$llm_model" == "gpt4" ]]; then
    python3 llm_processor_openai.py --model gpt4 --api_key "$api_key"
  elif [[ "$llm_model" == "gpt4o" ]]; then
    python3 llm_processor_openai.py --model gpt4o --api_key "$api_key"
  else
    echo "Invalid LLM_MODEL for OpenAI API"
    exit 1
  fi
else
  echo "Invalid API selection"
  exit 1
fi

# Step 6: Execute json2rss.py
python3 json2rss.py

# Step 7: Execute serve.py
python3 serve.py
