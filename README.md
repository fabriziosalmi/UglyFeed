# UglyCitizen

UglyCitizen is a Python application designed to retrieve, aggregate, and rewrite news feeds using a large language model. This repository provides the code and necessary files to run the application.

In my own setup I use:

- a mac laptop to test/run the repository scripts and retrieve the final RSS XML feed via [FluentReader](https://github.com/yang991178/fluent-reader)
- a linux LLM inference server running [llama3](https://ollama.com/library/llama3) (I use Ollama but I can test it on LMStudio and I'll provide feedback)

## Features

- Retrieve RSS feeds
- Aggregate feeds based on similarity
- Rewrite aggregated feeds using a language model
- Save rewritten feeds to JSON files
- Convert JSON to valid RSS feed
- Serve XML feed via HTTP server

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

1. Retrieve and aggregate RSS feeds (you can change feeds in the input/feeds.txt file)
    ```sh
    python main.py
    ```

2. Rewrite and save aggregated feeds (I have Ollama and llama3 running at http://192.168.100.41:11434, You can change it to fit your needs):
    ```sh
    python llm_processor.py
    ```
    
3. Convert JSON to RSS feed
    ```sh
    python json2rss.py
    ```
    
4. Serve RSS XML via HTTP server
    ```sh
    python serve.py
    ```

Expected output:

```
python serve.py
Serving uglyfeed.xml at: http://192.168.100.6:8000/uglyfeed.xml
```

## Project Structure

- `main.py`: Retrieves and aggregates RSS feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model.
- `json_manager.py`: Manages JSON file operations.
- `rss_reader.py`: Reads RSS feeds.
- `similarity_checker.py`: Checks similarity between feeds.
- `json2rss.py`: Convert JSON to RSS feed
- `serve.py`: Serve RSS XML via HTTP server
- `input/`: Directory for input files (if any).
- `requirements.txt`: List of dependencies.

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
