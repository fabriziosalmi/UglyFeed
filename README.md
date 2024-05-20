# UglyFeed

UglyFeed is a **simple** Python application designed to retrieve, aggregate, evaluate and rewrite news feeds using a large language model. This repository provides the code and necessary files to run the application.

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
    ```
    python evaluate.py
    ```
📈 Evaluate generated content against 25 metrics (an aggregated score is provided too).

I compared the performance of five state-of-the-art language models: GPT-4 OpenAI (GPT-4O), GPT-4, GPT-3.5, LLaMA3, and Phi3. The models were assessed on various natural language processing metrics across multiple files, providing a detailed analysis of their capabilities. Below is a summary of the results:

**Overview of Metrics**

The models were evaluated using the following metrics:
- BLEU-1
- Jaccard Similarity
- ROUGE-L
- TF-IDF Cosine Similarity
- METEOR
- Edit Distance
- BoW Cosine Similarity
- WER (Word Error Rate)
- CIDEr
- Hamming Distance
- F1 Score
- Overlap Coefficient
- Dice Coefficient
- Longest Common Subsequence
- Levenshtein Distance
- Average Token Length
- Type-Token Ratio
- Gunning Fog Index
- Automated Readability Index
- Lexical Diversity
- Syntactic Complexity
- Perplexity
- Readability Consensus
- Entropy
- Subjectivity Score
- Aggregated Score

### Aggregated Scores by Model and File
The table below shows the aggregated scores for each model across the evaluated files. The Q in the JSON filenames is the number of how many different source are included in the file, the S is the similarity score of the group of the aggregated sources in the file.

| Output File                                    | GPT-4O | GPT-4 | GPT-3.5 | LLaMA3 | Phi3  |
|------------------------------------------------|--------|-------|---------|--------|-------|
| 001-Q6-S0.35.json               | **27.7113** | 27.1664| 26.5937 | 26.5008| 25.5447|
| 002-Q3-S0.75.json               | 16.8161| 16.5364| 16.4435 | **16.8195** | 16.1289|
| 003-Q3-S0.56.json               | **16.5291** | 16.4713| 16.3715 | 16.2184| 16.2428|
| 004-Q4-S0.86.json               | **12.7142** | 12.2148| 11.9950 | 12.1501| 12.1181|
| 005-Q2-S0.74.json               | **16.1847** | 15.9528| 15.7940 | 15.8327| 15.9673|
| 006-Q5-S0.43.json               | 17.8144| 17.4919| 17.5431 | 17.8104| **20.4773** |
| 007-Q3-S0.51.json               | **16.8200** | 16.0705| 16.5045 | 16.2676| 15.9761|
| 008-Q3-S0.45.json               | 14.2836| 14.3113| 14.3091 | 15.3453| **15.9081** |

Optional: 
🎛️ You can customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
  
## Project Structure

- `main.py`: Retrieves and aggregates RSS feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model and Ollama API.
- `llm_processor_openai.py`: Rewrites aggregated feeds using a language model and OpenAI API.
- `json_manager.py`: Manages JSON file operations.
- `rss_reader.py`: Reads RSS feeds.
- `similarity_checker.py`: Checks similarity between feeds.
- `json2rss.py`: Convert JSON to RSS feed
- `evaluate.py`: Evaluate generated content against 25 metrics
- `proxy.py`: Serve HTTP proxy on port 8028 to transparently handle Ollama API to OpenAI API communications (initial workaround, use llm_processor_openai.py instead)
- `serve.py`: Serve RSS XML via HTTP server
- `input/`: Directory for input files (if any).
- `requirements.txt`: List of dependencies.

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
