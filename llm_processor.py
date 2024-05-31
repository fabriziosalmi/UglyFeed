import re
import json
import requests
import logging
import argparse
import yaml
import time
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure output and rewritten folders exist
output_folder = Path('output')
rewritten_folder = Path('rewritten')

output_folder.mkdir(parents=True, exist_ok=True)
rewritten_folder.mkdir(parents=True, exist_ok=True)

# Maximum context length for Groq API (this may need adjustment based on the actual limit)
MAX_TOKENS = 32768

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
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
    # Simple estimation: one token per 4 characters
    return len(text) / 4

def truncate_content(content, max_tokens):
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
        logging.error(f"OpenAI API request failed: {e}")
        return None

def call_groq_api(api_url, combined_content, model, api_key):
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    logging.debug(f"Groq API request data: {data}")
    try:
        response = requests_retry_session().post(api_url, data=data, headers=headers)
        response.raise_for_status()
        try:
            response_json = response.json()
            logging.debug(f"Groq API response: {response_json}")
            return response_json['choices'][0]['message']['content']
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response from Groq API: {e}")
            logging.error(f"Response content: {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Groq API request failed: {e}")
        if response is not None:
            logging.error(f"Groq API response content: {response.text}")
            if 'rate_limit_exceeded' in response.text:
                retry_after = parse_retry_after(response.json())
                logging.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                return call_groq_api(api_url, combined_content, model, api_key)
        return None

def parse_retry_after(response_json):
    try:
        message = response_json['error']['message']
        retry_after = float(re.search(r"try again in (\d+\.?\d*)s", message).group(1))
        return retry_after
    except (KeyError, AttributeError):
        return 60  # Default retry after 60 seconds if parsing fails

def call_ollama_api(api_url, combined_content, model):
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    logging.debug(f"Ollama API request data: {data}")
    try:
        response = requests_retry_session().post(api_url, data=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        try:
            response_json = response.json()
            logging.debug(f"Ollama API response: {response_json}")
            return response_json['message']['content']
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response from Ollama API: {e}")
            logging.error(f"Response content: {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Ollama API request failed: {e}")
        if response is not None:
            logging.error(f"Ollama API response content: {response.text}")
        return None

def ensure_proper_punctuation(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    corrected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        corrected_sentences.append(sentence)

    return ' '.join(corrected_sentences)

def process_json_file(filepath, api_url, model, api_key, content_prefix, rewritten_folder, api_type):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Error reading JSON from {filepath}: {e}")
        return

    combined_content = content_prefix + "\n".join(
        f"[source {idx + 1}] {item['content']}" for idx, item in enumerate(json_data))

    logging.info(f"Processing {filepath} - combined content prepared.")
    logging.debug(f"Combined content: {combined_content}")

    if estimate_token_count(combined_content) > MAX_TOKENS:
        logging.info(f"Truncating content to fit within {MAX_TOKENS} tokens.")
        combined_content = truncate_content(combined_content, MAX_TOKENS)

    if api_type == "openai":
        rewritten_content = call_openai_api(api_url, combined_content, model, api_key)
    elif api_type == "groq":
        rewritten_content = call_groq_api(api_url, combined_content, model, api_key)
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
            logging.info(f"Rewritten file saved to {new_filename}")
        except IOError as e:
            logging.error(f"Error writing to {new_filename}: {e}")
    else:
        logging.error("Failed to get rewritten content from LLM API.")
        logging.debug(f"Rewritten content: {rewritten_content}")

def validate_config(api_config):
    api_keys = ['openai_api_url', 'groq_api_url', 'ollama_api_url']
    active_apis = [key for key in api_keys if key in api_config]
    
    if len(active_apis) != 1:
        raise ValueError("Exactly one API configuration must be set in the config file.")
    
    if 'openai_api_url' in api_config:
        if 'openai_api_key' not in api_config or 'openai_model' not in api_config:
            raise ValueError("OpenAI API configuration is incomplete. Please set the API URL, API key, and model.")
    elif 'groq_api_url' in api_config:
        if 'groq_api_key' not in api_config or 'groq_model' not in api_config:
            raise ValueError("Groq API configuration is incomplete. Please set the API URL, API key, and model.")
    elif 'ollama_api_url' in api_config:
        if 'ollama_model' not in api_config:
            raise ValueError("Ollama API configuration is incomplete. Please set the API URL and model.")

def main(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        logging.error(f"Error reading config file {config_path}: {e}")
        return

    api_config = config.get('api_config', {})
    folder_config = config.get('folders', {})
    content_prefix = config.get('content_prefix', "")

    validate_config(api_config)

    if 'openai_api_url' in api_config:
        api_url = api_config['openai_api_url']
        model = api_config['openai_model']
        api_key = api_config['openai_api_key']
        api_type = 'openai'
    elif 'groq_api_url' in api_config:
        api_url = api_config['groq_api_url']
        model = api_config['groq_model']
        api_key = api_config['groq_api_key']
        api_type = 'groq'
    else:
        api_url = api_config['ollama_api_url']
        model = api_config['ollama_model']
        api_key = None  # Ollama does not need an API key
        api_type = 'ollama'

    output_folder = folder_config.get('output_folder', 'output')
    rewritten_folder = folder_config.get('rewritten_folder', 'rewritten')

    Path(rewritten_folder).mkdir(parents=True, exist_ok=True)

    json_files = Path(output_folder).glob('*.json')
    for json_file in json_files:
        process_json_file(json_file, api_url, model, api_key, content_prefix, rewritten_folder, api_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files with LLM API')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration YAML file (default: config.yaml in current directory)')
    args = parser.parse_args()

    config_path = args.config if args.config else 'config.yaml'
    main(config_path)
