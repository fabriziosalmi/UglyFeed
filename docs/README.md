# Project documentation
Welcome to the UglyFeed project documentation section. This guide provides detailed information for the scripts used by the project.

## Setup

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fabriziosalmi/UglyFeed.git
    cd UglyFeed
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```


### Configuration

1. Setup options by making your changes into the `config.yaml` file

2. Modify the `input/feeds.txt` file with your feeds urls

### Usage

1. Retrieve and aggregate RSS feeds
    ```sh
    python main.py
    ```
    
2. Rewrite and save aggregated feeds using configured LLM API:

    ```sh
    python llm_processor.py
    ```
    
3. Convert JSON to RSS feed
    ```sh
    python json2rss.py
    ```
    
4. Serve RSS XML via HTTP server
    ```sh
    python serve.py
    ```

## Project Structure

Main components:

- `requirements.txt`: List of dependencies.
- `config.yaml`: Configuration options for the application
- `main.py`: Retrieves and aggregates RSS feeds.
  - `json_manager.py`: Used by main.py, manages JSON file operations. 
  - `rss_reader.py`: Used by main.py, reads RSS feeds.
  - `similarity_checker.py`: Used by main.py, checks similarity between feeds.
- `llm_processor.py`: Rewrites aggregated feeds using a language model LLM APIs.
- `json2rss.py`: Convert JSON to RSS feed.
- `serve.py`: Serve RSS XML via HTTP server.
  - `uglyfeeds`: Used by serve.py is the directory where the uglyfeed.xml is served via HTTP

Optional components:

- `process_multiple_metrics.py`: Evaluate metrics of generated content.
- `evaluate_against_reference.py`: Evaluate metrics of generated content against reference content.

Directories:

- `input`: Directory for feeds list file
- `output`: Directory for aggregated (for similarity) feeds.
- `rewritten`: Directory for rewritten content and evaluation metrics.
- `reports`: Directory for metrics export in JSON and HTML

## Scripts documentation
Each script's documentation includes the following sections:

- **Introduction**
A brief introduction to the script, explaining its purpose and the specific problem it aims to solve.

- **Input/Output**
Information about the expected input formats and the structure of the output data, ensuring users understand what the script requires and what it produces.

- **Functionality**
A deep dive into the core functionality of the script, describing key functions and modules, and how they work together.

- **Code Structure**
An overview of the script's architecture, highlighting major components and their interactions, to give users a clear understanding of how the script is built.

#### Main scripts
- [main.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/main.py.md)
- [llm_processor.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/llm_processor.py.md)
- [json2rss.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/json2rss.py.md)
- [serve.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/serve.py.md)

## Evaluation documentation
#### Evaluation scripts
- [evaluate_against_reference.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/evaluate_against_reference.py.md)
- [process_multiple_metrics.py](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/process_multiple_metrics.py.md)
#### Evaluation docs

- [Metrics documentation](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/metrics.md)

## Additional documentation
#### Sources
- [Create RSS from any source via RSSHub](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/sources.md)


