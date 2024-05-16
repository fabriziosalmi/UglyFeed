# uglycitizen

_quick and dirty initial upload_

_under active dev then expect the unexpected :)_

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
Fetching and parsing RSS feeds: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 81/81 [00:29<00:00,  2.75it/s]
Total articles fetched and parsed: 1780
Grouping articles based on similarity (threshold=0.5)...
Grouping articles: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1780/1780 [00:01<00:00, 1127.85it/s]
Total groups formed: 1439
Saving grouped articles to JSON files...
Saving groups:   0%|                                                                                                                                    | 0/1439 [00:00<?, ?it/s]2024-05-16 12:02:21,027 - INFO - Saved output/20240516_1202-inchiesta_associazione_monte-Q2-S0.62.json with 2 items and similarity score 0.62
2024-05-16 12:02:21,038 - INFO - Saved output/20240516_1202-milano_livello_lambro-Q2-S0.47.json with 2 items and similarity score 0.47
2024-05-16 12:02:21,044 - INFO - Saved output/20240516_1202-donna_uccisa_colpo-Q2-S0.41.json with 2 items and similarity score 0.41
2024-05-16 12:02:21,049 - INFO - Saved output/20240516_1202-impianto_pescicoltura_taranto_-Q2-S0.41.json with 2 items and similarity score 0.41
2024-05-16 12:02:21,054 - INFO - Saved output/20240516_1202-alto_contadino_finisce-Q2-S0.52.json with 2 items and similarity score 0.52
2024-05-16 12:02:21,058 - INFO - Saved output/20240516_1202-pioggia_così_tanta-Q3-S0.38.json with 3 items and similarity score 0.38
2024-05-16 12:02:21,063 - INFO - Saved output/20240516_1202-allerta_arancione_lombardia-Q2-S0.42.json with 2 items and similarity score 0.42
2024-05-16 12:02:21,068 - INFO - Saved output/20240516_1202-fisioterapista_cliente_ucciso-Q2-S0.50.json with 2 items and similarity score 0.50
2024-05-16 12:02:21,072 - INFO - Saved output/20240516_1202-madre_figlio_morti-Q2-S0.66.json with 2 items and similarity score 0.66
2024-05-16 12:02:21,077 - INFO - Saved output/20240516_1202-resta_incastrato_operaio-Q2-S0.51.json with 2 items and similarity score 0.51
2024-05-16 12:02:21,082 - INFO - Saved output/20240516_1202-richiesta_domiciliari_italia-Q2-S0.75.json with 2 items and similarity score 0.75
2024-05-16 12:02:21,087 - INFO - Saved output/20240516_1202-prosciolta_della_sapienza-Q2-S0.30.json with 2 items and similarity score 0.30
2024-05-16 12:02:21,094 - INFO - Saved output/20240516_1202-delle_santalucia__inchieste-Q3-S0.34.json with 3 items and similarity score 0.34
2024-05-16 12:02:21,101 - INFO - Saved output/20240516_1202-precipita_banchina_tevere-Q2-S0.36.json with 2 items and similarity score 0.36
2024-05-16 12:02:21,107 - INFO - Saved output/20240516_1202-centro_ippico__muore-Q2-S0.64.json with 2 items and similarity score 0.64
Saving groups:  19%|██████████████████████▊                                                                                                 | 274/1439 [00:00<00:00, 2657.38it/s]2024-05-16 12:02:21,113 - INFO - Saved output/20240516_1202-metti_giubbotto_gualtieri-Q3-S0.77.json with 3 items and similarity score 0.77
2024-05-16 12:02:21,120 - INFO - Saved output/20240516_1202-passa_superbonus_senato-Q3-S0.34.json with 3 items and similarity score 0.34
2024-05-16 12:02:21,143 - INFO - Saved output/20240516_1202-paesi_italia_rimpatriati-Q4-S0.43.json with 4 items and similarity score 0.43
2024-05-16 12:02:21,149 - INFO - Saved output/20240516_1202-ateneo_california_vara-Q2-S0.60.json with 2 items and similarity score 0.60
2024-05-16 12:02:21,156 - INFO - Saved output/20240516_1202-cambiamento_climatico_degrado-Q5-S0.32.json with 5 items and similarity score 0.32
2024-05-16 12:02:21,162 - INFO - Saved output/20240516_1202-dipinto_monet_venduto-Q2-S0.87.json with 2 items and similarity score 0.87
2024-05-16 12:02:21,167 - INFO - Saved output/20240516_1202-edizione_record_salone-Q2-S0.59.json with 2 items and similarity score 0.59
Saving groups: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1439/1439 [00:00<00:00, 8763.92it/s]
RSS feed processing complete. 33 different articles are now grouped.
Details of groups saved: [3, 4, 5, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 4, 3, 4, 3, 6, 4, 5, 3, 5, 3, 3, 4, 3, 3, 4]
(Took 33.86 seconds)
Summarizing output files:
20240516_1202-prosciolta_della_sapienza-Q2-S0.30.json: 12 lines
20240516_1202-passa_superbonus_senato-Q3-S0.34.json: 17 lines
20240516_1202-delle_santalucia__inchieste-Q3-S0.34.json: 17 lines
20240516_1202-madre_figlio_morti-Q2-S0.66.json: 12 lines
20240516_1202-pioggia_così_tanta-Q3-S0.38.json: 17 lines
20240516_1202-edizione_record_salone-Q2-S0.59.json: 12 lines
20240516_1202-resta_incastrato_operaio-Q2-S0.51.json: 12 lines
20240516_1202-metti_giubbotto_gualtieri-Q3-S0.77.json: 17 lines
20240516_1202-inchiesta_associazione_monte-Q2-S0.62.json: 12 lines
20240516_1202-ateneo_california_vara-Q2-S0.60.json: 12 lines
20240516_1202-paesi_italia_rimpatriati-Q4-S0.43.json: 22 lines
20240516_1202-centro_ippico__muore-Q2-S0.64.json: 12 lines
20240516_1202-alto_contadino_finisce-Q2-S0.52.json: 12 lines
20240516_1202-cambiamento_climatico_degrado-Q5-S0.32.json: 27 lines
20240516_1202-donna_uccisa_colpo-Q2-S0.41.json: 12 lines
20240516_1202-milano_livello_lambro-Q2-S0.47.json: 12 lines
20240516_1202-impianto_pescicoltura_taranto_-Q2-S0.41.json: 12 lines
20240516_1202-dipinto_monet_venduto-Q2-S0.87.json: 12 lines
20240516_1202-allerta_arancione_lombardia-Q2-S0.42.json: 12 lines
20240516_1202-precipita_banchina_tevere-Q2-S0.36.json: 12 lines
20240516_1202-richiesta_domiciliari_italia-Q2-S0.75.json: 12 lines
20240516_1202-fisioterapista_cliente_ucciso-Q2-S0.50.json: 12 lines
Total output files: 22

