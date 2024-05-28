# main.py

## Introduction
This script processes RSS feeds, groups similar articles based on a similarity threshold, and saves the grouped articles into JSON files. It is designed to read configuration settings from a YAML file, fetch RSS feeds, and perform similarity checks on the articles.

## Input/Output

### Input
- **Configuration File**: `config.yaml` containing settings for similarity threshold and options.
- **RSS Feeds File**: `input/feeds.txt` containing a list of RSS feed URLs.

### Output
- **Grouped Articles**: JSON files saved in the `output` directory, each containing a group of similar articles.

## Functionality

### Features
1. **Configuration Loading**: Loads settings from a YAML configuration file.
2. **RSS Feeds Fetching**: Fetches and parses articles from RSS feeds listed in a text file.
3. **Article Grouping**: Groups articles based on similarity using a defined threshold.
4. **JSON Saving**: Saves the grouped articles into separate JSON files.

## Code Structure

### Imports
```python
import os
import argparse
import time
import yaml
from rss_reader import fetch_feeds_from_file
from similarity_checker import group_similar_articles
from json_manager import save_grouped_articles
```
- **os**: For file and directory operations.
- **argparse**: For parsing command-line arguments.
- **time**: For measuring execution time.
- **yaml**: For reading YAML configuration files.
- **rss_reader**: For fetching and parsing RSS feeds.
- **similarity_checker**: For grouping similar articles.
- **json_manager**: For saving grouped articles into JSON files.

### Configuration Loading
```python
def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
```
Loads configuration settings from the specified YAML file.

### Main Function
```python
def main(config: dict) -> None:
    """Main function to process RSS feeds and group similar articles."""
    print("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    start_time = time.time()

    print("Fetching and parsing RSS feeds...")
    articles = fetch_feeds_from_file(input_file_path)
    print(f"Total articles fetched and parsed: {len(articles)}")

    similarity_threshold = config['similarity_threshold']
    similarity_options = config['similarity_options']

    print(f"Grouping articles based on similarity (threshold={similarity_threshold})...")
    grouped_articles = group_similar_articles(articles, similarity_threshold, similarity_options)
    print(f"Total groups formed: {len(grouped_articles)}")

    print("Saving grouped articles to JSON files...")
    group_sizes = save_grouped_articles(grouped_articles, 'output')
    total_files_saved = len(group_sizes)

    elapsed_time = time.time() - start_time
    print(f"RSS feed processing complete. {total_files_saved} different articles are now grouped.")
    print(f"Details of groups saved: {group_sizes}")
    print(f"(Took {elapsed_time:.2f} seconds)")

    # Additional output to summarize file generation
    print("Summarizing output files:")
    output_files = os.listdir('output')
    for filename in output_files:
        path = os.path.join('output', filename)
        with open(path, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
        print(f"{filename}: {line_count} lines")
    print(f"Total output files: {len(output_files)}")
```
Processes the RSS feeds, groups similar articles, and saves the grouped articles into JSON files. It also prints summary information about the processed articles and generated files.

### Command-Line Interface
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process RSS feeds and group similar articles based on a similarity threshold.'
    )
    parser.add_argument(
        '-c', '--config', type=str, default='config.yaml',
        help='Path to the configuration file (default: config.yaml).'
    )
    args = parser.parse_args()
    config = load_config(args.config)
    main(config)
```
- **argparse**: Parses command-line arguments to get the path to the configuration file.
- **load_config**: Loads the configuration from the specified file.
- **main**: Calls the main function to process the RSS feeds.

## Usage Example
1. Create a `config.yaml` file with the following content:
    ```yaml
    similarity_threshold: 0.8
    similarity_options:
        method: "cosine"
        vectorizer: "tfidf"
    ```
2. Create an `input/feeds.txt` file with a list of RSS feed URLs.
3. Run the script:
    ```bash
    python main.py --config config.yaml
    ```
4. The grouped articles will be saved as JSON files in the `output` directory.
