# UglyFeed

_NEWS_
> - released: openai api added (llm_processor_openai.py), just run it instead of llm_processor.py
> - ongoing: dockerizing the application, overall improvements (docs, comments)

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
Optional: 
Properly setup a custom system prompt on your LLM inference server.
   
## Usage

1. Retrieve and aggregate RSS feeds (you can change feeds in the input/feeds.txt file)
    ```sh
    python main.py
    ```
   
2. Rewrite and save aggregated feeds using supported LLM API:

 - Ollama API
    ```sh
    python llm_processor.py
    ```
 - OpenAI API
    ```sh
    python llm_processor_openai.py
    ```
    
3. Convert JSON to RSS feed
    ```sh
    python json2rss.py
    ```
    
4. Serve RSS XML via HTTP server
    ```sh
    python serve.py
    ```

Optional:
📈 Evaluate generated content against BLEU-1, Jaccard Similarity, ROUGE-L, TF-IDF Cosine Similarity scores (an additional weighted aggregated score is provided too)
    ```
    python evaluate.py
    ```

| Output File | Model | BLEU-1 | Jaccard Similarity | ROUGE-L | TF-IDF Cosine Similarity | METEOR | Edit Distance | BoW Cosine Similarity | Aggregated Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| content1 | gpt-3.5-turbo | 0.600000 | 0.375000 | 0.181818 | 0.660978 | 0.389535 | 0.545455 | 0.763283 | **0.374743** |
|          | llama3 | 0.600000 | 0.375000 | 0.181818 | 0.392030 | 0.303253 | 0.545455 | 0.503019 | 0.313194 |
|          | Phi3 | 0.600000 | 0.375000 | 0.181818 | 0.599097 | 0.337187 | 0.545455 | 0.707138 | 0.357706 |
| content2 | gpt-3.5-turbo | 0.666667 | 0.444444 | 0.133333 | 0.526300 | 0.374514 | 0.533333 | 0.618528 | **0.354601** |
|          | llama3 | 0.666667 | 0.444444 | 0.133333 | 0.339200 | 0.241708 | 0.533333 | 0.433891 | 0.304147 |
|          | Phi3 | 0.666667 | 0.444444 | 0.133333 | 0.518680 | 0.320975 | 0.533333 | 0.606571 | 0.347289 |
| content3 | gpt-3.5-turbo | 0.666667 | 0.363636 | 0.133333 | 0.666370 | 0.482562 | 0.533333 | 0.760096 | **0.383873** |
|          | llama3 | 0.666667 | 0.363636 | 0.133333 | 0.640099 | 0.436270 | 0.533333 | 0.719034 | 0.372510 |
|          | Phi3 | 0.666667 | 0.363636 | 0.133333 | 0.552954 | 0.363119 | 0.533333 | 0.658565 | 0.350433 |
| content4 | gpt-3.5-turbo | 0.600000 | 0.375000 | 0.181818 | 0.373337 | 0.310227 | 0.545455 | 0.521980 | **0.313918** |
|          | llama3 | 0.600000 | 0.375000 | 0.181818 | 0.199557 | 0.233573 | 0.545455 | 0.300208 | 0.266698 |
|          | Phi3 | 0.600000 | 0.375000 | 0.181818 | 0.266569 | 0.258863 | 0.545455 | 0.391706 | 0.285077 |
| content5 | gpt-3.5-turbo | 0.600000 | 0.375000 | 0.181818 | 0.523415 | 0.437073 | 0.545455 | 0.628784 | 0.352291 |
|          | llama3 | 0.600000 | 0.375000 | 0.181818 | 0.522185 | 0.480200 | 0.545455 | 0.623483 | **0.355950** |
|          | Phi3 | 0.600000 | 0.375000 | 0.181818 | 0.468521 | 0.457982 | 0.545455 | 0.570876 | 0.343102 |
| content6 | gpt-3.5-turbo | 0.666667 | 0.444444 | 0.133333 | 0.452761 | 0.254774 | 0.533333 | 0.606382 | **0.334058** |
|          | llama3 | 0.666667 | 0.444444 | 0.133333 | 0.230188 | 0.257172 | 0.533333 | 0.337770 | 0.285180 |
|          | Phi3 | 0.666667 | 0.444444 | 0.133333 | 0.401519 | 0.284667 | 0.533333 | 0.550536 | 0.326339 |
| content7 | gpt-3.5-turbo | 0.600000 | 0.375000 | 0.181818 | 0.737304 | 0.405061 | 0.545455 | 0.809709 | **0.388571** |
|          | llama3 | 0.600000 | 0.375000 | 0.181818 | 0.538091 | 0.292103 | 0.545455 | 0.646695 | 0.341053 |
|          | Phi3 | 0.600000 | 0.375000 | 0.181818 | 0.444893 | 0.290764 | 0.545455 | 0.558493 | 0.322779 |
| content8 | gpt-3.5-turbo | 0.666667 | 0.363636 | 0.133333 | 0.592662 | 0.306119 | 0.533333 | 0.701155 | 0.352963 |
|          | llama3 | 0.666667 | 0.363636 | 0.133333 | 0.784819 | 0.464478 | 0.533333 | 0.850826 | **0.402982** |
|          | Phi3 | 0.666667 | 0.363636 | 0.133333 | 0.559636 | 0.289311 | 0.533333 | 0.679572 | 0.345822 |

Note: llama3 (8b) and phi3 models are the ones provided by Ollama.

- 🎛️ You can customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
  
## Project Structure

- `main.py`: Retrieves and aggregates RSS feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model and Ollama API.
- `llm_processor_openai.py`: Rewrites aggregated feeds using a language model and OpenAI API.
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
