"""
This script processes JSON files using various LLM APIs and saves the rewritten content.
"""

import re
import json
import logging
import argparse
import yaml
import os
import time
from pathlib import Path
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from openai import OpenAI

# Configure logging using the new method
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Maximum context length for LLM APIs
MAX_TOKENS = 32768

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """Create a requests session with retry logic."""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def estimate_token_count(text):
    """Estimate the number of tokens in a text."""
    return len(text) / 4

def truncate_content(content, max_tokens):
    """Truncate the content to fit within the maximum token limit."""
    tokens = content.split()
    truncated_content = []
    current_tokens = 0

    for token in tokens:
        current_tokens += len(token) / 4
        if current_tokens > max_tokens:
            break
        truncated_content.append(token)

    return ' '.join(truncated_content)

def call_openai_api(api_url, combined_content, model, api_key):
    """Call the OpenAI API with the given parameters."""
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
                {"role": "user", "content": combined_content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("OpenAI API request failed: %s", e)
        return None

def call_groq_api(api_url, combined_content, model, api_key):
    """Call the Groq API with the given parameters."""
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    logger.debug("Groq API request data: %s", data)
    try:
        response = requests_retry_session().post(api_url, data=data, headers=headers)
        response.raise_for_status()
        try:
            response_json = response.json()
            logger.debug("Groq API response: %s", response_json)
            return response_json['choices'][0]['message']['content']
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON response from Groq API: %s", e)
            logger.error("Response content: %s", response.text)
            return None
    except requests.RequestException as e:
        logger.error("Groq API request failed: %s", e)
        if response is not None:
            logger.error("Groq API response content: %s", response.text)
            if 'rate_limit_exceeded' in response.text:
                retry_after = parse_retry_after(response.json())
                logger.info("Rate limit exceeded. Retrying after %s seconds.", retry_after)
                time.sleep(retry_after)
                return call_groq_api(api_url, combined_content, model, api_key)
        return None

def call_ollama_api(api_url, combined_content, model):
    """Call the Ollama API with the given parameters."""
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    logger.debug("Ollama API request data: %s", data)
    try:
        response = requests_retry_session().post(api_url, data=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        try:
            response_json = response.json()
            logger.debug("Ollama API response: %s", response_json)
            return response_json['message']['content']
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON response from Ollama API: %s", e)
            logger.error("Response content: %s", response.text)
            return None
    except requests.RequestException as e:
        logger.error("Ollama API request failed: %s", e)
        if response is not None:
            logger.error("Ollama API response content: %s", response.text)
        return None

def call_anthropic_api(api_url, combined_content, model, api_key):
    """Call the Anthropic API with the given parameters."""
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "user", "content": combined_content}
        ],
        "max_tokens": 4096
    })
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    logger.debug("Anthropic API request data: %s", data)
    try:
        response = requests_retry_session().post(api_url, data=data, headers=headers)
        response.raise_for_status()
        try:
            response_json = response.json()
            logger.debug("Anthropic API response: %s", response_json)

            # Print the full response for debugging purposes
            print("Anthropic API response:", response_json)

            # Extract the content from the response
            if 'content' in response_json and isinstance(response_json['content'], list):
                # Assuming the desired text is in the first object of the content array
                content_items = response_json['content']
                text_content = " ".join(item['text'] for item in content_items if 'text' in item)
                return text_content
            else:
                logger.error("Expected 'content' key with list structure not found in response: %s", response_json)
                return None
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON response from Anthropic API: %s", e)
            logger.error("Response content: %s", response.text)
            return None
    except requests.RequestException as e:
        logger.error("Anthropic API request failed: %s", e)
        if response is not None:
            logger.error("Anthropic API response content: %s", response.text)
        return None

def parse_retry_after(response_json):
    """Parse the retry-after duration from the response."""
    try:
        message = response_json['error']['message']
        retry_after = float(re.search(r"try again in (\d+\.?\d*)s", message).group(1))
        return retry_after
    except (KeyError, AttributeError):
        return 60  # Default retry after 60 seconds if parsing fails

