# UglyCitizen

UglyCitizen is a Python application designed to retrieve, aggregate, and rewrite news feeds using a language model. This repository provides the code and necessary files to run the application.

## Features

- Retrieve RSS feeds
- Aggregate feeds based on similarity
- Rewrite aggregated feeds using a language model
- Save rewritten feeds to JSON files

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fabriziosalmi/uglycitizen.git
    cd uglycitizen
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Retrieve and aggregate RSS feeds:
    ```sh
    python main.py
    ```

2. Rewrite and save aggregated feeds:
    ```sh
    python llm_processor.py
    ```

## Project Structure

- `main.py`: Retrieves and aggregates RSS feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model.
- `json_manager.py`: Manages JSON file operations.
- `rss_reader.py`: Reads RSS feeds.
- `similarity_checker.py`: Checks similarity between feeds.
- `input/`: Directory for input files (if any).
- `requirements.txt`: List of dependencies.

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
