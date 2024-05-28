# UglyFeed

UglyFeed is a **simple** Python application designed to **retrieve**, **aggregate**, **filter**, **rewrite**, **evaluate** and **serve** content (RSS feeds) written by a large language model. This repository provides the code and necessary files to run the application.

![UglyFeed](https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/docs/UglyFeed.png)


## Features

- 📡 Retrieve RSS feeds
- 🧮 Aggregate feeds based on similarity
- 🤖 Rewrite aggregated feeds using a language model
- 📈 Evaluate generated content
- 💾 Save rewritten feeds to JSON files
- 🔁 Convert JSON to valid RSS feed
- 🌐 Serve XML feed via HTTP server

**Requirements**

- You need python and an Internet connection 
- To retrieve the final RSS XML feed I use [FluentReader](https://github.com/yang991178/fluent-reader) on OSX and [NetNewsWire](https://netnewswire.com/) on mobile but [any RSS reader](https://github.com/topics/rss-reader) will work!

**Supported API and models**

- OpenAI API (`gpt-3.5-turbo`, `gpt4`, `gpt4o`)
- Ollama API (all models like `llama3` or `phi3`)
  
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fabriziosalmi/UglyFeed.git
    cd UglyFeed
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
Optional: 
Properly setup a custom system prompt on your LLM inference server.
   
## Usage

1. Setup options (similarity options, API, model, content_prefix, max_items and max_age_days) by making your changes into the `config.yaml` file

2. Retrieve and aggregate RSS feeds (you can change feeds in the `input/feeds.txt` file)
    ```sh
    python main.py
    ```

   Optional: You can extract RSS urls from local or remote OPML file by running `python opml2feeds.py source OPML_file_or_URL` (check code, barely tested)

3. Rewrite and save aggregated feeds using configured LLM API:

    ```sh
    python llm_processor.py
    ```
   
    Optional: You can change prompt/role, just look into the **prompts** folder. By using specific prompts You can force specific languages to use for generation.
   
4. Convert JSON to RSS feed
    ```sh
    python json2rss.py
    ```
    
5. Serve RSS XML via HTTP server
    ```sh
    python serve.py
    ```

Optional:
- 📈 Evaluate generated content against several [metrics](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/metrics.md) (an aggregated score is provided too) by running `python evaluate_against_reference.py` (evaluate comparison metrics of generated files against the reference files) and `process_multiple_metrics.py` (evaluate only the generated content files against different metrics).
- 🎛️ You can easily customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md).
- 🕒 You can setup a cronjob to have fresh content automatically updated on your RSS reader by executing all files in the order specified (an automation script is under development)
- 🌎 You can reach your local generated feed securely via Internet by using solutions like ngrok, cloudflared, wireguard, tailscale and so on.
- 🎛️ You can create RSS from any content by using RSSHub and rewrite its feeds by using UglyFeed.

## Project Structure

Main components:

- `requirements.txt`: List of dependencies.
- `config.yaml`: Configuration options for the application
- `main.py`: Retrieves and aggregates RSS feeds.
  - `json_manager.py`: Used by main.py, manages JSON file operations. 
  - `rss_reader.py`: Used by main.py, reads RSS feeds.
  - `similarity_checker.py`: Used by main.py, checks similarity between feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model LLM APIs.
- `json2rss.py`: Convert JSON to RSS feed.
- `serve.py`: Serve RSS XML via HTTP server.
  - `uglyfeeds/`: Used by serve.py is the directory where the uglyfeed.xml is served via HTTP

Optional components:

- `process_multiple_metrics.py`: Evaluate metrics of generated content.
- `evaluate_against_reference.py`: Evaluate metrics of generated content against reference content.

Directories:

- `input`: Directory for feeds list file
- `output`: Directory for aggregated (for similarity) feeds.
- `rewritten`: Directory for rewritten content and evaluation metrics.
- `reports`: Directory for metrics export in JSON and HTML
  
## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

**Disclaimer**

> _It is crucial to acknowledge the potential misuse of AI language models by this tool. The use of adversarial prompts and models can easily lead to the creation of misleading content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## License

This project is licensed under the MIT License.