def ensure_proper_punctuation(text):
    """Ensure proper punctuation in the text."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    corrected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        corrected_sentences.append(sentence)

    return ' '.join(corrected_sentences)

def read_content_prefix(prefix_file_path):
    """Read content prefix from a file."""
    try:
        with open(prefix_file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (IOError, FileNotFoundError) as e:
        logger.error("Error reading content prefix file %s: %s", prefix_file_path, e)
        return ""

def process_json_file(filepath, api_url, model, api_key, content_prefix, rewritten_folder, api_type):
    """Process a JSON file using the specified API."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            logger.debug("Type of json_data: %s", type(json_data))
            if isinstance(json_data, dict):
                # If json_data is a dictionary, convert it to a list of one dictionary
                json_data = [json_data]
                logger.warning("Converted dictionary to list. File: %s", filepath)
            elif isinstance(json_data, str):
                logger.error("Expected list of dictionaries but got a string. File: %s", filepath)
                return
    except (json.JSONDecodeError, IOError) as e:
        logger.error("Error reading JSON from %s: %s", filepath, e)
        return

    # Ensure 'content' key exists in each dictionary
    combined_content = content_prefix + "\n".join(
        f"[source {idx + 1}] {item.get('content', 'No content provided')}" for idx, item in enumerate(json_data))

    logger.info("Processing %s - combined content prepared.", filepath)
    logger.debug("Combined content: %s", combined_content)

    if estimate_token_count(combined_content) > MAX_TOKENS:
        logger.info("Truncating content to fit within %s tokens.", MAX_TOKENS)
        combined_content = truncate_content(combined_content, MAX_TOKENS)

    if api_type == "openai":
        rewritten_content = call_openai_api(api_url, combined_content, model, api_key)
    elif api_type == "groq":
        rewritten_content = call_groq_api(api_url, combined_content, model, api_key)
    elif api_type == "anthropic":
        rewritten_content = call_anthropic_api(api_url, combined_content, model, api_key)
    else:
        rewritten_content = call_ollama_api(api_url, combined_content, model)

    if rewritten_content:
        cleaned_content = re.sub(r'\*\*', '', rewritten_content)
        cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
        cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)

        cleaned_content = ensure_proper_punctuation(cleaned_content)

        links = [item.get('link') for item in json_data if 'link' in item]

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_data = {
            'title': json_data[0].get('title', 'No Title'),
            'content': cleaned_content,
            'processed_at': current_datetime,
            'links': links,
            'api': api_type,
            'model': model
        }

        new_filename = Path(rewritten_folder) / (Path(filepath).stem + '_rewritten.json')
        try:
            with open(new_filename, 'w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, ensure_ascii=False, indent=4)
            print(f"Rewritten file saved to {new_filename}")
            logger.info("Rewritten file saved to %s", new_filename)
        except IOError as e:
            logger.error("Error writing to %s: %s", new_filename, e)
    else:
        logger.error("Failed to get rewritten content from LLM API.")
        logger.debug("Rewritten content: %s", rewritten_content)

def validate_config(api_config):
    """Validate the configuration for the selected API."""
    selected_api = api_config.get('selected_api')

    if selected_api == "OpenAI":
        required_keys = ['openai_api_url', 'openai_api_key', 'openai_model']
    elif selected_api == "Groq":
        required_keys = ['groq_api_url', 'groq_api_key', 'groq_model']
    elif selected_api == "Ollama":
        required_keys = ['ollama_api_url', 'ollama_model']
    elif selected_api == "Anthropic":
        required_keys = ['anthropic_api_url', 'anthropic_api_key', 'anthropic_model']
    else:
        raise ValueError("Invalid API selection. Please choose OpenAI, Groq, Ollama, or Anthropic.")

    missing_keys = [key for key in required_keys if not api_config.get(key)]
    if missing_keys:
        raise ValueError(f"The selected API configuration is incomplete. Missing keys: {', '.join(missing_keys)}")

def main(config_path, prompt_path=None, api=None, api_key=None, model=None, api_url=None, output_folder=None, rewritten_folder=None):
    """Main function to process JSON files with LLM API."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        logger.error("Error reading config file %s: %s", config_path, e)
        return

    api_config = config.get('api_config', {})
    folder_config = config.get('folders', {})
    prompt_file_path = prompt_path or config.get('prompt_file', "")

    # Override with environment variables if present
    selected_api = api or os.getenv('API_TYPE', api_config.get('selected_api'))
    model = model or os.getenv('API_MODEL', api_config.get(f'{selected_api.lower()}_model'))
    api_key = api_key or os.getenv('API_KEY', api_config.get(f'{selected_api.lower()}_api_key'))
    api_url = api_url or os.getenv('API_URL', api_config.get(f'{selected_api.lower()}_api_url'))
    output_folder = output_folder or os.getenv('OUTPUT_FOLDER', folder_config.get('output_folder', 'output'))
    rewritten_folder = rewritten_folder or os.getenv('REWRITTEN_FOLDER', folder_config.get('rewritten_folder', 'rewritten'))
    prompt_file_path = prompt_path or os.getenv('PROMPT_FILE', prompt_file_path)
    content_prefix = read_content_prefix(prompt_file_path) if prompt_file_path else config.get('content_prefix', "")

    validate_config({
        'selected_api': selected_api,
        f'{selected_api.lower()}_model': model,
        f'{selected_api.lower()}_api_key': api_key,
        f'{selected_api.lower()}_api_url': api_url
    })

    Path(rewritten_folder).mkdir(parents=True, exist_ok=True)

    json_files = Path(output_folder).glob('*.json')
    for json_file in json_files:
        process_json_file(json_file, api_url, model, api_key, content_prefix, rewritten_folder, selected_api.lower())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files with LLM API')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration YAML file (default: config.yaml in current directory)')
    parser.add_argument('--prompt', type=str, help='Path to the prompt file')
    parser.add_argument('--api', type=str, help='API type (OpenAI, Groq, Ollama, Anthropic)')
    parser.add_argument('--api_key', type=str, help='API key for the selected API')
    parser.add_argument('--model', type=str, help='Model to use for the selected API')
    parser.add_argument('--api_url', type=str, help='API URL for the selected API')
    parser.add_argument('--output_folder', type=str, help='Output folder containing JSON files to process')
    parser.add_argument('--rewritten_folder', type=str, help='Folder to save the rewritten JSON files')

    args = parser.parse_args()

    config_path = args.config if args.config else 'config.yaml'
    main(config_path, args.prompt, args.api, args.api_key, args.model, args.api_url, args.output_folder, args.rewritten_folder)
