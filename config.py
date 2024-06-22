import yaml
from pathlib import Path

config_path = Path("config.yaml")
feeds_path = Path("input/feeds.txt")

def load_config():
    """Load existing configuration if available."""
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def ensure_default_config(config_data):
    """Ensure all required keys are in the config_data with default values."""
    defaults = {
        'similarity_threshold': 0.66,
        'similarity_options': {
            'min_samples': 2,
            'eps': 0.66
        },
        'api_config': {
            'selected_api': "OpenAI",
            'openai_api_url': "https://api.openai.com/v1/chat/completions",
            'openai_api_key': "",
            'openai_model': "gpt-3.5-turbo",
            'groq_api_url': "https://api.groq.com/openai/v1/chat/completions",
            'groq_api_key': "",
            'groq_model': "llama3-70b-8192",
            'ollama_api_url': "http://localhost:11434/api/chat",
            'ollama_model': "phi3"
        },
        'folders': {
            'output_folder': "output",
            'rewritten_folder': "rewritten"
        },
        'content_prefix': "In qualità di giornalista esperto, utilizza un tono professionale, preciso e dettagliato...",
        'max_items': 50,
        'max_age_days': 10,
        'scheduling_enabled': False,
        'scheduling_interval': 2,
        'scheduling_period': 'minutes',
        'feed_title': "UglyFeed RSS",
        'feed_link': "https://github.com/fabriziosalmi/UglyFeed",
        'feed_description': "This is a default description for the feed.",
        'feed_language': "it",
        'feed_self_link': "https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/examples/uglyfeed-source-1.xml",
        'author': "UglyFeed",
        'category': "Fun",
        'copyright': "None",
        'http_server_port': 8001  # Default server port
    }

    def recursive_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = recursive_update(d.get(k, {}), v)
            else:
                d.setdefault(k, v)
        return d

    return recursive_update(config_data, defaults)

def save_configuration(config_data, feeds):
    """Save configuration and feeds to file."""
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)
    with open(feeds_path, "w") as f:
        f.write(feeds)
