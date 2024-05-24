# Scripts documentation
Welcome to the Scripts Documentation section. This comprehensive guide provides detailed information and instructions for each script in our project. I use to complete the docs also to catch some placeholder functions around the code and replace it with usable stuff :)

**Demo script**
- [demo.sh](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#demosh)

**Main scripts**
- [main.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#mainpy)
- [llm_processor.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#llm_processorpy)
- [llm_processor_openai.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#llm_processor_openaipy)
- [json2rss.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#json2rsspy)
- [serve.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#servepy)

**Optional scripts**
- [evaluate_against_reference.py]()
- [evaluate_cohesion_concreteness.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#evaluate_cohesion_concretenesspy)

Each script's documentation includes the following sections:

- **Overview**
A brief introduction to the script, explaining its purpose and the specific problem it aims to solve.

- **Installation**
Detailed instructions on how to install any necessary dependencies and set up the script in your environment.

- **Usage**
Step-by-step instructions on how to run the script, including command-line arguments, configuration options, and practical examples.

- **Functionality**
A deep dive into the core functionality of the script, describing key functions and modules, and how they work together.

- **Input/Output**
Information about the expected input formats and the structure of the output data, ensuring users understand what the script requires and what it produces.

- **Code Structure**
An overview of the script's architecture, highlighting major components and their interactions, to give users a clear understanding of how the script is built.


---
## demo.sh

### Overview
This script is designed to automate the process of interacting with different language model APIs (OpenAI or Ollama) to process RSS feeds and serve the processed data. It guides the user through selecting an API, specifying model parameters, and then runs a sequence of Python scripts to handle the data processing and serving.

### Installation
To set up this script in your environment, follow these steps:

1. **Clone the repository (if applicable)**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Python dependencies**:
   Ensure you have Python 3 installed. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (if necessary):
   - For OpenAI API, ensure you have an API key.
   - For Ollama API, ensure the Ollama API is running and accessible.

### Usage
To run the script, follow these steps:

1. **Make the script executable** (if it isn't already):
   ```bash
   chmod +x script.sh
   ```

2. **Run the script**:
   ```bash
   ./script.sh
   ```

3. **Follow the prompts**:
   - Enter the RSS feeds.
   - Select the API (Ollama or OpenAI).
   - Provide the necessary API keys or URLs.
   - Choose the appropriate language model.

### Functionality
The script consists of several key functions:

- **prompt**: Prompts the user for input and returns the input.
- **select_api**: Guides the user through selecting the API (Ollama or OpenAI).
- **select_llm_model**: Prompts the user to select the appropriate language model based on the chosen API.

After gathering the necessary inputs, the script:
1. **Saves the RSS feeds** to a file.
2. **Starts the main processing** by running `main.py`.
3. **Processes the feeds** using the selected API and model (`llm_processor.py` or `llm_processor_openai.py`).
4. **Converts the processed data** to RSS format using `json2rss.py`.
5. **Serves the processed data** using `serve.py`.

### Input/Output
**Input**:
- A list of RSS feeds provided by the user.
- API selection (Ollama or OpenAI).
- Specific model selection within the chosen API.
- API keys or URLs for authentication.

**Output**:
- Processed RSS feeds saved in the specified format.
- A running server providing access to the processed data.

### Code Structure
The script is organized as follows:

1. **User Input Section**:
   - Prompts for RSS feeds, API selection, and model selection.
   
2. **API and Model Configuration**:
   - Saves the RSS feeds to `input/feeds.txt`.
   - Prompts for API keys or URLs.

3. **Execution of Processing Scripts**:
   - Runs `main.py` to initiate the processing.
   - Runs the appropriate LLM processing script based on user selection (`llm_processor.py` for Ollama, `llm_processor_openai.py` for OpenAI).

4. **Conversion and Serving**:
   - Converts the processed data to RSS format using `json2rss.py`.
   - Starts the server using `serve.py`.

### Detailed Script Breakdown

**1. Prompt for RSS Feeds**:
```bash
echo "Please enter up to 100 RSS feeds, either separated by spaces or one per line. Enter an empty line to finish:"
rss_feeds=()
while IFS= read -r line; do
  [[ -z "$line" ]] && break
  rss_feeds+=("$line")
done
```
This block collects the RSS feeds from the user.

**2. Select API**:
```bash
select_api
```
This function prompts the user to choose between Ollama and OpenAI APIs.

**3. Select LLM Model**:
```bash
select_llm_model
```
Based on the selected API, this function prompts the user to choose a language model.

**4. Execute Processing Scripts**:
```bash
python3 main.py
python3 llm_processor.py --model phi3 --api_url "$ollama_url"
```
These lines run the main processing script and the appropriate LLM processing script.

**5. Serve Processed Data**:
```bash
python3 serve.py
```
This command starts a server to serve the processed RSS data.

This script provides a guided, interactive way to process and serve RSS feeds using different language model APIs, ensuring flexibility and ease of use.


## main.py

### Overview
This Python script processes RSS feeds, groups similar articles based on a similarity threshold, and saves the grouped articles as JSON files. It is designed to automate the aggregation and organization of news articles from various RSS feeds, making it easier to identify and manage similar content.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Install necessary Python packages**:
   This script may depend on additional packages for RSS fetching, similarity checking, and JSON handling. Ensure you have them installed by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the directory structure**:
   Ensure you have an `input` directory containing your `feeds.txt` file and create an `output` directory for the results:
   ```bash
   mkdir -p input output
   ```

### Usage
To run the script, follow these steps:

1. **Place your RSS feeds list**:
   Ensure your `feeds.txt` file with RSS feed URLs is located in the `input` directory.

2. **Execute the script** with the desired similarity threshold:
   ```bash
   python3 main.py --threshold 0.5
   ```
   Adjust the `--threshold` value as needed.

3. **Check the output**:
   The grouped articles will be saved as JSON files in the `output` directory.

### Functionality
The script includes the following key functions:

- **fetch_feeds_from_file(input_file_path)**: Reads RSS feed URLs from a file and fetches the articles.

- **group_similar_articles(articles, similarity_threshold)**: Groups articles based on a similarity threshold.

- **save_grouped_articles(grouped_articles, output_dir)**: Saves the grouped articles as JSON files.

### Input/Output
**Input**:
- A text file named `feeds.txt` located in the `input` directory. This file should contain RSS feed URLs, one per line.

**Output**:
- JSON files saved in the `output` directory. Each file contains grouped articles based on the specified similarity threshold.

### Code Structure
The script is structured as follows:

1. **Imports and Argument Parsing**:
   ```python
   import os
   import argparse
   import time
   from rss_reader import fetch_feeds_from_file
   from similarity_checker import group_similar_articles
   from json_manager import save_grouped_articles
   ```

2. **Main Function**:
   Orchestrates the entire process of fetching, grouping, and saving articles.
   ```python
   def main(similarity_threshold: float) -> None:
       print("Starting RSS feed processing...")
       input_file_path = 'input/feeds.txt'
       start_time = time.time()

       print("Fetching and parsing RSS feeds...")
       articles = fetch_feeds_from_file(input_file_path)
       print(f"Total articles fetched and parsed: {len(articles)}")

       print(f"Grouping articles based on similarity (threshold={similarity_threshold})...")
       grouped_articles = group_similar_articles(articles, similarity_threshold)
       print(f"Total groups formed: {len(grouped_articles)}")

       print("Saving grouped articles to JSON files...")
       group_sizes = save_grouped_articles(grouped_articles, 'output')
       total_files_saved = len(group_sizes)

       elapsed_time = time.time() - start_time
       print(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
       print(f"Details of groups saved: {group_sizes}")
       print(f"(Took {elapsed_time:.2f} seconds)")

       print("Summarizing output files:")
       output_files = os.listdir('output')
       for filename in output_files:
           path = os.path.join('output', filename)
           with open(path, 'r', encoding='utf-8') as file:
               line_count = sum(1 for _ in file)
           print(f"{filename}: {line_count} lines")
       print(f"Total output files: {len(output_files)}")
   ```

3. **Argument Parsing and Script Execution**:
   Parses command-line arguments and runs the main function.
   ```python
   if __name__ == "__main__":
       parser = argparse.ArgumentParser(
           description='Process RSS feeds and group similar articles based on a similarity threshold.'
       )
       parser.add_argument(
           '-t', '--threshold', type=float, default=0.5,
           help='Set the similarity threshold for grouping articles (default: 0.5).'
       )
       args = parser.parse_args()
       main(args.threshold)
   ```

### Detailed Script Breakdown

**1. Imports and Argument Parsing**:
   Imports necessary modules and sets up command-line argument parsing.
   ```python
   import os
   import argparse
   import time
   from rss_reader import fetch_feeds_from_file
   from similarity_checker import group_similar_articles
   from json_manager import save_grouped_articles
   ```

**2. Main Function**:
   Processes the RSS feeds, groups similar articles, and saves them.
   ```python
   def main(similarity_threshold: float) -> None:
       print("Starting RSS feed processing...")
       input_file_path = 'input/feeds.txt'
       start_time = time.time()

       print("Fetching and parsing RSS feeds...")
       articles = fetch_feeds_from_file(input_file_path)
       print(f"Total articles fetched and parsed: {len(articles)}")

       print(f"Grouping articles based on similarity (threshold={similarity_threshold})...")
       grouped_articles = group_similar_articles(articles, similarity_threshold)
       print(f"Total groups formed: {len(grouped_articles)}")

       print("Saving grouped articles to JSON files...")
       group_sizes = save_grouped_articles(grouped_articles, 'output')
       total_files_saved = len(group_sizes)

       elapsed_time = time.time() - start_time
       print(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
       print(f"Details of groups saved: {group_sizes}")
       print(f"(Took {elapsed_time:.2f} seconds)")

       print("Summarizing output files:")
       output_files = os.listdir('output')
       for filename in output_files:
           path = os.path.join('output', filename)
           with open(path, 'r', encoding='utf-8') as file:
               line_count = sum(1 for _ in file)
           print(f"{filename}: {line_count} lines")
       print(f"Total output files: {len(output_files)}")
   ```

**3. Argument Parsing and Script Execution**:
   Parses the similarity threshold argument and runs the main function.
   ```python
   if __name__ == "__main__":
       parser = argparse.ArgumentParser(
           description='Process RSS feeds and group similar articles based on a similarity threshold.'
       )
       parser.add_argument(
           '-t', '--threshold', type=float, default=0.5,
           help='Set the similarity threshold for grouping articles (default: 0.5).'
       )
       args = parser.parse_args()
       main(args.threshold)
   ```

This script provides a comprehensive solution for processing and organizing RSS feed articles, making it easier to manage and analyze large volumes of news content.

## llm_processor.py

### Overview
This Python script processes JSON files containing news articles, calls a language model API to rewrite the content, and saves the rewritten articles into a separate directory. The purpose of this script is to integrate and harmonize information from various sources, ensuring the final content is clear, complete, and coherent.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Install necessary Python packages**:
   This script relies on several Python libraries. Install them using:
   ```bash
   pip install requests
   ```

3. **Set up the directory structure**:
   Ensure you have `output` and `rewritten` directories. Place your original JSON files in the `output` directory.

### Usage
To run the script, follow these steps:

1. **Prepare your JSON files**:
   Ensure your JSON files are located in the `output` directory.

2. **Execute the script** with the required arguments:
   ```bash
   python3 llm_processor.py --api_url <API_URL> --model <MODEL>
   ```
   Replace `<API_URL>` with the URL of the language model API and `<MODEL>` with the model you wish to use.

3. **Check the output**:
   The rewritten articles will be saved in the `rewritten` directory.

### Functionality
The script includes the following key functions:

- **requests_retry_session**: Configures a requests session with retry logic to handle temporary network issues.

- **call_llm_api**: Sends the combined content to the language model API and retrieves the rewritten content.

- **ensure_proper_punctuation**: Ensures that the rewritten content has proper punctuation.

- **process_json_file**: Reads a JSON file, combines the content, calls the API, processes the response, and saves the rewritten content.

### Input/Output
**Input**:
- JSON files located in the `output` directory. Each file should contain multiple articles.

**Output**:
- Rewritten JSON files saved in the `rewritten` directory, with a `_rewritten.json` suffix.

### Code Structure
The script is structured as follows:

1. **Imports and Constants**:
   ```python
   import re
   import json
   import requests
   import logging
   import argparse
   from pathlib import Path
   from time import sleep
   from datetime import datetime
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry

   OUTPUT_FOLDER = Path('output')
   REWRITTEN_FOLDER = Path('rewritten')
   RETRIES = 3
   BACKOFF_FACTOR = 0.3
   HEADERS = {'Content-Type': 'application/json'}
   COMBINED_CONTENT_PREFIX = (
       "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato..."
   )
   ```

2. **requests_retry_session Function**:
   Configures a session with retry logic.
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

3. **call_llm_api Function**:
   Sends combined content to the API and retrieves the response.
   ```python
   def call_llm_api(api_url, model, combined_content):
       data = json.dumps({
           "model": model,
           "messages": [{"role": "user", "content": combined_content}],
           "stream": False
       })
       try:
           response = requests_retry_session().post(api_url, data=data, headers=HEADERS)
           response.raise_for_status()
           return response.json()['message']['content']
       except requests.RequestException as e:
           logging.error(f"API request failed: {e}")
           return None
   ```

4. **ensure_proper_punctuation Function**:
   Ensures proper punctuation in the text.
   ```python
   def ensure_proper_punctuation(text: str) -> str:
       sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
       corrected_sentences = []
       for sentence in sentences:
           sentence = sentence.strip()
           if sentence and not sentence.endswith('.'):
               sentence += '.'
           corrected_sentences.append(sentence)
       return ' '.join(corrected_sentences)
   ```

5. **process_json_file Function**:
   Processes a JSON file, calls the API, and saves the rewritten content.
   ```python
   def process_json_file(filepath, api_url, model):
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

       rewritten_content = call_llm_api(api_url, model, combined_content)

       if rewritten_content:
           cleaned_content = re.sub(r'\*\*', '', rewritten_content)
           cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
           cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = ensure_proper_punctuation(cleaned_content)

           links = [item['link'] for item in json_data if 'link' in item]
           current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

           new_data = {
               'title': json_data[0]['title'],
               'content': cleaned_content,
               'processed_at': current_datetime,
               'links': links
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

6. **main Function**:
   Parses arguments and processes all JSON files in the `output` directory.
   ```python
   def main():
       parser = argparse.ArgumentParser(description='Process JSON files and call LLM API.')
       parser.add_argument('--api_url', type=str, required=True, help='The URL of the LLM API.')
       parser.add_argument('--model', type=str, required=True, help='The model to use for the LLM API.')

       args = parser.parse_args()

       REWRITTEN_FOLDER.mkdir(parents=True, exist_ok=True)

       json_files = list(OUTPUT_FOLDER.glob('*.json'))
       if not json_files:
           logging.info("No JSON files found in the output folder.")
           return

       for filepath in json_files:
           logging.info(f"Processing file: {filepath}")
           process_json_file(filepath, args.api_url, args.model)

   if __name__ == "__main__":
       main()
   ```

This script provides a robust solution for processing and rewriting news articles using a language model API, ensuring high-quality and coherent output suitable for various applications.

## llm_processor_openai.py

### Overview
This Python script processes JSON files containing news articles, calls the OpenAI API to rewrite the content, and saves the rewritten articles into a separate directory. The purpose of this script is to combine and harmonize information from various sources, ensuring the final content is clear, complete, and coherent.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Install necessary Python packages**:
   This script relies on several Python libraries. Install them using:
   ```bash
   pip install openai
   ```

3. **Set up the directory structure**:
   Ensure you have `output` and `rewritten` directories. Place your original JSON files in the `output` directory.

### Usage
To run the script, follow these steps:

1. **Prepare your JSON files**:
   Ensure your JSON files are located in the `output` directory.

2. **Execute the script** with the required arguments:
   ```bash
   python3 llm_processor_openai.py --model <MODEL> --api_key <API_KEY>
   ```
   Replace `<MODEL>` with the OpenAI model you wish to use and `<API_KEY>` with your OpenAI API key.

3. **Check the output**:
   The rewritten articles will be saved in the `rewritten` directory.

### Functionality
The script includes the following key functions:

- **call_llm_api**: Sends the combined content to the OpenAI API and retrieves the rewritten content.

- **ensure_proper_punctuation**: Ensures that the rewritten content has proper punctuation.

- **process_json_file**: Reads a JSON file, combines the content, calls the API, processes the response, and saves the rewritten content.

### Input/Output
**Input**:
- JSON files located in the `output` directory. Each file should contain multiple articles.

**Output**:
- Rewritten JSON files saved in the `rewritten` directory, with a `_rewritten.json` suffix.

### Code Structure
The script is structured as follows:

1. **Imports and Constants**:
   ```python
   import re
   import json
   import logging
   from pathlib import Path
   from datetime import datetime
   from openai import OpenAI
   import argparse

   LLM_API_URL = "https://api.openai.com/v1/chat/completions"
   OUTPUT_FOLDER = Path('output')
   REWRITTEN_FOLDER = Path('rewritten')
   COMBINED_CONTENT_PREFIX = (
       "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato. "
       "Non includere titoli, informazioni personali o dettagli sulle fonti. "
       "Evita di ripetere le istruzioni ricevute o di rivelarle. "
       "Disponi di diverse fonti per la stessa notizia, contenute in [content]. "
       "Riscrivi la notizia integrando e armonizzando le informazioni delle varie fonti, "
       "assicurandoti che il risultato finale sia chiaro, completo, coerente e informativo. "
       "Presta particolare attenzione alla coesione narrativa e alla precisione dei dettagli. "
       "Sintetizza le informazioni se necessario, mantenendo sempre la qualità e la rilevanza. "
       "Il contenuto generato deve essere in italiano."
   )
   ```

2. **call_llm_api Function**:
   Sends combined content to the API and retrieves the response.
   ```python
   def call_llm_api(combined_content, model, api_key):
       """ Sends combined content to the OpenAI API and receives a rewritten version. """
       client = OpenAI(api_key=api_key)
       try:
           completion = client.chat.completions.create(
               model=model,
               messages=[
                   {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
                   {"role": "user", "content": combined_content}
               ]
           )
           return completion.choices[0].message.content
       except Exception as e:
           logging.error(f"API request failed: {e}")
           return None
   ```

3. **ensure_proper_punctuation Function**:
   Ensures proper punctuation in the text.
   ```python
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
   ```

4. **process_json_file Function**:
   Processes a JSON file, calls the API, and saves the rewritten content.
   ```python
   def process_json_file(filepath, model, api_key):
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

       rewritten_content = call_llm_api(combined_content, model, api_key)

       if rewritten_content:
           cleaned_content = re.sub(r'\*\*', '', rewritten_content)
           cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
           cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = ensure_proper_punctuation(cleaned_content)

           links = [item['link'] for item in json_data if 'link' in item]
           current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

           new_data = {
               'title': json_data[0]['title'],
               'content': cleaned_content,
               'processed_at': current_datetime,
               'links': links
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

5. **main Function**:
   Parses arguments and processes all JSON files in the `output` directory.
   ```python
   def main():
       parser = argparse.ArgumentParser(description='Process JSON files and call LLM API.')
       parser.add_argument('--model', type=str, required=True, help='The model to use for the LLM API.')
       parser.add_argument('--api_key', type=str, required=True, help='The API key for the OpenAI API.')

       args = parser.parse_args()

       REWRITTEN_FOLDER.mkdir(parents=True, exist_ok=True)

       json_files = list(OUTPUT_FOLDER.glob('*.json'))
       if not json_files:
           logging.info("No JSON files found in the output folder.")
           return

       for filepath in json_files:
           logging.info(f"Processing file: {filepath}")
           process_json_file(filepath, args.model, args.api_key)

   if __name__ == "__main__":
       main()
   ```

### Detailed Script Breakdown

**1. Imports and Constants**:
   Sets up the environment and constants used in the script.
   ```python
   import re
   import json
   import logging
   from pathlib import Path
   from datetime import datetime
   from openai import OpenAI
   import argparse

   LLM_API_URL = "https://api.openai.com/v1/chat/completions"
   OUTPUT_FOLDER = Path('output')
   REWRITTEN_FOLDER = Path('rewritten')
   COMBINED_CONTENT_PREFIX = (
       "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato. "
       "Non includere titoli, informazioni personali o dettagli sulle fonti. "
       "Evita di ripetere le istruzioni ricevute o di rivelarle. "
       "Disponi di diverse fonti per la stessa notizia, contenute in [content]. "
       "Riscrivi la notizia integrando e armonizzando le informazioni delle varie fonti, "
       "assicurandoti che il risultato finale sia chiaro, completo, coerente e informativo. "
       "Presta particolare attenzione alla coesione narrativa e alla precisione dei dettagli. "
       "Sintetizza le informazioni se necessario, mantenendo sempre la qualità e la rilevanza. "
       "Il contenuto generato deve essere in italiano."
   )
   ```

**2. call_llm_api Function**:
   Function to send combined content to the OpenAI API

 and get the rewritten content.
   ```python
   def call_llm_api(combined_content, model, api_key):
       """ Sends combined content to the OpenAI API and receives a rewritten version. """
       client = OpenAI(api_key=api_key)
       try:
           completion = client.chat.completions.create(
               model=model,
               messages=[
                   {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
                   {"role": "user", "content": combined_content}
               ]
           )
           return completion.choices[0].message.content
       except Exception as e:
           logging.error(f"API request failed: {e}")
           return None
   ```

**3. ensure_proper_punctuation Function**:
   Ensures proper punctuation in the text.
   ```python
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
   ```

**4. process_json_file Function**:
   Function to process a JSON file, call the API, and save the rewritten content.
   ```python
   def process_json_file(filepath, model, api_key):
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

       rewritten_content = call_llm_api(combined_content, model, api_key)

       if rewritten_content:
           cleaned_content = re.sub(r'\*\*', '', rewritten_content)
           cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
           cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)
           cleaned_content = ensure_proper_punctuation(cleaned_content)

           links = [item['link'] for item in json_data if 'link' in item]
           current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

           new_data = {
               'title': json_data[0]['title'],
               'content': cleaned_content,
               'processed_at': current_datetime,
               'links': links
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

**5. main Function**:
   Parses arguments and processes all JSON files in the `output` directory.
   ```python
   def main():
       parser = argparse.ArgumentParser(description='Process JSON files and call LLM API.')
       parser.add_argument('--model', type=str, required=True, help='The model to use for the LLM API.')
       parser.add_argument('--api_key', type=str, required=True, help='The API key for the OpenAI API.')

       args = parser.parse_args()

       REWRITTEN_FOLDER.mkdir(parents=True, exist_ok=True)

       json_files = list(OUTPUT_FOLDER.glob('*.json'))
       if not json_files:
           logging.info("No JSON files found in the output folder.")
           return

       for filepath in json_files:
           logging.info(f"Processing file: {filepath}")
           process_json_file(filepath, args.model, args.api_key)

   if __name__ == "__main__":
       main()
   ```

This script provides a robust solution for processing and rewriting news articles using the OpenAI API, ensuring high-quality and coherent output suitable for various applications.

## json2rss.py

### Overview
This Python script processes JSON files containing news articles and generates an RSS feed. It reads JSON files from a specified directory, extracts relevant information, and creates an RSS feed in XML format. The script aims to automate the conversion of JSON-formatted news data into a standard RSS feed that can be used for news aggregation.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Install necessary Python packages**:
   This script uses the built-in Python libraries, so no additional packages are required. However, if you use a virtual environment, you can set it up as follows:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Set up the directory structure**:
   Ensure that you have a directory named `rewritten` containing your `_rewritten.json` files.

### Usage
To run the script, follow these steps:

1. **Place your JSON files**:
   Ensure your `_rewritten.json` files are located in the `rewritten` directory.

2. **Execute the script**:
   Run the script using Python:
   ```bash
   python3 json2rss.py
   ```

3. **Check the output**:
   The RSS feed will be generated in the `uglyfeeds` directory as `uglyfeed.xml`.

### Functionality
The script includes the following key functions:

- **read_json_files(directory)**: Reads all JSON files ending with `_rewritten.json` from the specified directory and returns their content as a list of dictionaries.

- **create_rss_feed(json_data, output_path)**: Creates an RSS feed in XML format using the provided JSON data and saves it to the specified output path.

- **main()**: Main function that orchestrates the reading of JSON files, RSS feed creation, and directory setup.

### Input/Output
**Input**:
- JSON files located in the `rewritten` directory. Each file should have a filename ending with `_rewritten.json`.

**Output**:
- An RSS feed saved as `uglyfeed.xml` in the `uglyfeeds` directory.

### Code Structure
The script is structured as follows:

1. **Imports and Namespace Registration**:
   ```python
   import json
   import os
   import urllib.parse
   from datetime import datetime
   from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

   register_namespace('atom', 'http://www.w3.org/2005/Atom')
   ```

2. **read_json_files(directory)**:
   Reads JSON files from a directory.
   ```python
   def read_json_files(directory):
       json_data = []
       for filename in os.listdir(directory):
           if filename.endswith('_rewritten.json'):
               filepath = os.path.join(directory, filename)
               with open(filepath, 'r') as f:
                   data = json.load(f)
                   json_data.append(data)
       return json_data
   ```

3. **create_rss_feed(json_data, output_path)**:
   Constructs an RSS feed from the JSON data and writes it to the output path.
   ```python
   def create_rss_feed(json_data, output_path):
       rss = Element('rss')
       rss.set('version', '2.0')
       rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

       channel = SubElement(rss, 'channel')

       title = SubElement(channel, 'title')
       title.text = "Feed di Notizie UglyCitizen"

       link = SubElement(channel, 'link')
       link.text = "https://github.com/fabriziosalmi/UglyFeed"

       description = SubElement(channel, 'description')
       description.text = "Feed di notizie aggregato e riscritto da UglyCitizen"

       language = SubElement(channel, 'language')
       language.text = "it"

       atom_link = SubElement(channel, 'atom:link')
       atom_link.set('href', 'https://github.com/fabriziosalmi/UglyFeed/uglyfeeds/uglyfeed.xml')
       atom_link.set('rel', 'self')
       atom_link.set('type', 'application/rss+xml')

       for item in json_data:
           item_element = SubElement(channel, 'item')

           item_title = SubElement(item_element, 'title')
           item_title.text = item.get('title', 'Nessun Titolo')

           item_description = SubElement(item_element, 'description')
           content = item.get('content', 'Nessun Contenuto')

           if 'links' in item:
               content += "<br/><br/><small>Fonti:</small><br/>"
               for link in item['links']:
                   content += f'<small><a href="{link}" target="_blank">{link}</a></small><br/>'

           item_description.text = content

           pubDate = SubElement(item_element, 'pubDate')
           processed_at = item.get('processed_at', datetime.now().isoformat())
           pubDate.text = datetime.strptime(processed_at, '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y %H:%M:%S GMT')

           guid = SubElement(item_element, 'guid')
           guid.text = "https://github.com/fabriziosalmi/UglyFeed/{}".format(urllib.parse.quote(item.get('title', 'Nessun Titolo')))

       tree = ElementTree(rss)
       tree.write(output_path, encoding='utf-8', xml_declaration=True)
   ```

4. **main()**:
   Sets up directories, reads JSON data, and creates the RSS feed.
   ```python
   def main():
       rewritten_dir = 'rewritten'
       output_path = os.path.join('uglyfeeds', 'uglyfeed.xml')

       os.makedirs('uglyfeeds', exist_ok=True)

       json_data = read_json_files(rewritten_dir)

       if json_data:
           create_rss_feed(json_data, output_path)
           print(f'RSS feed successfully created at {output_path}')
       else:
           print('Nessun file JSON trovato nella directory riscritta.')

   if __name__ == '__main__':
       main()
   ```

This script provides a straightforward way to convert JSON news data into an RSS feed, making it easy to integrate with RSS readers or news aggregation services.

## serve.py

### Overview
This Python script sets up a simple HTTP server to serve an RSS feed file (`uglyfeed.xml`) from a specified directory (`uglyfeeds`). It is designed to provide easy access to the RSS feed by hosting it locally, making it accessible via a web browser or any RSS feed reader.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Set up the directory structure**:
   Ensure that you have an `uglyfeeds` directory containing the `uglyfeed.xml` file.

### Usage
To run the script, follow these steps:

1. **Place the RSS feed file**:
   Ensure your `uglyfeed.xml` file is located in the `uglyfeeds` directory.

2. **Execute the script**:
   Run the script using Python:
   ```bash
   python3 serve.py
   ```

3. **Access the RSS feed**:
   Open a web browser or RSS reader and navigate to the URL displayed in the console (e.g., `http://<local_ip>:8000/uglyfeed.xml`).

### Functionality
The script includes the following key components:

- **UglyFeedHandler**: A custom HTTP request handler that serves the `uglyfeed.xml` file when the root URL (`/`) is accessed.

- **get_local_ip()**: A function to retrieve the local IP address of the machine running the server.

- **run(server_class, handler_class, port)**: Sets up and starts the HTTP server, making the RSS feed file accessible.

### Input/Output
**Input**:
- The `uglyfeed.xml` file located in the `uglyfeeds` directory.

**Output**:
- An HTTP server running locally, serving the `uglyfeed.xml` file, accessible via a web browser or RSS reader.

### Code Structure
The script is structured as follows:

1. **Imports and Directory Setup**:
   ```python
   import http.server
   import socket
   import os
   from urllib.parse import urljoin

   uglyfeeds_dir = 'uglyfeeds'
   uglyfeed_file = 'uglyfeed.xml'
   os.chdir(uglyfeeds_dir)
   ```

2. **UglyFeedHandler Class**:
   Custom HTTP request handler to serve the `uglyfeed.xml` file.
   ```python
   class UglyFeedHandler(http.server.SimpleHTTPRequestHandler):
       def do_GET(self):
           if self.path == '/':
               self.path = f'/{uglyfeed_file}'
           return super().do_GET()
   ```

3. **get_local_ip() Function**:
   Retrieves the local IP address of the machine running the server.
   ```python
   def get_local_ip():
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       try:
           s.connect(('10.254.254.254', 1))
           local_ip = s.getsockname()[0]
       except Exception:
           local_ip = '127.0.0.1'
       finally:
           s.close()
       return local_ip
   ```

4. **run() Function**:
   Sets up and starts the HTTP server.
   ```python
   def run(server_class=http.server.HTTPServer, handler_class=UglyFeedHandler, port=8000):
       server_address = ('', port)
       httpd = server_class(server_address, handler_class)
       local_ip = get_local_ip()
       final_url = urljoin(f'http://{local_ip}:{port}/', uglyfeed_file)
       print(f'Serving {uglyfeed_file} at: {final_url}')
       httpd.serve_forever()
   ```

5. **Script Execution**:
   Starts the server when the script is executed directly.
   ```python
   if __name__ == '__main__':
       run()
   ```

### Detailed Script Breakdown

**1. Imports and Directory Setup**:
   Sets up the environment and changes to the directory containing the `uglyfeed.xml` file.
   ```python
   import http.server
   import socket
   import os
   from urllib.parse import urljoin

   uglyfeeds_dir = 'uglyfeeds'
   uglyfeed_file = 'uglyfeed.xml'
   os.chdir(uglyfeeds_dir)
   ```

**2. UglyFeedHandler Class**:
   Custom handler to serve the `uglyfeed.xml` file at the root URL.
   ```python
   class UglyFeedHandler(http.server.SimpleHTTPRequestHandler):
       def do_GET(self):
           if self.path == '/':
               self.path = f'/{uglyfeed_file}'
           return super().do_GET()
   ```

**3. get_local_ip() Function**:
   Function to determine the local IP address for serving the file.
   ```python
   def get_local_ip():
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       try:
           s.connect(('10.254.254.254', 1))
           local_ip = s.getsockname()[0]
       except Exception:
           local_ip = '127.0.0.1'
       finally:
           s.close()
       return local_ip
   ```

**4. run() Function**:
   Sets up the server and starts serving the `uglyfeed.xml` file.
   ```python
   def run(server_class=http.server.HTTPServer, handler_class=UglyFeedHandler, port=8000):
       server_address = ('', port)
       httpd = server_class(server_address, handler_class)
       local_ip = get_local_ip()
       final_url = urljoin(f'http://{local_ip}:{port}/', uglyfeed_file)
       print(f'Serving {uglyfeed_file} at: {final_url}')
       httpd.serve_forever()
   ```

**5. Script Execution**:
   Runs the server when the script is executed directly.
   ```python
   if __name__ == '__main__':
       run()
   ```

This script provides a simple and effective way to serve an RSS feed file locally, making it easily accessible for testing or local use.

## evaluate_against_reference.py

### Overview
This Python script evaluates rewritten JSON files against their original versions using various metrics to determine the quality of the rewritten content. It calculates multiple text similarity and readability metrics, normalizes the scores, and aggregates them into a final evaluation score.

### Installation
To set up this script in your environment, follow these steps:

1. **Ensure Python 3 is installed** on your system.

2. **Install necessary Python packages**:
   This script relies on several Python libraries. Install them using:
   ```bash
   pip install nltk textstat spacy scikit-learn textblob pandas
   python -m spacy download en_core_web_sm
   ```

3. **Ensure NLTK resources are downloaded**:
   The script will download necessary NLTK resources if they are not already available.

4. **Set up the directory structure**:
   Ensure you have `output` and `rewritten` directories containing the respective JSON files.

### Usage
To run the script, simply execute it using Python:
```bash
python evaluate_against_reference.py
```

### Functionality
The script includes the following key functions:

- **normalize_for_aggregated_score**: Normalizes the scores for different metrics to a common scale.
- **compare_json_files**: Compares two JSON files using various similarity and readability metrics.
- **save_individual_metrics**: Saves the individual metric results for each comparison.
- **calculate_bleu**: Calculates the BLEU score.
- **custom_sentence_bleu**: Custom implementation of sentence-level BLEU score.
- **flatten_json**: Flattens nested JSON objects.
- **jaccard_similarity**: Calculates the Jaccard similarity between two lists.
- **rouge_l_similarity**: Calculates the ROUGE-L similarity.
- **tfidf_cosine_similarity**: Calculates TF-IDF cosine similarity.
- **calculate_meteor**: Calculates the METEOR score.
- **calculate_edit_distance**: Calculates the edit distance.
- **bow_cosine_similarity**: Calculates Bag-of-Words cosine similarity.
- **calculate_wer**: Calculates Word Error Rate (WER).
- **calculate_cider**: Calculates the CIDEr score.
- **hamming_distance**: Calculates the Hamming distance.
- **f1_score**: Calculates the F1 score.
- **overlap_coefficient**: Calculates the overlap coefficient.
- **dice_coefficient**: Calculates the Dice coefficient.
- **longest_common_subsequence**: Calculates the longest common subsequence.
- **levenshtein_distance**: Calculates the Levenshtein distance.
- **readability_score**: Calculates the readability score.
- **smog_index**: Calculates the SMOG index.
- **ari_score**: Calculates the Automated Readability Index (ARI) score.
- **nist_score**: Calculates the NIST score.
- **lsa_similarity**: Calculates Latent Semantic Analysis (LSA) similarity.
- **sentiment_analysis**: Performs sentiment analysis.
- **lexical_density**: Calculates lexical density.
- **gunning_fog_index**: Calculates the Gunning Fog index.
- **coleman_liau_index**: Calculates the Coleman-Liau index.
- **automated_readability_index**: Calculates the Automated Readability Index.
- **save_results_to_json**: Saves the evaluation results to a JSON file.
- **save_results_to_html**: Saves the evaluation results to an HTML file.

### Input/Output
**Input**:
- JSON files located in the `output` and `rewritten` directories. Each pair of files should have matching names, with the rewritten files suffixed by `_rewritten.json`.

**Output**:
- A JSON file (`evaluation_results.json`) containing the evaluation results.
- An HTML file (`evaluation_results.html`) containing a formatted view of the evaluation results.

### Code Structure
The script is structured as follows:

1. **Imports and Setup**:
   ```python
   import json
   import os
   import difflib
   import nltk
   from nltk.tokenize import word_tokenize
   from nltk.translate.meteor_score import meteor_score
   from collections import Counter
   from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
   from sklearn.metrics.pairwise import cosine_similarity
   import pandas as pd
   import math
   from functools import reduce
   from sklearn.decomposition import TruncatedSVD
   from textblob import TextBlob
   import textstat
   import spacy

   # Ensure nltk resources are downloaded
   nltk.download("punkt", quiet=True)
   nltk.download("wordnet", quiet=True)
   nltk.download("omw-1.4", quiet=True)

   # Load spacy model
   nlp = spacy.load("en_core_web_sm")

   output_folder = "output"
   rewritten_folder = "rewritten"
   results_json_path = "reports/evaluation_results.json"
   results_html_path = "reports/evaluation_results.html"
   ```

2. **Normalization Function**:
   ```python
   def normalize_for_aggregated_score(scores, reference):
       # Normalize scores for aggregated scoring
       # ... (implementation details)
   ```

3. **Comparison Function**:
   ```python
   def compare_json_files(output_file, rewritten_file):
       # Compare two JSON files using various metrics
       # ... (implementation details)
   ```

4. **Save Individual Metrics**:
   ```python
   def save_individual_metrics(output_file, metrics):
       # Save individual metric results for each comparison
       # ... (implementation details)
   ```

5. **Metric Calculation Functions**:
   Implement various text similarity and readability metrics.
   ```python
   def calculate_bleu(reference, candidate, n=4, smoothing=None):
       # Calculate BLEU score
       # ... (implementation details)

   def custom_sentence_bleu(references, hypothesis):
       # Custom implementation of sentence-level BLEU score
       # ... (implementation details)

   # Other metric calculation functions...
   ```

6. **Helper Functions**:
   Implement various helper functions used in metric calculations.
   ```python
   def flatten_json(data, prefix=""):
       # Flatten nested JSON objects
       # ... (implementation details)

   def jaccard_similarity(list1, list2):
       # Calculate Jaccard similarity
       # ... (implementation details)

   # Other helper functions...
   ```

7. **Save Results Functions**:
   Functions to save results to JSON and HTML files.
   ```python
   def save_results_to_json(results, path):
       # Save evaluation results to JSON
       # ... (implementation details)

   def save_results_to_html(results, path):
       # Save evaluation results to HTML
       # ... (implementation details)
   ```

8. **Main Evaluation Loop**:
   Evaluate all rewritten files against their original versions.
   ```python
   rewritten_files = [f for f in os.listdir(rewritten_folder) if f.endswith("_rewritten.json")]

   all_results = []
   for rewritten_file in rewritten_files:
       rewritten_path = os.path.join(rewritten_folder, rewritten_file)

       output_file = rewritten_file.replace("_rewritten.json", ".json")
       output_path = os.path.join(output_folder, output_file)

       if os.path.isfile(output_path):
           print("\nEvaluating:", output_file)
           result = compare_json_files(output_path, rewritten_path)
           if result:
               all_results.append(result)
               save_individual_metrics(rewritten_file, result)
       else:
           print(f"WARNING: No corresponding file found in 'output' for {rewritten_file}")

   save_results_to_json(all_results, results_json_path)
   save_results_to_html(all_results, results_html_path)

   print(f"Results saved to {results_json_path} and {results_html_path}")
   ```

This script provides a comprehensive evaluation of rewritten news articles against their original versions, offering insights into the quality and coherence of the rewritten content.


## evaluate_cohesion_concreteness.py

This Python script evaluates the cohesion and information density metrics of a text extracted from a JSON file. It uses several libraries, including `json`, `nltk`, `langdetect`, and `spacy`. Here is an explanation of each section of the code:

### Imports and Setup
```python
import json
import nltk
import sys
from langdetect import detect
import spacy
from collections import Counter
```
- **json**: To handle JSON files.
- **nltk**: For natural language processing tasks such as tokenization.
- **sys**: To handle command-line arguments.
- **langdetect**: To detect the language of the input text.
- **spacy**: For advanced NLP tasks using pre-trained models.
- **Counter**: To count token occurrences.

### Download NLTK Resources
```python
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
```
- Downloads the necessary NLTK resources for tokenization and stop words.

### Load spaCy Models
```python
nlp_en = spacy.load("en_core_web_sm")
nlp_it = spacy.load("it_core_news_sm")
```
- Loads spaCy models for English and Italian.

### Define Language Detection and Model Selection Functions
```python
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian
```
- Detects the language of the text using `langdetect`. Defaults to Italian if detection fails.

```python
def get_spacy_model(lang):
    if lang == 'en':
        return nlp_en
    else:
        return nlp_it
```
- Returns the appropriate spaCy model based on the detected language.

### Placeholder Function for Coh-Metrix Scores
```python
def calculate_coh_metrix_scores(text):
    return 0.5
```
- A placeholder function for Coh-Metrix Scores. It returns a dummy score of 0.5.

### Define Metric Calculation Functions
```python
def calculate_cohesion_score(text):
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return 0
    overlaps = 0
    for i in range(len(sentences) - 1):
        tokens1 = set(nltk.word_tokenize(sentences[i].lower()))
        tokens2 = set(nltk.word_tokenize(sentences[i+1].lower()))
        overlaps += len(tokens1.intersection(tokens2))
    return overlaps / (len(sentences) - 1)
```
- Calculates the cohesion score by analyzing overlapping tokens between consecutive sentences.

```python
def calculate_cohesive_harmony_index(text, nlp):
    doc = nlp(text)
    harmony_score = 0
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('nsubj', 'dobj', 'iobj', 'pobj'):
                harmony_score += 1
    return harmony_score / len(list(doc.sents)) if len(list(doc.sents)) > 0 else 0
```
- Calculates the cohesive harmony index by counting the occurrences of specific syntactic dependencies.

```python
def calculate_referential_density(text, nlp):
    doc = nlp(text)
    referential_count = sum(1 for token in doc if token.pos_ in ('NOUN', 'PRON'))
    return referential_count / len(doc) if len(doc) > 0 else 0
```
- Calculates referential density based on the occurrence of nouns and pronouns.

```python
def calculate_information_density(text):
    words = nltk.word_tokenize(text)
    unique_words = set(words)
    return len(unique_words) / len(words) if len(words) > 0 else 0
```
- Calculates information density as the ratio of unique words to total words.

### Evaluation Function
```python
def evaluate_cohesion_information_density_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Coh-Metrix Scores": calculate_coh_metrix_scores(text),
        "Cohesion Score": calculate_cohesion_score(text),
        "Cohesive Harmony Index": calculate_cohesive_harmony_index(text, nlp),
        "Referential Density": calculate_referential_density(text, nlp),
        "Information Density": calculate_information_density(text)
    }

    max_values = {
        "Coh-Metrix Scores": 1,
        "Cohesion Score": 1,
        "Cohesive Harmony Index": 1,
        "Referential Density": 1,
        "Information Density": 1
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    weights = {
        "Coh-Metrix Scores": 0.2,
        "Cohesion Score": 0.2,
        "Cohesive Harmony Index": 0.2,
        "Referential Density": 0.2,
        "Information Density": 0.2
    }

    aggregated_score = sum(normalized_metrics[metric] * weights[metric] for metric in normalized_metrics) * 100
    
    return metrics, normalized_metrics, aggregated_score
```
- Evaluates the cohesion and information density metrics, normalizes them, and calculates an aggregated score.

### Main Function and Execution
```python
def main(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            text = data.get("content", "")

        if not text:
            print("No content found in the provided JSON file.")
            return

        lang = detect_language(text)
        metrics, normalized_metrics, aggregated_score = evaluate_cohesion_information_density_metrics(text, lang)

        output = {
            "Cohesion Information Density Metrics": metrics,
            "Aggregated Cohesion Information Density Score": aggregated_score
        }

        print("Text Cohesion and Information Density Metrics:")
        for metric, score in metrics.items():
            print(f"{metric}: {score:.4f}")
        print("\nNormalized Metrics:")
        for metric, score in normalized_metrics.items():
            print(f"{metric}: {score:.4f}")
        print(f"\nAggregated Cohesion and Information Density Score: {aggregated_score:.4f}")

        output_file_path = file_path.replace(".json", "_metrics_cohesion_information_density.json")
        with open(output_file_path, 'w') as out_file:
            json.dump(output, out_file, indent=4)
        print(f"Metrics exported to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The provided file is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_cohesion_information_density_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
```
- Reads the input JSON file, extracts the text, detects its language, calculates various metrics, normalizes them, and prints/export the results.
