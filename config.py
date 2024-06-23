import yaml
from pathlib import Path

config_path = Path("config.yaml")
feeds_path = Path("input/feeds.txt")

def tuple_constructor(loader, node):
    """Constructor for !!python/tuple tag."""
    return tuple(loader.construct_sequence(node))

# Add the constructor to PyYAML with SafeLoader replaced by the BaseLoader to handle tuples
yaml.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor, Loader=yaml.FullLoader)

def load_config(config_file=config_path):
    """Load the configuration from the specified YAML file."""
    if isinstance(config_file, str):
        config_file = Path(config_file)

    try:
        if config_file.exists():
            with open(config_file, "r") as f:
                return yaml.load(f, Loader=yaml.FullLoader)  # Use yaml.FullLoader to support custom constructors
        else:
            return {}
    except yaml.YAMLError as e:
        raise Exception(f"Error loading YAML configuration: {e}")
    except Exception as e:
        raise Exception(f"Failed to load configuration from {config_file}: {e}")

def ensure_default_config(config_data):
    """Ensure all required keys are in the config_data with default values."""
    defaults = {
        'similarity_threshold': 0.5,  # Updated to match the latest config
        'preprocessing': {
            'remove_html': True,
            'lowercase': True,
            'remove_punctuation': True,
            'lemmatization': True,
            'use_stemming': False,
            'stop_words': 'italian',  # Assuming Italian stop words as default
            'additional_stopwords': [],
            'min_word_length': 2,  # Adding minimum word length as a common option
        },
        'vectorization': {
            'method': 'tfidf',  # Options: 'tfidf', 'count', 'hashing'
            'ngram_range': (1, 3),  # Updated to reflect the tuple format in config.yaml
            'max_df': 0.85,
            'min_df': 0.01,
            'max_features': 5000,
        },
        'similarity_options': {
            'method': 'dbscan',  # Options: 'dbscan', 'kmeans', 'agglomerative'
            'eps': 0.5,  # Only for DBSCAN
            'min_samples': 2,  # Only for DBSCAN
            'n_clusters': 5,  # Only for 'kmeans' and 'agglomerative'
            'linkage': 'average'  # Only for 'agglomerative'
        },
        'api_config': {
            'selected_api': "Groq",  # Default to Groq as per latest config
            'openai_api_url': "https://api.openai.com/v1/chat/completions",
            'openai_api_key': "",
            'openai_model': "gpt-3.5-turbo",
            'groq_api_url': "https://api.groq.com/openai/v1/chat/completions",
            'groq_api_key': "",
            'groq_model': "llama3-8b-8192",  # Updated to the latest model
            'ollama_api_url': "http://localhost:11434/api/chat",
            'ollama_model': "phi3"
        },
        'folders': {
            'output_folder': "output",
            'rewritten_folder': "rewritten"
        },
        'content_prefix': "Sei un giornalista esperto quindi utilizza un tono professionale, preciso e dettagliato...",
        'max_items': 50,
        'max_age_days': 10,
        'scheduling_enabled': True,  # Updated to reflect enabled scheduling
        'scheduling_interval': 4,  # Updated to the latest config
        'scheduling_period': 'hours',  # Updated to match the latest config
        'feed_title': "UglyFeed RSS",
        'feed_link': "https://github.com/fabriziosalmi/UglyFeed",
        'feed_description': "A dynamically generated feed using UglyFeed.",
        'feed_language': "it",
        'feed_self_link': "https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml",
        'author': "UglyFeed",
        'category': "Technology",
        'copyright': "UglyFeed",
        'http_server_port': 8001,  # Default server port
        'enable_github': False,  # Updated to match the latest config
        'enable_gitlab': False,  # Updated to match the latest config
        'github_repo': 'your_github_username/uglyfeed-cdn',
        'github_token': 'your_github_token',
        'gitlab_repo': 'your_gitlab_username/uglyfeed-cdn',
        'gitlab_token': 'your_gitlab_token',
    }

    def recursive_update(d, u):
        """Recursively update dictionary d with u."""
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = recursive_update(d.get(k, {}), v)
            else:
                d.setdefault(k, v)
        return d

    return recursive_update(defaults, config_data)  # Update with default values if not present

def save_configuration(config_data, feeds):
    """Save configuration and feeds to file."""
    try:
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)
        with open(feeds_path, "w") as f:
            f.write(feeds)
    except Exception as e:
        raise Exception(f"Failed to save configuration: {e}")

# Usage example
if __name__ == "__main__":
    config = load_config()
    config = ensure_default_config(config)
    save_configuration(config, "https://example.com/rss/feed\nhttps://another.com/rss/feed")
