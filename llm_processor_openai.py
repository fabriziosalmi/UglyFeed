import re
import json
import logging
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# Constants
LLM_API_URL = "https://api.openai.com/v1/chat/completions" # Change this to any OpenAI API compatible LLM inference endpoint
LLM_MODEL = "gpt-3.5-turbo"  # Change this to switch between models (e.g., "gpt-4")
API_KEY = ""  # Add your OpenAI API key here

OUTPUT_FOLDER = Path('output')
REWRITTEN_FOLDER = Path('rewritten')
COMBINED_CONTENT_PREFIX = (
    "Scrivi la notizia unendo tutte le informazioni ottenute dalle fonti in lingua italiana. Sii professionale, preciso, dettagliato e prolisso. "
    "Non scrivere mai TITOLO o TITOLO NOTIZIA o informazioni su di te, scrivi sempre direttamente il fatto e niente altro. "
    "Non ripetere mai le istruzioni ricevute.\n"
    "Hai a tua disposizione diverse fonti per la stessa notizia. Le fonti sono contenute in [content]. "
)

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def call_llm_api(combined_content):
    """ Sends combined content to the OpenAI API and receives a rewritten version. """
    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
                {"role": "user", "content": combined_content}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"API request failed: {e}")
        return None

def ensure_proper_punctuation(text: str) -> str:
    """ Ensure that the text has proper punctuation. """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    corrected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        corrected_sentences.append(sentence)

    return ' '.join(corrected_sentences)

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

    combined_content = COMBINED_CONTENT_PREFIX + "\n".join(
        f"[source {idx + 1}] {item['content']}" for idx, item in enumerate(json_data))

    logging.info(f"Processing {filepath} - combined content prepared.")
    logging.debug(f"Combined content: {combined_content}")

    rewritten_content = call_llm_api(combined_content)

    if rewritten_content:
        # Clean the content from API
        cleaned_content = re.sub(r'\*\*', '', rewritten_content)
        cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
        cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)

        # Ensure proper punctuation
        cleaned_content = ensure_proper_punctuation(cleaned_content)

        # Get all links from the original JSON data
        links = [item['link'] for item in json_data if 'link' in item]

        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_data = {
            'title': json_data[0]['title'],
            'content': cleaned_content,
            'processed_at': current_datetime,  # Add the current date and time
            'links': links  # Add the links
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
        logging.debug(f"Rewritten content: {rewritten_content}")

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
