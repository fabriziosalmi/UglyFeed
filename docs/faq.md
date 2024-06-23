# UglyFeed Q&A

Welcome to the UglyFeed Q&A. This document answers common questions about UglyFeed, its functionalities, configurations, and advanced features.

## Table of Contents

- [General Functionality](#general-functionality)
- [Configuration and Customization](#configuration-and-customization)
- [API Integration and Advanced Features](#api-integration-and-advanced-features)
- [Usage and Operations](#usage-and-operations)

## General Functionality

- **Q:** What is UglyFeed?
- **A:** UglyFeed is a minimalistic RSS feed aggregator that not only fetches and processes content from multiple RSS feeds but also uses advanced language models (LLMs) to rewrite and enhance the content, delivering an impeccably curated final feed.

- **Q:** How does UglyFeed fetch RSS feeds?
- **A:** UglyFeed reads URLs from a specified file and uses the `feedparser` library to fetch and parse the content of these RSS feeds efficiently.

- **Q:** What preprocessing steps does UglyFeed perform on feed content?
- **A:** UglyFeed can remove HTML tags, convert text to lowercase, remove punctuation, apply lemmatization, and use stemming, all configurable to suit the user’s needs.

- **Q:** What methods does UglyFeed use for text vectorization?
- **A:** UglyFeed supports TF-IDF, Count Vectorization, and Hashing Vectorization to convert text into numerical vectors for analysis and comparison.

- **Q:** How does UglyFeed determine the similarity between articles?
- **A:** UglyFeed uses cosine similarity to evaluate how closely related the content of different articles is, based on their textual features.

- **Q:** What clustering methods are available in UglyFeed for grouping similar articles?
- **A:** UglyFeed offers several clustering methods, including DBSCAN, KMeans, and Agglomerative clustering, to group articles by their similarities.

- **Q:** Can UglyFeed detect the language of the articles it processes?
- **A:** Yes, UglyFeed uses the `langdetect` library to automatically detect and handle the language of each article, ensuring appropriate processing and analysis.

- **Q:** How does UglyFeed handle stopwords during text preprocessing?
- **A:** UglyFeed removes common stopwords using lists from the `nltk` library, and users can specify additional stopwords in the configuration to further refine the content.

- **Q:** What is the role of the `content_prefix` setting in UglyFeed?
- **A:** The `content_prefix` sets the context or instructions for the language model to follow when rewriting and enhancing the feed content, allowing for tailored output that meets specific editorial standards.

- **Q:** How does UglyFeed transform and manage RSS feeds from the processed content?
- **A:** UglyFeed converts the processed and rewritten articles into an XML format for RSS feeds, managing updates and ensuring the final feed is aligned with the configured retention and presentation policies.

## Configuration and Customization

- **Q:** How can I customize text preprocessing options in UglyFeed?
- **A:** You can configure options like HTML tag removal, text conversion to lowercase, punctuation removal, lemmatization, and stemming in the `config.yaml` file under the `preprocessing` section.

- **Q:** What vectorization parameters can be adjusted in UglyFeed?
- **A:** Parameters such as the vectorization method (TF-IDF, Count, or Hashing), n-gram range, maximum and minimum document frequency, and maximum number of features can be adjusted in the `config.yaml` file.

- **Q:** How do I change the clustering method used by UglyFeed?
- **A:** The clustering method can be set in the `config.yaml` file under the `similarity_options` section, allowing you to choose between DBSCAN, KMeans, and Agglomerative clustering.

- **Q:** How can I set the output directory for the processed articles in UglyFeed?
- **A:** The output directory can be specified in the `config.yaml` file under the `folders` section, directing where the processed articles and feeds will be stored.

- **Q:** How do I adjust the similarity threshold for article grouping?
- **A:** You can change the similarity threshold in the `config.yaml` file, which controls how closely articles need to be related to be grouped together.

- **Q:** How can I customize the appearance and content of the generated RSS feed?
- **A:** You can set the feed’s title, link, description, language, and other metadata in the `config.yaml` file under the RSS feed settings.

- **Q:** Can UglyFeed handle feeds in multiple languages?
- **A:** Yes, UglyFeed can process and detect content in various languages, adapting its preprocessing and clustering accordingly.

- **Q:** How do I set a maximum number of items to include in the RSS feed?
- **A:** The `max_items` setting in the `config.yaml` file allows you to limit the number of items included in the RSS feed.

- **Q:** How can I define additional stopwords for removal during preprocessing?
- **A:** Additional stopwords can be specified as a list in the `config.yaml` file under the `preprocessing` section.

- **Q:** What happens if required environment variables are not set in UglyFeed?
- **A:** If environment variables are not set, UglyFeed defaults to the values specified in the configuration file.

## API Integration and Advanced Features

- **Q:** Which APIs can UglyFeed integrate with for content processing?
- **A:** UglyFeed supports integration with OpenAI, Groq, Ollama, and Anthropic APIs to leverage advanced language models for content enhancement and rewriting.

- **Q:** How can I switch between different language model APIs in UglyFeed?
- **A:** You can select the desired API in the `api_config` section of the `config.yaml` file, customizing the processing according to your preferred service.

- **Q:** What is the `MAX_TOKENS` setting used for in UglyFeed?
- **A:** The `MAX_TOKENS` setting defines the maximum number of tokens allowed during content processing with language models to ensure the output fits within API constraints.

- **Q:** How does UglyFeed handle rate limiting with APIs?
- **A:** UglyFeed includes retry mechanisms and parses rate limit headers to manage API rate limiting, automatically retrying requests as needed.

- **Q:** Can UglyFeed rewrite aggregated content using language models?
- **A:** Yes, UglyFeed can utilize language models to rewrite and enhance aggregated content, creating a polished and cohesive output that aligns with the given instructions.

- **Q:** How can I customize the instructions given to language models in UglyFeed?
- **A:** You can modify the `content_prefix` in the `config.yaml` file to provide specific rewriting instructions for the language model to follow.

- **Q:** What logging options are available in UglyFeed?
- **A:** UglyFeed uses a flexible logging setup defined in `logging_setup.py`, allowing logs to be directed to the console or a file with configurable verbosity levels.

- **Q:** How does UglyFeed save processed and rewritten articles?
- **A:** Processed and rewritten articles are saved as JSON files in the directories specified in the configuration, making them available for further processing or review.

- **Q:** Can UglyFeed run as a standalone HTTP server?
- **A:** Yes, UglyFeed can be configured to run on a custom HTTP server port, serving the generated XML feed through a web interface.

- **Q:** How can I deploy the generated RSS feed to GitHub or GitLab?
- **A:** Deployment settings in the `config.yaml` file allow you to configure GitHub and GitLab integrations, including tokens and repository details for automatic publishing.

## Usage and Operations

- **Q:** How do I start UglyFeed without Docker?
- **A:** Clone the repository and start the application using Streamlit with the command: `streamlit run gui.py --server.address 0.0.0.0`.

- **Q:** How can I run UglyFeed with Docker?
- **A:** Populate `config.yaml` and `feeds.txt`, and use Docker to run the container with the necessary volume mounts and port mappings, as specified in `docker-compose.yml`.

- **Q:** What is the purpose of the `scheduling_enabled` option in UglyFeed?
- **A:** The `scheduling_enabled` setting allows you to enable the scheduler to automatically fetch and process feeds at specified intervals.

- **Q:** How do I specify the scheduling interval for automated jobs in UglyFeed?
- **A:** You can configure the interval and period (e.g., minutes, hours, days) for scheduling in the `config.yaml` file, enabling automated feed updates and processing.

- **Q:** How does UglyFeed manage and serve the XML feed?
- **A:** UglyFeed can serve the generated XML feed through a built-in HTTP server, providing a direct URL that can be used by any RSS reader to access the feed.

- **Q:** Can I monitor and debug the scripts running in UglyFeed?
- **A:** Yes, UglyFeed provides detailed logs and output for each script execution, which can be viewed and debugged through the web interface or log files.

- **Q:** What happens during the script execution in UglyFeed?
- **A:** Scripts like `main.py`, `llm_processor.py`, and `json2rss.py` are run sequentially to fetch feeds, process and rewrite content, and generate the final RSS feed.

- **Q:** How can I configure the logging setup in UglyFeed?
- **A:** Logging configurations are defined in `logging_setup.py`, where you can adjust log levels, formats, and handlers for both console and file outputs.

- **Q:** What options do I have for running scripts in UglyFeed?
- **A:** You can run individual scripts or a sequence of scripts directly from the web interface, with real-time output and error logging for each execution.

- **Q:** How does UglyFeed handle HTTP requests for the XML feed?
- **A:** UglyFeed uses a custom HTTP server to serve the XML feed with correct content type and cache headers, ensuring compatibility with RSS readers.

- **Q:** Can UglyFeed operate in a Docker container?
- **A:** Yes, UglyFeed is fully compatible with Docker, and can be run using Docker or Docker Compose with pre-configured settings in `docker-compose.yml`.

- **Q:** How do I update the XML feed generated by UglyFeed?
- **A:** The XML feed is updated whenever the processing scripts are run, either manually or automatically through the scheduler, and can be redeployed as needed.

- **Q:** Can UglyFeed handle multiple RSS feeds and aggregate them into a single output?
- **A:** Yes, UglyFeed can process and aggregate multiple RSS feeds into a single cohesive output, which is then enhanced and rewritten using LLMs.

- **Q:** What scheduling capabilities does UglyFeed offer?
- **A:** UglyFeed offers flexible scheduling options, allowing you to set intervals for automatic execution of feed fetching and processing tasks.

- **Q:** How do I ensure the XML feed is always up-to-date in UglyFeed?
- **A:** By enabling scheduling and configuring regular intervals for script execution, you can ensure the XML feed is consistently updated with the latest content.

- **Q:** How can I control the number of items and their age in the XML feed?
- **A:** The `max_items` and `max_age_days` settings in the `config.yaml` file allow you to limit the number and age of items included in the RSS feed.

- **Q:** Can UglyFeed rewrite content in multiple languages?
- **A:** Yes, UglyFeed’s language models can process and rewrite content in various languages, depending on the capabilities of the selected API.

- **Q:** How does UglyFeed enhance the quality of the final feed content?
- **A:** By using advanced language models to rewrite and refine the aggregated content, UglyFeed ensures the final feed is clear, coherent, and professionally polished.

- **Q:** What should I do if I encounter an error during script execution in UglyFeed?
- **A:** Check the detailed logs provided by UglyFeed to identify and troubleshoot errors. You can also refer to the documentation or open an issue on the GitHub repository for further assistance.

- **Q:** How do I deploy and serve the XML feed for public access?
- **A:** After generating the XML feed, you can deploy it to GitHub or GitLab using the deployment features in UglyFeed, providing a public URL that can be accessed by any RSS reader.
