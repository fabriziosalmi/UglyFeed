# uglycitizen

_quick and dirty initial upload_

- Execute main.py to retrieve feeds and merge by similarity
- Execute llm_processor.py to rewrite and save merged feeds to json

1. it get feeds
2. it aggregates feeds for similarity into new json files
3. it send aggregated news to llm for rewriting
4. it save the rewritten feeds

## Example

```
python main.py
Starting RSS feed processing...
Fetching and parsing RSS feeds...
Fetching feeds: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 81/81 [00:31<00:00,  2.59it/s]
Total articles fetched and parsed: 1790
Grouping articles based on similarity (threshold=0.5)...
Grouping articles: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1790/1790 [00:00<00:00, 2253.98it/s]
Total groups formed: 1444
Saving grouped articles to JSON files...
Saving groups:   0%|                                                                                                                                    | 0/1444 [00:00<?, ?it/s]2024-05-16 09:44:10,074 - INFO - Saved output/20240516_0944-fisioterapista_arrestato_presunto-Q4-S0.45.json with 4 items and similarity score 0.45
2024-05-16 09:44:10,078 - INFO - Saved output/20240516_0944-lambro_preoccupa_milano-Q3-S0.50.json with 3 items and similarity score 0.50
2024-05-16 09:44:10,080 - INFO - Saved output/20240516_0944-chef_rubio_sotto-Q2-S0.42.json with 2 items and similarity score 0.42
2024-05-16 09:44:10,082 - INFO - Saved output/20240516_0944-donna_uccisa_colpo-Q2-S0.41.json with 2 items and similarity score 0.41
2024-05-16 09:44:10,084 - INFO - Saved output/20240516_0944-impianto_pescicoltura_taranto_-Q2-S0.41.json with 2 items and similarity score 0.41
2024-05-16 09:44:10,086 - INFO - Saved output/20240516_0944-alto_contadino_finisce-Q2-S0.52.json with 2 items and similarity score 0.52
2024-05-16 09:44:10,087 - INFO - Saved output/20240516_0944-incendio_casa_palermo_-Q2-S0.30.json with 2 items and similarity score 0.30
2024-05-16 09:44:10,089 - INFO - Saved output/20240516_0944-allerta_meteo_oggi-Q3-S0.38.json with 3 items and similarity score 0.38
2024-05-16 09:44:10,091 - INFO - Saved output/20240516_0944-truffa_ecobonus__savona-Q2-S0.77.json with 2 items and similarity score 0.77
2024-05-16 09:44:10,094 - INFO - Saved output/20240516_0944-madre_figlio_morti-Q3-S0.45.json with 3 items and similarity score 0.45
2024-05-16 09:44:10,096 - INFO - Saved output/20240516_0944-resta_incastrato_operaio-Q2-S0.51.json with 2 items and similarity score 0.51
2024-05-16 09:44:10,097 - INFO - Saved output/20240516_0944-richiesta_domiciliari_italia-Q2-S0.75.json with 2 items and similarity score 0.75
2024-05-16 09:44:10,099 - INFO - Saved output/20240516_0944-problemi_monte_bianco_-Q3-S0.34.json with 3 items and similarity score 0.34
2024-05-16 09:44:10,101 - INFO - Saved output/20240516_0944-prosciolta_della_sapienza-Q2-S0.30.json with 2 items and similarity score 0.30
2024-05-16 09:44:10,103 - INFO - Saved output/20240516_0944-delle_santalucia__inchieste-Q3-S0.34.json with 3 items and similarity score 0.34
2024-05-16 09:44:10,104 - INFO - Saved output/20240516_0944-precipita_banchina_tevere-Q2-S0.36.json with 2 items and similarity score 0.36
2024-05-16 09:44:10,106 - INFO - Saved output/20240516_0944-centro_ippico__muore-Q2-S0.64.json with 2 items and similarity score 0.64
2024-05-16 09:44:10,108 - INFO - Saved output/20240516_0944-metti_giubbotto_gualtieri-Q3-S0.77.json with 3 items and similarity score 0.77
2024-05-16 09:44:10,110 - INFO - Saved output/20240516_0944-spari_contro_premier-Q2-S0.44.json with 2 items and similarity score 0.44
2024-05-16 09:44:10,112 - INFO - Saved output/20240516_0944-copperfield_accusato_abusi-Q2-S0.49.json with 2 items and similarity score 0.49
2024-05-16 09:44:10,114 - INFO - Saved output/20240516_0944-ateneo_california_vara-Q2-S0.60.json with 2 items and similarity score 0.60
2024-05-16 09:44:10,116 - INFO - Saved output/20240516_0944-cambiamento_climatico_degrado-Q5-S0.32.json with 5 items and similarity score 0.32
2024-05-16 09:44:10,118 - INFO - Saved output/20240516_0944-edizione_record_salone-Q2-S0.59.json with 2 items and similarity score 0.59
Saving groups: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1444/1444 [00:00<00:00, 28461.48it/s]
RSS feed processing complete. 33 grouped articles have been saved to the output directory.
Details of groups saved: [5, 6, 3, 5, 3, 3, 5, 4, 3, 3, 5, 3, 3, 4, 3, 6, 4, 3, 5, 4, 3, 3, 4, 3, 6, 3, 3, 3, 5, 4, 3, 3, 4]
(Took 33.46 seconds)

python llm_processor.py
2024-05-16 09:44:14,754 - INFO - Processing file: output/20240516_0944-impianto_pescicoltura_taranto_-Q2-S0.41.json
2024-05-16 09:44:14,754 - INFO - Processing output/20240516_0944-impianto_pescicoltura_taranto_-Q2-S0.41.json - sending to LLM API...
2024-05-16 09:45:14,328 - INFO - Rewritten file saved to rewritten/20240516_0944-impianto_pescicoltura_taranto_-Q2-S0.41_rewritten.json
2024-05-16 09:45:14,329 - INFO - Processing file: output/20240516_0944-cambiamento_climatico_degrado-Q5-S0.32.json
2024-05-16 09:45:14,329 - INFO - Processing output/20240516_0944-cambiamento_climatico_degrado-Q5-S0.32.json - sending to LLM API...
[...]

cat rewritten/20240516_0944-impianto_pescicoltura_taranto_-Q2-S0.41_rewritten.json
{
    "title": "Taranto, impianto di pescicoltura inquinava acqua e suolo: 5 gli indagati",
    "content": "**Emergenza Ambientale: la Guardia Costiera Ittica viola vincoli e compromette Ecosistema Mariano**\n\nInformati emergenti dalla zona costiera italiana: la Guardia Costiera ha subito un grave danno ambientale che potrebbe avere conseguenze devastanti sull'ecosistema marino e sul prodotto ittico. Secondo fonti ufficiali, il danno è stato causato da una serie di azioni incompatibili con i vincoli ambientali e paesaggistici presenti nella zona.\n\nLa notizia è emersa grazie a una indagine condotta dalla Guardia Costiera stessa, la quale ha rilevato che l'ecosistema marino è stato gravemente alterato e il prodotto ittico è stato intossicato. Ciò potrebbe avere ripercussioni negative sulla fauna e sulla flora marina, nonché sull'economia locale.\n\nIl danno ambientale è stato causato da una serie di azioni che hanno violato i vincoli ambientali e paesaggistici presenti nella zona. La Guardia Costiera ha deciso di intraprendere azioni per ripristinare l'ecosistema marino e proteggere il prodotto ittico.\n\nQuesta emergenza ambientale mette in guardia sulla necessità di proteggere i nostri mari e le nostre risorse naturali, affinché possano essere conservate per le generazioni future."
}
```

