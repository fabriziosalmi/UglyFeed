# UglyFeed



UglyFeed is a **simple** Python application designed to **retrieve**, **aggregate**, **filter**, **rewrite**, **evaluate** and **serve** content (RSS feeds) written by a large language model. This repository provides the code, the [docs](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md) and the necessary files to run the application.

<p align="center">
  <img src="https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/docs/UglyFeed.png" alt="UglyFeed">
</p>

## Features

- 📡 Retrieve RSS feeds
- 🧮 Aggregate feeds based on similarity
- 🤖 Rewrite aggregated feeds using a language model
- 💾 Save rewritten feeds to JSON files
- 🔁 Convert JSON to valid RSS feed
- 🌐 Serve XML feed via HTTP server
- 📈 Evaluate generated content

**Requirements**
- 🐍 Python
- 🌎 Internet connection
- 📰 [an RSS reader](https://github.com/topics/rss-reader)

To retrieve the final feed I use [FluentReader](https://github.com/yang991178/fluent-reader) on laptop and [NetNewsWire](https://netnewswire.com/) on mobile.

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


## Configuration

1. Setup options by making your changes into the `config.yaml` file

2. Modify the `input/feeds.txt` file with your feeds urls

## Usage

1. Retrieve and aggregate RSS feeds
    ```sh
    python main.py
    ```
    
2. Rewrite and save aggregated feeds using configured LLM API:

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

## Tuning

**Tune it for your own needs**
- 🎛️ Customize user prompt, check the [prompts](https://github.com/fabriziosalmi/UglyFeed/tree/main/prompts) folder for inspiration. You can also check the [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts)
- 🎛️ Force specific languages to use for generation just by using specific prompts
- 📈 Evaluate generated content against several [metrics](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/metrics.md) (an aggregated score is provided too) by running `python evaluate_against_reference.py` to evaluate comparison metrics of generated files against the reference files or `python process_multiple_metrics.py` to evaluate only the generated content files against different metrics
- 🕒 Setup a cronjob to have fresh content automatically updated on your RSS reader by executing all files in the order specified

**Tune it by using 3rd party tools**
- 🔁 Create RSS from any content by using [RSSHub](https://github.com/DIYgod/RSSHub) and rewrite its feeds by using [UglyFeed](https://github.com/fabriziosalmi/UglyFeed)
- 🎛️ Customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- 🌎 You can reach your local generated feed securely via Internet by using solutions like ngrok, cloudflared, wireguard, tailscale and so on

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## Disclaimer

> _It is crucial to acknowledge the potential misuse of AI language models by this tool. The use of adversarial prompts and models can easily lead to the creation of misleading content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## License

This project is licensed under the MIT License.