python llm_processor.py
2024-05-16 12:03:01,675 - INFO - Processing file: output/20240516_1202-prosciolta_della_sapienza-Q2-S0.30.json
2024-05-16 12:03:01,676 - INFO - Processing output/20240516_1202-prosciolta_della_sapienza-Q2-S0.30.json - combined content prepared.
2024-05-16 12:04:12,432 - INFO - Rewritten file saved to rewritten/20240516_1202-prosciolta_della_sapienza-Q2-S0.30_rewritten.json
[...]

cat rewritten/20240516_1202-prosciolta_della_sapienza-Q2-S0.30_rewritten.json
{
    "title": "Prosciolta prof della Sapienza querelata da Lollobrigida",
    "content": "**LA CRIMINALIZZAZIONE DEL DISSENSO FA TEMERE**\n\nUn docente, soddisfatta ma preoccupata per la situazione attuale, ha espresso le sue paure sulla crescente tendenza a criminalizzare il dissenso. La sua voce è solo uno dei tanti warning che vengono emessi da molti settori della società civile, che si sentono minacciati dalle recenti azioni del governo.\n\nSecondo il docente, la criminalizzazione del dissenso non è solo un problema per i movimenti sociali e politici, ma anche una minaccia per la democrazia stessa. \"La libertà di espressione è essenziale per la salute di qualsiasi società democratica\", ha affermato. \"Se noi permettiamo che il dissenso venga criminalizzato, stiamo aprendo la porta ai totalitarismi\".\n\nLa sua voce si aggiunge a quella del ministro Di Cesare, che ha recentemente querelato una delle maggiori testate giornalistiche del paese. \"Preoccupa la criminalizzazione\", ha detto il ministro. \"Non vogliamo che la libertà di espressione venga limitata\".\n\nLa situazione attuale è quindi molto preoccupante. La criminalizzazione del dissenso può portare a una repressione delle opinioni diverse, alla chiusura dei canali di comunicazione e all'eliminazione della critica sociale. Ecco perché è importante che noi, come società civile, ci organiziamo per difendere la libertà di espressione e la democrazia.\n\nFonti:\n[source 1]\n[source 2]"
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
