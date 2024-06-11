# Project documentation
Welcome to the UglyFeed project documentation section. This guide provides detailed information for the scripts used by the project.

## Quick start
**UglyFeed now can be used via Docker, please check the updated [documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/docker.md).**

## Setup

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fabriziosalmi/UglyFeed.git
    cd UglyFeed
    ```

2. Run the web application:
    ```sh
    streamlit run gui.py --server.address 0.0.0.0
    ```

### Configuration

1. Setup options by making your changes into the Configuration page

**Source Feeds**
- Modify the source feeds list to fit with your preferred RSS feeds (changes will still be saved as `input/feeds.txt` for backward compatibility)

**Similarity options**
For a general use the default values seems to be a good fit to aggressively filter out some noise. To increase items count try to reduce min_samples to 2 and play around eps and similarity.

- `similarity_threshold` (range: 0-1)
- `min_samples` (Minimum number of samples in a cluster for DBSCAN)
- `eps` (Maximum distance between two samples for one to be considered as in the neighborhood of the other in DBSCAN)

**API and LLM options**
You can use OpenAI API or Ollama API, not togheter at the same time. Please comment or delete the unused API to avoid issues.

- `openai_api_url` (OpenAI API endpoint)
- `openai_api_key` (OpenAI API key) [OpenAI models](https://platform.openai.com/docs/models)
- `openai_model` (OpenAI model)
- `groq_api_url` (Groq API endpoint)
- `groq_api_key` (Groq API key)
- `groq_model` (Groq model) [Groq models](https://console.groq.com/docs/models)
- `ollama_api_url` (Ollama API endpoint)
- `ollama_model` (Ollama model) [Ollama models](https://platform.openai.com/docs/models)

**Instructions/role/prompt option**
- `content_prefix` (prompt to be used as instruction for the rewriting process)

**RSS retention options**
- `max_items` (Maximum number of items to process for the rewriting process)
- `max_age_days` (Maximum age of items in days to be considered)

2. Run `main.py` from its dedicated page, it will retrieve and aggregate feeds items based on similarity

3. Run `llm_processor.py` from its dedicated page, it will rewrite feeds based on LLM instruction/prompt and options and it will save a single JSON file for each unique rewritten feeds item.

4. Run `json2rss.py` from its dedicated page, it will create a valid RSS XML file with all rewritten feeds items.

5. Go to the Serve XML feed page to get the generated XML content and a working HTTP URL you can use with any RSS reader as feed source.
