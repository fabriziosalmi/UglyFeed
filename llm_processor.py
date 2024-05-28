import re
import json
import requests
import logging
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def call_ollama_api(api_url, combined_content, model):
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
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

    if api_type == "openai":
        rewritten_content = call_openai_api(api_url, combined_content, model, api_key)
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
    if 'openai_api_url' in api_config and 'ollama_api_url' in api_config:
        raise ValueError("Both OpenAI and Ollama API configurations are set. Please configure only one.")
    if 'openai_api_url' not in api_config and 'ollama_api_url' not in api_config:
        raise ValueError("Neither OpenAI nor Ollama API configuration is set. Please configure one.")
    if 'openai_api_url' in api_config and ('openai_api_key' not in api_config or 'openai_model' not in api_config):
        raise ValueError("OpenAI API configuration is incomplete. Please set the API URL, API key, and model.")
    if 'ollama_api_url' in api_config and 'ollama_model' not in api_config:
        raise ValueError("Ollama API configuration is incomplete. Please set the API URL and model.")

def main():
    parser = argparse.ArgumentParser(description='Process JSON files and call LLM API.')
    parser.add_argument('--config', type=str, help='Path to the configuration file.', default='config.yaml')

    args = parser.parse_args()

    config_path = args.config if args.config else 'config.yaml'

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    api_config = config['api_config']
    folders = config['folders']
    content_prefix = config['content_prefix']

    validate_config(api_config)

    rewritten_folder = Path(folders['rewritten_folder'])
    rewritten_folder.mkdir(parents=True, exist_ok=True)

    output_folder = Path(folders['output_folder'])
    json_files = list(output_folder.glob('*.json'))
    if not json_files:
        logging.info("No JSON files found in the output folder.")
        return

    if 'openai_api_url' in api_config:
        api_url = api_config['openai_api_url']
        model = api_config['openai_model']
        api_key = api_config['openai_api_key']
        api_type = 'openai'
    else:
        api_url = api_config['ollama_api_url']
        model = api_config['ollama_model']
        api_key = None
        api_type = 'ollama'

    for filepath in json_files:
        logging.info(f"Processing file: {filepath}")
        process_json_file(filepath, api_url, model, api_key, content_prefix, rewritten_folder, api_type)

if __name__ == "__main__":
    main()
