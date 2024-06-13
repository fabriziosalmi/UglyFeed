# Documentation
Welcome to the UglyFeed documentation. This guide provides detailed information to run UglyFeed.

## Installation and run

Clone the repository and run the web application:

```sh
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
streamlit run gui.py --server.address 0.0.0.0
```

If you want to disable streamlit telemetry just add browser.gatherUsageStats flag:

`streamlit run gui.py --server.address 0.0.0.0 --browser.gatherUsageStats false`


## Configuration

You can change source feeds by modifying the `input/feeds.txt` file or in the **Configuration** page of the web application.

You can change options by modifying the `config.yaml` file or in the **Configuration** page of the web application.

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

**Scheduler options**
- `scheduling_enabled`: `true` (Enable the scheduler)
- `scheduling_interval`: `4` 
- `scheduling_period`: `hours`

**Deploy options**

- `github_token`: your_github_token
- `gitlab_token`: your_gitlab_token
- `github_repo`: your_github_username/uglyfeed-cdn
- `gitlab_repo`: your_gitlab_username/uglyfeed-cdn
- `enable_github`: `false` or `true`
- `enable_gitlab`: `false` or `true`



### Use

- Run all main scripts from the `Run scripts` page, feeds items will be aggregated by similarity and rewritten following the LLM instruction/prompt and options. Logs are shown in the page for debugging purposes.
- Go to the View and Serve XML page where you can view and download the generated XML. You can also enable the HTTP server to have a valid XML URL to use with any RSS reader.
- Go to the Deploy page to publish the XML to GitHub or GitLab, a public URL you can use with any RSS reader will be returned.
