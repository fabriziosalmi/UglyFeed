# Scripts documentation
Welcome to the Scripts Documentation section. This comprehensive guide provides detailed information and instructions for each script in our project. I use to complete the docs also to catch some placeholder functions around the code and replace it with usable stuff :)
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

## List of scripts (ongoing.. back here soon for updates ^_^)

- [demo.sh](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#demosh)
- [json2rss.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#json2rsspy)
- [evaluate_cohesion_concreteness.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/scripts.md#evaluate_cohesion_concretenesspy)

---

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
