# UglyFeed

UglyFeed is a **simple** Python application designed to **retrieve**, **aggregate**, **filter**, **rewrite**, **evaluate** and **serve** content (RSS feeds) written by a large language model. This repository provides the code, the **[documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md)** and all necessary files to run the application.

<p align="center">
  <img src="https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/docs/UglyFeed.png" alt="UglyFeed">
</p>

## Features

- 📡 Retrieve RSS feeds
- 🧮 Aggregate feeds items by similarity
- 🤖 Rewrite aggregated feeds using a language model
- 💾 Save rewritten feeds to JSON files
- 🔁 Convert JSON to valid RSS feed
- 🌐 Serve XML feed via HTTP server
- 🌎 Deploy XML feed to GitHub or GitLab
- 📈 Evaluate generated content
- 🖥️ Web UI based on Streamlit

**Requirements**
- 🐍 Python
- 🌎 Internet connection
- 📰 [an RSS reader](https://github.com/topics/rss-reader) (to retrieve the final feed I use [FluentReader](https://github.com/yang991178/fluent-reader) on laptop and [NetNewsWire](https://netnewswire.com/) on mobile)
- 🤖 a large language model

**Supported API and models**

- OpenAI API (`gpt-3.5-turbo`, `gpt4`, `gpt4o`)
- Ollama API (all models like `llama3` or `phi3`)
- Groq API (`llama3-8b-8192`, `llama3-70b-8192`, `gemma-7b-it`, `mixtral-8x7b-32768`)

## Quick start

### Prerequisites

- **Docker**: Ensure you have Docker installed on your system. You can download and install it from [Docker's official site](https://www.docker.com/get-started).
- **Ollama** to run local models or an **OpenAI** or **Groq** API key.

### Running the Container

To start the UglyFeed app, use the following `docker run` command:

```bash
docker run -p 8001:8001 -p 8501:8501 fabriziosalmi/uglyfeed:latest
```

### Configure the application
In the Configuration page you can change options for aggregation similarity, LLM API and model, retention options and the scheduler.

### Execute the application scripts
Execute all scripts in the **Run scripts** page easily by clicking on the button **Run `main.py`, `llm_processor.py`, `json2rss.py` sequentially**.
You can check for logs, errors and informational messages.

### Get the final rewritten XML feed
Once all scripts completed go to the View and Serve XML page and start the HTTP server, you can access to the final rewritten XML url at `http://container_ip:8001/uglyfeed.xml`

### Deploy the final rewritten XML feed
Once all scripts completed go to the Deploy page where you can push the final rewritten XML file to the configured GitHub/GitLab repository, the public XML URL to use by RSS readers is returned for each enabled platform.

## Documentation

Please refer to the extended [documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md) to better understand how to get the best from this application.

## Use cases

The project can be easily customized to fit several use cases:

- **Smart Content Curation**: Create bespoke newsfeeds tailored to niche interests, blending articles from diverse sources into a captivating, engaging narrative.
- **Dynamic Blog Generation**: Automate blog post creation by rewriting and enhancing existing articles, optimizing them for readability and SEO.
- **Interactive Educational Tools**: Develop AI-driven study aids that summarize and rephrase academic papers or textbooks, making complex topics more accessible and fun.
- **Personalized Reading Experiences**: Craft custom reading lists that adapt to user preferences, offering fresh perspectives on favorite topics.
- **Brand Monitoring**: Aggregate and summarize brand mentions across the web, providing concise, actionable insights for marketing teams.
- **Multilingual Content Delivery**: Automatically translate and rewrite content from international sources, broadening the scope of accessible information.
- **Enhanced RSS Feeds**: Offer enriched RSS feeds that summarize, evaluate, and filter content, providing users with high-quality, relevant updates.
- **Creative Writing Assistance**: Assist writers by generating rewritten drafts of their work, helping overcome writer's block and sparking new ideas.
- **Content Repurposing**: Transform long-form content into shorter, more digestible formats like infographics, slideshows, and social media snippets.
- **Fake News Detection Datasets**: Generate datasets by rewriting news articles for use in training models to recognize and combat fake news.
- **Image Captioning**: Integrate with image recognition systems to create engaging and accurate descriptions for images.
- **AI-Driven Research Companions**: Develop virtual research assistants that can provide concise summaries and save time.

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

[![Pylint](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml/badge.svg)](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml)

## Disclaimer

> _It is crucial to acknowledge the potential misuse of AI language models by this tool. The use of adversarial prompts and models can easily lead to the creation of misleading content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## License

This project is licensed under the MIT License.
