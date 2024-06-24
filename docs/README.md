# Documentation
Welcome to the UglyFeed documentation. This guide provides detailed information on how to run UglyFeed.

- [Installation and Automated Runs](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#%EF%B8%8F-installation-and-automated-runs-github-actions)
- [Installation (Pip)](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#-installation-pip)
- [Installation and run (without Docker)](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#%EF%B8%8F-installation-and-run-without-docker)
- [Installation and Run (Docker)](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#-installation-and-run-docker)
- [Installation and Run (Docker Compose)](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#-installation-and-run-docker-compose)
- [Configuration](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#-configuration)
- [Usage](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#%EF%B8%8F-usage)


## ⚙️ Installation and Automated Runs (GitHub Actions)

You can use the UglyFeed repository as a GitHub action application source, and your own public repository as an XML CDN. A file named `uglyfeed.xml` will be saved to your repository daily. No local installation or execution is required; simply configure the actions to suit your needs. 

- 📙 Additional actions will be added soon for popular setups supporting remote Ollama servers and more setups.
- 🔒 To mask your important vars you can use a private repository and, of course, protect all params by using GitHub Actions secrets only.

Here the current available actions:

**Daily delivery via GitHub Actions**

- [Groq and llama3-8b-8192](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-Groq-llama3-8b-8192.yml)
- [Groq and llama3-70b-8192](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-Groq-llama3-70b-8192.yml)
- [Groq and gemma-7b-it](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-Groq-gemma-7b-it.yml)
- [Groq and mixtral-8x7b-32768](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-Groq-mixtral-8x7b-32768.yml)
- [OpenAI and gpt-3.5-turbo](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-OpenAI-gpt-3.5-turbo.yml)
- [OpenAI and gpt-4](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-OpenAI-gpt-4.yml)
- [OpenAI and gpt-4o](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-OpenAI-gpt-4o.yml)

## 🐍 Installation (pip)

UglyFeed can be installed via `pip` using the `uglypy` package. This integration allows users to incorporate UglyFeed features into existing pipelines easily. 
For more information, visit the [PyPI page for uglypy](https://pypi.org/project/uglypy/).

```bash
pip install uglypy
```

## 🖥️ Installation and Run (Without Docker)

To run the UglyFeed web application without Docker, clone the repository and start the application with Streamlit:

```sh
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
streamlit run gui.py --server.address 0.0.0.0
```
That command will run UglyFeed web UI on all interfaces, if You prefer to make it listen on localhost only go this way:
```
streamlit run gui.py --server.address 127.0.0.1
```

To disable Streamlit telemetry, use the following command:

```sh
streamlit run gui.py --browser.gatherUsageStats false
```

## 🐳 Installation and Run (Docker)

To run the UglyFeed app using Docker, populate the `config.yaml` and `feeds.txt` with your settings, and mount these files in the container:

```bash
docker run -p 8001:8001 -p 8501:8501 -v /path/to/local/feeds.txt:/app/input/feeds.txt -v /path/to/local/config.yaml:/app/config.yaml fabriziosalmi/uglyfeed:latest
```

## 🐳 Installation and Run (Docker Compose)

For an easier setup with Docker Compose, use the following commands:

```bash
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
docker compose up -d
```

The stack defined in the `docker-compose.yaml` file has been successfully tested on Portainer 🎉.

## 📝 Configuration

You can customize UglyFeed's behavior by modifying the configuration files or using the web application's **Configuration** page.

### Configuration Files

- **`feeds.txt`**: Specify the source feeds.
- **`config.yaml`**: Modify settings such as preprocessing, vectorization, similarity options, and API configurations.

### Configuration Options

#### Pre-processing

Control the steps to preprocess text before feeding it into the system:

- `remove_html` (default: `true`): Remove HTML tags from the text.
- `lowercase` (default: `true`): Convert text to lowercase.
- `remove_punctuation` (default: `true`): Remove punctuation.
- `lemmatization` (default: `true`): Apply lemmatization to reduce words to their base form.
- `use_stemming` (default: `false`): Apply stemming to reduce words to their root form.
- `additional_stopwords` (default: `[]`): List of additional words to remove.

#### Vectorization

Define how text is converted into numerical vectors:

- `method` (default: `tfidf`): Vectorization method (`tfidf`, `count`, or `hashing`).
- `ngram_range` (default: `[1, 2]`): The range of n-values for n-grams.
- `max_df` (default: `0.85`): Maximum document frequency to filter out common terms.
- `min_df` (default: `0.01`): Minimum document frequency to filter out rare terms.
- `max_features` (default: `5000`): Maximum number of features to retain.

#### Similarity

Control how items are grouped based on similarity:

- `method` (default: `dbscan`): Clustering method (`dbscan`, `kmeans`, or `agglomerative`).
- `eps` (default: `0.5`): Maximum distance for items to be considered neighbors in `dbscan`.
- `min_samples` (default: `2`): Minimum number of samples in a cluster for `dbscan`.
- `n_clusters` (default: `5`): Number of clusters for `kmeans` and `agglomerative`.
- `linkage` (default: `average`): Linkage criterion for `agglomerative` clustering.

#### API Configuration

Specify the API for processing:

- `selected_api` (default: `Groq`): Active API (`OpenAI`, `Groq`, `Anthropic` or `Ollama`).

##### OpenAI API

- `openai_api_url`: API endpoint for OpenAI chat completions.
- `openai_api_key`: OpenAI API key.
- `openai_model`: OpenAI model to use (e.g., `gpt-3.5-turbo`).

##### Groq API

- `groq_api_url` (default: `https://api.groq.com/openai/v1/chat/completions`): Groq API endpoint.
- `groq_api_key`: Groq API key.
- `groq_model` (default: `llama3-8b-8192`): Groq model to use.

##### Anthropic API

- `anthropic_api_url` (default: `https://api.anthropic.com/v1/messages`): Anthropic API endpoint.
- `anthropic_api_key`: Anthropic API key.
- `anthropic_model`:  Anthropic model to use (e.g., `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-3-opus-20240229`)
##### Ollama API

- `ollama_api_url`: Ollama API endpoint.
- `ollama_model`: Ollama model to use.

#### Content Generation

Set the instructions for the LLM to process and rewrite content:

- `content_prefix`: Instruction template for content rewriting.

#### XML Feed

Define the settings for the XML feed:

- `max_items` (default: `50`): Maximum number of items to process.
- `max_age_days` (default: `10`): Maximum age of items in days to consider.
- `feed_title` (default: `"UglyFeed RSS"`): Title of the feed.
- `feed_link` (default: `"https://github.com/fabriziosalmi/UglyFeed"`): Link for the feed.
- `feed_description` (default: `"A dynamically generated feed using UglyFeed."`): Description of the feed.
- `feed_language` (default: `it`): Language of the feed.
- `feed_self_link` (default: `"https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml"`): Self-referencing link for the feed.
- `author` (default: `"UglyFeed"`): Author of the feed.
- `category` (default: `"Technology"`): Category of the feed.
- `copyright` (default: `"UglyFeed"`): Copyright information.

#### Scheduler

Enable and configure automated jobs:

- `scheduling_enabled` (default: `false`): Enable the scheduler.
- `scheduling_interval` (default: `4`): Interval for the scheduler.
- `scheduling_period` (default: `hours`): Period for the interval (`hours` or `minutes`).

#### HTTP Server Port

Change the port for the custom HTTP server:

- `http_server_port` (default: `8001`): Port number for the HTTP server.

#### Deployment

Configure deployment to GitHub or GitLab:

- `enable_github` (default: `false`): Enable GitHub deployment.
- `github_repo`: GitHub repository for deployment.
- `github_token`: GitHub token for authentication.
- `enable_gitlab` (default: `false`): Enable GitLab deployment.
- `gitlab_repo`: GitLab repository for deployment.
- `gitlab_token`: GitLab token for authentication.

## ▶️ Usage

- **Run Scripts**: From the `Run scripts` page, aggregate feed items by similarity and rewrite them according to the LLM instructions. Logs are displayed for debugging.
- **View and Serve XML**: View and download the generated XML, or enable the HTTP server to provide a valid XML URL for any RSS reader.
- **Deploy**: Publish the XML feed to GitHub or GitLab. A public URL will be provided for use with any RSS reader.

