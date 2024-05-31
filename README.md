# UglyFeed

UglyFeed is a **simple** Python application designed to **retrieve**, **aggregate**, **filter**, **rewrite**, **evaluate** and **serve** content (RSS feeds) written by a large language model. This repository provides the code, the **[documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/README.md)** and all necessary files to run the application.

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
- 📰 [an RSS reader](https://github.com/topics/rss-reader) (to retrieve the final feed I use [FluentReader](https://github.com/yang991178/fluent-reader) on laptop and [NetNewsWire](https://netnewswire.com/) on mobile)
- 🤖 a large language model

**Supported API and models**

- OpenAI API (`gpt-3.5-turbo`, `gpt4`, `gpt4o`)
- Ollama API (all models like `llama3` or `phi3`)
- Groq API (`llama3-8b-8192`, `llama3-70b-8192`, `gemma-7b-it`, `mixtral-8x7b-32768`)


## [Documentation](https://github.com/fabriziosalmi/UglyFeed/tree/main/docs)

Please refer to the updated documentation [here](https://github.com/fabriziosalmi/UglyFeed/tree/main/docs).

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
- **Crisis Communication**: Quickly rewrite and disseminate critical updates during emergencies, ensuring clear and consistent messaging.
- **Fake News Detection Datasets**: Generate datasets by rewriting news articles for use in training models to recognize and combat fake news.
- **Image Captioning**: Integrate with image recognition systems to create engaging and accurate descriptions for images.
- **AI-Driven Research Companions**: Develop virtual research assistants that can provide concise summaries and 

## Contribution

Feel free to open issues or submit pull requests. Any contributions are welcome!

[![Pylint](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml/badge.svg)](https://github.com/fabriziosalmi/UglyFeed/actions/workflows/pylint.yml)

## Disclaimer

> _It is crucial to acknowledge the potential misuse of AI language models by this tool. The use of adversarial prompts and models can easily lead to the creation of misleading content. This application should not be used with the intent to deceive or mislead others. Be a responsible user and prioritize ethical practices when utilizing language models and AI technologies._

## License

This project is licensed under the MIT License.
