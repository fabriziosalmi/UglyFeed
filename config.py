import yaml
from pathlib import Path

config_path = Path("config.yaml")
feeds_path = Path("input/feeds.txt")

def tuple_constructor(loader, node):
    """Constructor for !!python/tuple tag."""
    return tuple(loader.construct_sequence(node))

# Add the constructor to PyYAML with SafeLoader replaced by the FullLoader to handle tuples
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
        'input_feeds_path': "input/feeds.txt",
        'similarity_threshold': 0.5,
        'preprocessing': {
            'remove_html': True,
            'lowercase': True,
            'remove_punctuation': True,
            'lemmatization': True,
            'use_stemming': False,
            'stop_words': 'italian',
            'additional_stopwords': [],
            'min_word_length': 2,
        },
        'vectorization': {
            'method': 'tfidf',
            'ngram_range': (1, 2),
            'max_df': 0.85,
            'min_df': 0.01,
            'max_features': 5000,
        },
        'similarity_options': {
            'method': 'dbscan',
            'eps': 0.5,
            'min_samples': 2,
            'n_clusters': 5,
            'linkage': 'average'
        },
        'api_config': {
            'selected_api': "Groq",
            'openai_api_url': "https://api.openai.com/v1/chat/completions",
            'openai_api_key': "",
            'openai_model': "gpt-3.5-turbo",
            'groq_api_url': "https://api.groq.com/openai/v1/chat/completions",
            'groq_api_key': "",
            'groq_model': "llama3-8b-8192",
            'ollama_api_url': "http://localhost:11434/api/chat",
            'ollama_model': "phi3",
            'anthropic_api_key': "your_anthropic_api_key",
            'anthropic_api_url': "https://api.anthropic.com/v1/messages",
            'anthropic_model': "claude-3-haiku-20240307"
        },
        'folders': {
            'output_folder': "output",
            'rewritten_folder': "rewritten"
        },
        'prompt_file': "prompt_IT.txt",
        'max_items': 50,
        'max_age_days': 10,
        'feed_title': "UglyFeed RSS",
        'feed_link': "https://github.com/fabriziosalmi/UglyFeed",
        'feed_description': "A dynamically generated feed using UglyFeed.",
        'feed_language': "it",
        'feed_self_link': "https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml",
        'author': "UglyFeed",
        'category': "Technology",
        'copyright': "UglyFeed",
        'moderation': {
            'enabled': False,
            'words_file': 'moderation/IT.txt',
            'allow_duplicates': False
        },
        'scheduling_enabled': False,
        'scheduling_interval': 4,
        'scheduling_period': 'hours',
        'http_server_port': 8001,
        'enable_github': False,
        'enable_gitlab': False,
        'github_repo': 'your_github_username/uglyfeed-cdn',
        'github_token': 'your_github_token',
        'gitlab_repo': 'your_gitlab_username/uglyfeed-cdn',
        'gitlab_token': 'your_gitlab_token',
        'tts': {
            'input': "rewritten",
            'output': "media",
            'language': "it",
            'speed_factor': 1.25,
            'enable_tts': False
        }
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