---

## llm_processor.py

### Code Description

This script processes JSON files in a specified directory, sends their content to a language model API for rewriting, and saves the rewritten content to a new JSON file. Here's a detailed explanation of the code:

#### Imports and Constants
```python
import json
import requests
import logging
from pathlib import Path
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
```
- **json**: For reading and writing JSON files.
- **requests**: For making HTTP requests to the language model API.
- **logging**: For logging informational, debug, and error messages.
- **Path**: For handling file paths in an OS-independent way.
- **sleep**: For adding delays, if needed.
- **HTTPAdapter, Retry**: For configuring retries on HTTP requests.

```python
API_URL = "http://192.168.100.41:11434/api/chat"
OUTPUT_FOLDER = Path('output')
REWRITTEN_FOLDER = Path('rewritten')
RETRIES = 3
BACKOFF_FACTOR = 0.3
HEADERS = {'Content-Type': 'application/json'}
COMBINED_CONTENT_PREFIX = "Sei un giovane giornalista. Crea un unico contenuto in lingua italiana da tutte le informazioni contenute in [content]\n"
```
- **API_URL**: The URL of the language model API.
- **OUTPUT_FOLDER**: The directory where the input JSON files are located.
- **REWRITTEN_FOLDER**: The directory where the rewritten JSON files will be saved.
- **RETRIES**: Number of retries for HTTP requests.
- **BACKOFF_FACTOR**: Factor by which the delay between retries will increase.
- **HEADERS**: Headers to be included in the HTTP request.
- **COMBINED_CONTENT_PREFIX**: Prefix text added to the combined content before sending to the API.

#### Logging Configuration
```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
- Configures logging to display messages with timestamps, log levels, and the actual message.

#### Retry Session Function
```python
def requests_retry_session(retries=RETRIES, backoff_factor=BACKOFF_FACTOR, status_forcelist=(500, 502, 504), session=None):
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
```
- **requests_retry_session**: Configures a `requests.Session` to retry on specific HTTP status codes (500, 502, 504) with exponential backoff.

#### API Call Function
```python
def call_llm_api(combined_content):
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
```
- **call_llm_api**: Sends a POST request to the language model API with the combined content and returns the rewritten content. It uses the retry session for robustness.

#### JSON File Processing Function
```python
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
        logging.debug(f"Rewritten content: {rewritten_content}")
```
- **process_json_file**: Reads a JSON file, prepares combined content, sends it to the LLM API, and writes the rewritten content to a new JSON file. It handles errors during reading, writing, and API calls.

#### Main Function
```python
def main():
    REWRITTEN_FOLDER.mkdir(parents=True, exist_ok=True)

    json_files = list(OUTPUT_FOLDER.glob('*.json'))
    if not json_files:
        logging.info("No JSON files found in the output folder.")
        return

    for filepath in json_files:
        logging.info(f"Processing file: {filepath}")
        process_json_file(filepath)
```
- **main**: Ensures the rewritten folder exists, lists all JSON files in the output folder, and processes each file.

#### Script Entry Point
```python
if __name__ == "__main__":
    main()
```
- Runs the `main` function when the script is executed directly.

### Summary
This script automates the process of reading JSON files, sending their combined content to a language model API for rewriting, and saving the rewritten content to new JSON files. It includes robust error handling, logging for easier debugging, and retry logic for handling transient API request failures.
