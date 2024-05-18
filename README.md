# UglyFeed

UglyFeed is a **simple** Python application designed to retrieve, aggregate, and rewrite news feeds using a large language model. This repository provides the code and necessary files to run the application.

Supported setup:

- You need python and an Internet connection to test/run the repository scripts and to retrieve the final RSS XML feed via [FluentReader](https://github.com/yang991178/fluent-reader) or any other RSS reader
- [Ollama](https://ollama.com/download) or any OpenAI API compatible LLM inference server (you need to run proxy.py in that case) running [llama3](https://ollama.com/library/llama3) (better) or [phi3](https://ollama.com/library/phi3) (faster)


> _It is crucial to acknowledge the potential misuse of this tool. The use of adversarial prompts and models can easily lead to the creation of spam, fake news, and other malicious content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## Features

- 📡 Retrieve RSS feeds
- 🧮 Aggregate feeds based on similarity
- 🤖 Rewrite aggregated feeds using a language model
- 📈 Automatically evaluate generated content
- 💾 Save rewritten feeds to JSON files
- 🔁 Convert JSON to valid RSS feed
- 🌐 Serve XML feed via HTTP server

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
3. ⚠️ Optional: properly setup a custom system prompt on your LLM inference server.
   
## Usage

1. Retrieve and aggregate RSS feeds (you can change feeds in the input/feeds.txt file)
    ```sh
    python main.py
    ```

2. ⚠️ Optional: run proxy.py if you have OpenAI API compatbile server and change API port to 8028 in llm_processor.py
   
3. Rewrite and save aggregated feeds (I have Ollama and llama3 or phi3 running at http://localhost:11434, You can change it to fit your needs):
    ```sh
    python llm_processor.py
    ```
    
4. Convert JSON to RSS feed
    ```sh
    python json2rss.py
    ```
    
5. Serve RSS XML via HTTP server
    ```sh
    python serve.py
    ```

6. Evaluate generated content against BLEU-1, Jaccard Similarity, ROUGE-L, TF-IDF Cosine Similarity scores (an additional weighted aggregated score is provided too)
    ```sh
    python evaluate.py
    ```
    
7. Optional

- 🎛️ You can customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
  
## Project Structure

- `main.py`: Retrieves and aggregates RSS feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model.
- `json_manager.py`: Manages JSON file operations.
- `rss_reader.py`: Reads RSS feeds.
- `similarity_checker.py`: Checks similarity between feeds.
- `json2rss.py`: Convert JSON to RSS feed
- `evaluate.py`: Evaluate generated content against BLEU-1, Jaccard Similarity, ROUGE-L, TF-IDF Cosine Similarity
- `proxy.py`: Serve HTTP proxy on port 8028 to transparently handle Ollama API to OpenAI API communications
- `serve.py`: Serve RSS XML via HTTP server
- `input/`: Directory for input files (if any).
- `requirements.txt`: List of dependencies.

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
