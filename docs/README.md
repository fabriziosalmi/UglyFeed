# Documentation
Welcome to the UglyFeed documentation. This guide provides detailed information to run UglyFeed.

## Installation and automated runs (GitHub Actions)

You can use UglyFeed repo as GitHub action application source and you own repository as XML CDN, a file named uglyfeed.xml will be saved to your own repository once a day. 
You don't need to install and run anything on your computer, just copy and configure actions to fit your own needs. _I'll add more actions in the next days to cover popular setups_.

Available actions:

- [Daily delivery via Groq and llama3-8b-8192](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/UglyFeed-GitHub-Action-Groq-llama3-8b-8192.yml)


## Installation (pip)

You can use UglyFeed also via `pip install uglypy`. Users with already in place pipelines can now easily adopt the UglyFeed features. Here the [pypi.org uglypy page](https://pypi.org/project/uglypy/0.0.1/), please check the documentation to understand how to run it.

⚠️ Note that the 0.0.1 version is missing some features, I will add them very soon :) 

## Installation and run (without Docker)

Clone the repository and run the web application:

```sh
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
streamlit run gui.py --server.address 0.0.0.0
```

If you want to disable Streamlit telemetry just run this command: 

`streamlit run gui.py --server.address 0.0.0.0 --browser.gatherUsageStats false`

## Installation and run (with Docker)
Populate config.yaml and feeds.txt with your own settings and mount such files in the container. To start the UglyFeed app, use the following `docker run` command:

```bash
docker run -p 8001:8001 -p 8501:8501 -v /path/to/local/feeds.txt:/app/input/feeds.txt -v /path/to/local/config.yaml:/app/config.yaml fabriziosalmi/uglyfeed:latest
```

## Installation and run (Docker Compose)

To start the UglyFeed app, use the following `docker run` command:

```bash
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
docker compose up -d
```

The stack defined in the `docker-compose.yaml` file has been succesfully tested on Portainer 🎉

## Configuration
- You can change source feeds by modifying the `input/feeds.txt` file or in the **Configuration** page of the web application.
- All others options can be changed via environment variables, by updating the `config.yaml` file or in the **Configuration** page of the web application.

### Options

**Similarity**
> For a general use the default values seems to be a good fit to aggressively filter out some noise. To increase items count try to reduce min_samples to 2 and play around eps and similarity.

- `similarity_threshold` (range: 0-1, example: `0.5`)
- `min_samples` (Minimum number of samples in a cluster for DBSCAN, example: `3`)
- `eps` (Maximum distance between two samples for one to be considered as in the neighborhood of the other in DBSCAN, example: `0.65`)

**Preprocessing**
> Control text preprocessing steps before feeding into the system:

- `remove_html` (example: `true`): Remove HTML tags from the text.
- `lowercase` (example: `true`): Convert all text to lowercase.
- `remove_punctuation` (example: `true`): Remove punctuation from the text.
- `lemmatization` (example: `true`): Apply lemmatization to reduce words to their base form.
- `stop_words` (example: `italian`): Language for stop words removal.
- `use_stemming` (example: `false`): Apply stemming to reduce words to their root form.
- `additional_stopwords` (example: `["specific", "words"]`): Additional specific words to remove from the text.
- `min_word_length` (example: `3`): Minimum length of words to keep.

**Vectorization**
> Define how text is converted into numerical vectors:

- `method` (example: `tfidf`): Vectorization method, options include `tfidf`, `count`, or `hashing`.
- `max_df` (example: `0.85`): Maximum document frequency to filter out terms that are too common.
- `min_df` (example: `0.01`): Minimum document frequency to filter out terms that are too rare.
- `max_features` (example: `5000`): Maximum number of features to retain in the vectorized representation.

**LLM API and model**
> You can use OpenAI API, Groq API or Ollama API:

- `selected_api` (Active API can be `OpenAI`, `Groq`, or `Ollama`)

- `openai_api_url` (OpenAI API chat completions endpoint)
- `openai_api_key` (OpenAI API key) 
- `openai_model` (OpenAI [models](https://platform.openai.com/docs/models))

- `groq_api_url` (Groq API OpenAI compatible chat completion endpoint)
- `groq_api_key` (Groq API key)
- `groq_model` (Groq [models](https://console.groq.com/docs/models)) 

- `ollama_api_url` (Ollama API endpoint)
- `ollama_model` (Ollama [models](https://platform.openai.com/docs/models)) 

**Instructions/role/prompt**
> You can force the LLM to translate, aggregate, summarize, extend, say the opposite or any other creative mix you can imagine, just test it against a bunch of source feeds to fit to your own needs. If you need some ideas check the [prompts folder](https://github.com/fabriziosalmi/UglyFeed/tree/main/prompts)

- `content_prefix` (prompt to be used as instruction for the rewriting process)

**XML feed**
> You can set limits for content retention.

- `max_items`: `250` (Maximum number of items to process for the rewriting process)
- `max_age_days`: `7` (Maximum age of items in days to be considered)
- `feed_title`: `Default Feed Title`
- `feed_link`: `https://example.com`
- `feed_description`: `This is a default description for the feed.`
- `feed_language`: `en`
- `feed_self_link`: `https://example.com/feed.xml`
- `author`: `Default Author`
- `category`: `Default Category`
- `copyright`: `Copyright info`
  
**Scheduler**
> You can set automated jobs for retrieval, aggregation, rewriting and XML generation (deployment job will be soon added to the same pipeline)

- `scheduling_enabled`: `false` or `true` (Enable the scheduler)
- `scheduling_interval`: `4`
- `scheduling_period`: `hours` or `minutes`

**HTTP server port**
> You can change the port used by the custom HTTP server used to serve the final valid XML rewritten feed

- `http_server_port`: `8001`

**Deploy**
> You can publish the final generated XML feed to your own GitHub or GitLab repository.

- `enable_github`: `false` or `true`
- `github_repo`: `your_github_username/uglyfeed-cdn`
- `github_token`: `your_github_token`

- `enable_gitlab`: `false` or `true`
- `gitlab_repo`: `your_gitlab_username/uglyfeed-cdn`
- `gitlab_token`: `your_gitlab_token`


### Use

- Run all main scripts from the `Run scripts` page, feeds items will be aggregated by similarity and rewritten following the LLM instruction/prompt and options. Logs are shown in the page for debugging purposes.
- You can go to the View and Serve XML page where you can view and download the generated XML. You can also enable the HTTP server to have a valid XML URL to use with any RSS reader.
- You can go to the Deploy page to publish the XML to GitHub or GitLab, a public URL you can use with any RSS reader will be returned.
