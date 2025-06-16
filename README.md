# <img src="https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/docs/UglyFeed.png" alt="UglyFeed" height="32" width="32"> UglyFeed

UglyFeed is a **simple** application designed to **retrieve**, **aggregate**, **filter**, **rewrite**, **evaluate** and **serve** content (RSS feeds) written by a large language model. This repository provides the [code](https://github.com/fabriziosalmi/UglyFeed.git), the **[documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md)**, a [FAQ](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/faq.md), a [troubleshooting guide](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/troubleshooting.md), and some optional scripts to evaluate the generated content.

![GitHub last commit](https://img.shields.io/github/last-commit/fabriziosalmi/UglyFeed) ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-raw/fabriziosalmi/UglyFeed) [![Pylint](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml/badge.svg)](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml) [![CodeQL](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/github-code-scanning/codeql) ![Docker Pulls](https://img.shields.io/docker/pulls/fabriziosalmi/uglyfeed) ![PyPI - Downloads](https://img.shields.io/pypi/dm/uglypy?label=uglypy) ![Docker Image Version](https://img.shields.io/docker/v/fabriziosalmi/uglyfeed?style=social&logo=GitHub&labelColor=white&color=black)




## Features

- 📡 Retrieve RSS feeds
- 🧮 Aggregate feeds items by similarity
- ✨ Rewrite content using LLM API
- 💾 Save rewritten feeds to JSON files
- 🔁 Convert JSON to valid RSS feed
- 🌐 Serve XML feed via HTTP server
- 🌎 Deploy XML feed to GitHub or GitLab
- 📈 Evaluate generated content
- 🖥️ Web UI based on Streamlit
- 📰 [RSS test feeds available](https://github.com/fabriziosalmi/uglyfeed-cdn)
- 🤖 Same codebase for all releases
- 🛑 Simple post-filter moderation
- ➡️ [Translate feeds](https://github.com/fabriziosalmi/UglyFeed/blob/main/prompts/translate.txt) into your own language
- 📝 Tons of [prompts](https://github.com/fabriziosalmi/UglyFeed/tree/main/prompts) ready to use

## Get it now

- 💾 [Source code](https://github.com/fabriziosalmi/UglyFeed/releases/latest)
- 🐳 [Docker installable package](https://hub.docker.com/r/fabriziosalmi/uglyfeed)
- 🐍 [Pip installable package](https://pypi.org/project/uglypy/)
- ⚙️ [Github actions workflows](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md#%EF%B8%8F-installation-and-automated-runs-github-actions)
  
## Quick start

### Prerequisites

- 🌎 Internet connection
- 🐳 Docker
- ✨ LLM API
- 📲 RSS reader
  
**Supported API and models**

- OpenAI API (`gpt-3.5-turbo`, `gpt-4`, `gpt-4o`)
- Ollama API (all models like `llama3`, `phi3`, `qwen2`)
- Groq API (`llama3-8b-8192`, `llama3-70b-8192`, `gemma-7b-it`, `mixtral-8x7b-32768`)
- Anthropic API (`claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-3-opus-20240229`)
- Google Gemini API (Free tier: `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`, `gemini-1.5-flash-8b`, `gemma-3`, `gemma-3n`)

> You can use your own models by running a compatible OpenAI LLM server. You must change the OpenAI API url parameter.
 
### Running the Container

To start the UglyFeed app, use the following `docker run` command:

```bash
docker run -p 8001:8001 -p 8501:8501 -v /path/to/local/feeds.txt:/app/input/feeds.txt -v /path/to/local/config.yaml:/app/config.yaml fabriziosalmi/uglyfeed:latest
```

### Configure the application
In the **Configuration** page (or by manually editing the `config.yaml` file) you will find all configuration options. You must change at least the source feeds you want to aggregate, the LLM API and model to use to rewrite the aggregated feeds. You can then retrieve the final `uglyfeed.xml` feed in many ways: 

- local filesystem
- download from web UI
- HTTP server url
- HTTPS GitHub CDN url

> You can easily extend it to send it to cms, notification or messaging systems.

### Execute the application scripts
Execute all scripts in the **Run scripts** page easily by clicking on the button **Run `main.py`, `llm_processor.py`, `json2rss.py` sequentially**.
You can check for logs, errors and informational messages.

### Serve the final rewritten XML feed via HTTP
Once all scripts completed go to the **View and Serve XML** page where you can view and download the generated XML feed. If you start the HTTP server you can access to the XML url at `http://container_ip:8001/uglyfeed.xml`

### Deploy the final rewritten XML feed to GitHub/GitLab
Once all scripts completed go to the **Deploy** page where you can push the final rewritten XML file to the configured GitHub/GitLab repository, the public XML URL to use by RSS readers is returned for each enabled platform.

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

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

## Others projects

If You like my projects, you may also like these ones:

- [caddy-waf](https://github.com/fabriziosalmi/caddy-waf) Caddy WAF (Regex Rules, IP and DNS filtering, Rate Limiting, GeoIP, Tor, Anomaly Detection) 
- [patterns](https://github.com/fabriziosalmi/patterns) Automated OWASP CRS and Bad Bot Detection for Nginx, Apache, Traefik and HaProxy
- [blacklists](https://github.com/fabriziosalmi/blacklists) Hourly updated domains blacklist 🚫 
- [proxmox-vm-autoscale](https://github.com/fabriziosalmi/proxmox-vm-autoscale) Automatically scale virtual machines resources on Proxmox hosts 
- [proxmox-lxc-autoscale](https://github.com/fabriziosalmi/proxmox-lxc-autoscale) Automatically scale LXC containers resources on Proxmox hosts 
- [DevGPT](https://github.com/fabriziosalmi/DevGPT) Code togheter, right now! GPT powered code assistant to build project in minutes
- [websites-monitor](https://github.com/fabriziosalmi/websites-monitor) Websites monitoring via GitHub Actions (expiration, security, performances, privacy, SEO)
- [caddy-mib](https://github.com/fabriziosalmi/caddy-mib) Track and ban client IPs generating repetitive errors on Caddy 
- [zonecontrol](https://github.com/fabriziosalmi/zonecontrol) Cloudflare Zones Settings Automation using GitHub Actions 
- [lws](https://github.com/fabriziosalmi/lws) linux (containers) web services
- [cf-box](https://github.com/fabriziosalmi/cf-box) cf-box is a set of Python tools to play with API and multiple Cloudflare accounts.
- [limits](https://github.com/fabriziosalmi/limits) Automated rate limits implementation for web servers 
- [dnscontrol-actions](https://github.com/fabriziosalmi/dnscontrol-actions) Automate DNS updates and rollbacks across multiple providers using DNSControl and GitHub Actions 
- [proxmox-lxc-autoscale-ml](https://github.com/fabriziosalmi/proxmox-lxc-autoscale-ml) Automatically scale the LXC containers resources on Proxmox hosts with AI
- [csv-anonymizer](https://github.com/fabriziosalmi/csv-anonymizer) CSV fuzzer/anonymizer
- [iamnotacoder](https://github.com/fabriziosalmi/iamnotacoder) AI code generation and improvement


## Disclaimer

> _It is crucial to acknowledge the potential misuse of AI language models by this tool. The use of adversarial prompts and models can easily lead to the creation of misleading content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## License

This project is licensed under the AGPL3 License.
