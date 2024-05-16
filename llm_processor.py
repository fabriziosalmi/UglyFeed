import json
import requests
import os
import logging
from pathlib import Path
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Constants
API_URL = "http://192.168.100.41:11434/api/chat" 
OUTPUT_FOLDER = Path('output')
REWRITTEN_FOLDER = Path('rewritten')
RETRIES = 3
BACKOFF_FACTOR = 0.3
HEADERS = {'Content-Type': 'application/json'}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def requests_retry_session(retries=RETRIES, backoff_factor=BACKOFF_FACTOR, status_forcelist=(500, 502, 504), session=None):
    """ Returns a session with retry logic configured """
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

def call_llm_api(combined_content):
    """ Sends combined content to the LLM API and receives a rewritten version. """
    data = json.dumps({
        "model": "llama3",
        "messages": [{"role": "user", "content": combined_content}],
        "stream": False
    })
    try:
        response = requests_retry_session().post(API_URL, data=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

def process_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error reading JSON from {filepath}: {e}")
        return
    except IOError as e:
        logging.error(f"Error opening file {filepath}: {e}")
        return

    combined_content = "Sei un giovane giornalista. Crea un unico contenuto in lingua italiana da tutte le informazioni contenute in [content]\n" + "\n".join(
        f"[source {idx + 1}] {item['content']}" for idx, item in enumerate(json_data))

    logging.info(f"Processing {filepath} - sending to LLM API...")
    rewritten_content = call_llm_api(combined_content)

    if rewritten_content:
        new_data = {
            'title': json_data[0]['title'],
            'content': rewritten_content
        }
        new_filename = REWRITTEN_FOLDER / (Path(filepath).stem + '_rewritten.json')
        try:
            with open(new_filename, 'w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, ensure_ascii=False, indent=4)
            logging.info(f"Rewritten file saved to {new_filename}")
        except IOError as e:
            logging.error(f"Error writing to {new_filename}: {e}")
    else:
        logging.error("Failed to get rewritten content from LLM API.")

def main():
    REWRITTEN_FOLDER.mkdir(parents=True, exist_ok=True)

    json_files = list(OUTPUT_FOLDER.glob('*.json'))
    if not json_files:
        logging.info("No JSON files found in the output folder.")
        return

    for filepath in json_files:
        logging.info(f"Processing file: {filepath}")
        process_json_file(filepath)

if __name__ == "__main__":
    main()
