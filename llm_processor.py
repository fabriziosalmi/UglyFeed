"""
This script processes JSON files using various LLM APIs and saves the rewritten content.
Supports OpenAI and compatible APIs, including Azure OpenAI, Anthropic, Groq, and Ollama.
"""

import re
import json
import logging
import argparse
import yaml
import os
import sys
import time
from pathlib import Path
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI
from typing import Optional, Dict, Any, Union, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Maximum context length for LLM APIs
MAX_TOKENS = 32768

class APIClientFactory:
    """Factory class to create appropriate API clients based on provider type."""
    
    @staticmethod
    def create_client(provider: str, api_key: str, api_url: Optional[str] = None) -> 'BaseAPIClient':
        """Create and return appropriate API client based on provider."""
        providers = {
            'openai': OpenAICompatibleClient,
            'azure': AzureOpenAIClient,
            'anthropic': AnthropicClient,
            'groq': GroqClient,
            'ollama': OllamaClient,
            'together': TogetherAIClient,
            'mistral': MistralAIClient,
            'gemini': GeminiClient
        }
        
        client_class = providers.get(provider.lower())
        if not client_class:
            raise ValueError(f"Unsupported provider: {provider}")
            
        return client_class(api_key, api_url)

class BaseAPIClient:
    """Base class for API clients."""
    
    def __init__(self, api_key: str, api_url: Optional[str] = None):
        self.api_key = api_key
        self.api_url = api_url or self._get_default_api_url()
        self.session = self._create_session()

    def _get_default_api_url(self) -> str:
        """Get default API URL for the provider."""
        raise NotImplementedError
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        retry = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_headers(self) -> Dict[str, str]:
        """Get headers for API request."""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def format_messages(self, content: str) -> List[Dict[str, str]]:
        """Format messages for API request."""
        return [
            {"role": "system", "content": "You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources."},
            {"role": "user", "content": content}
        ]

    def parse_response(self, response: Dict[str, Any]) -> Optional[str]:
        """Parse API response and extract content."""
        raise NotImplementedError

    def handle_rate_limit(self, response: requests.Response) -> Optional[float]:
        """Handle rate limiting and return retry delay if applicable."""
        if 'rate_limit_exceeded' in response.text:
            try:
                retry_after = float(re.search(r"try again in (\d+\.?\d*)s", 
                                            response.json()['error']['message']).group(1))
                return retry_after
            except (KeyError, AttributeError):
                return 60.0  # Default retry after 60 seconds
        return None

    def call_api(self, content: str, model: str) -> Optional[str]:
        """Make API call and return processed response."""
        try:
            data = {
                "model": model,
                "messages": self.format_messages(content),
                "max_tokens": 4096,
                "temperature": 0.7
            }
            
            response = self.session.post(
                self.api_url,
                headers=self.get_headers(),
                json=data
            )
            
            if response.status_code == 429:  # Rate limit exceeded
                retry_after = self.handle_rate_limit(response)
                if retry_after:
                    logger.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                    return self.call_api(content, model)
                    
            response.raise_for_status()
            return self.parse_response(response.json())
            
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            if response is not None:
                logger.error(f"Response content: {response.text}")
            return None

class OpenAICompatibleClient(BaseAPIClient):
    """Client for OpenAI and compatible APIs."""
    
    def _get_default_api_url(self) -> str:
        return "https://api.openai.com/v1/chat/completions"

    def call_api(self, content: str, model: str) -> Optional[str]:
        """Call API using the official OpenAI client."""
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.api_url)
            response = client.chat.completions.create(
                model=model,
                messages=self.format_messages(content),
                max_tokens=4096,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            return None
        
    def parse_response(self, response: Dict[str, Any]) -> Optional[str]:
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing OpenAI compatible response: {e}")
            return None

class AzureOpenAIClient(OpenAICompatibleClient):
    """Client for Azure OpenAI Services."""
    
    def get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }

class AnthropicClient(BaseAPIClient):
    """Client for Anthropic API."""
    
    def _get_default_api_url(self) -> str:
        return "https://api.anthropic.com/v1/messages"
        
    def get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        }
        
    def parse_response(self, response: Dict[str, Any]) -> Optional[str]:
        try:
            content_items = response.get('content', [])
            return " ".join(item['text'] for item in content_items if 'text' in item)
        except (KeyError, AttributeError) as e:
            logger.error(f"Error parsing Anthropic response: {e}")
            return None

class GroqClient(OpenAICompatibleClient):
    """Client for Groq API."""
    
    def _get_default_api_url(self) -> str:
        return "https://api.groq.com/openai/v1/chat/completions"

class TogetherAIClient(OpenAICompatibleClient):
    """Client for Together.ai API."""
    
    def _get_default_api_url(self) -> str:
        return "https://api.together.xyz/v1/chat/completions"

class MistralAIClient(OpenAICompatibleClient):
    """Client for Mistral AI API."""
    
    def _get_default_api_url(self) -> str:
        return "https://api.mistral.ai/v1/chat/completions"

class OllamaClient(BaseAPIClient):
    """Client for Ollama API."""
    
    def _get_default_api_url(self) -> str:
        return "http://localhost:11434/api/chat"
        
    def get_headers(self) -> Dict[str, str]:
        return {'Content-Type': 'application/json'}
        
    def parse_response(self, response: Dict[str, Any]) -> Optional[str]:
        try:
            return response['message']['content']
        except (KeyError, AttributeError) as e:
            logger.error(f"Error parsing Ollama response: {e}")
            return None

class GeminiClient(BaseAPIClient):
    """Client for Google Gemini API."""
    
    def _get_default_api_url(self) -> str:
        return "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
    def get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json'
        }
    
    def format_messages(self, content: str) -> Dict[str, Any]:
        """Format messages for Gemini API request."""
        return {
            "contents": [{
                "parts": [{
                    "text": f"You are a professional assistant, skilled in composing detailed and accurate news articles from multiple sources.\n\n{content}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096,
                "topP": 0.95,
                "topK": 64
            }
        }
    
    def call_api(self, content: str, model: str) -> Optional[str]:
        """Make API call to Gemini and return processed response."""
        try:
            # Truncate content if it's too long
            truncated_content = truncate_content(content, MAX_TOKENS)
            
            # Format URL with model and API key
            url = self.api_url.format(model=model)
            if '?' in url:
                url += f"&key={self.api_key}"
            else:
                url += f"?key={self.api_key}"
            
            data = self.format_messages(truncated_content)
            
            response = self.session.post(
                url,
                headers=self.get_headers(),
                json=data
            )
            
            if response.status_code == 429:  # Rate limit exceeded
                retry_after = self.handle_rate_limit(response)
                if retry_after:
                    logger.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                    return self.call_api(content, model)
                    
            response.raise_for_status()
            return self.parse_response(response.json())
            
        except Exception as e:
            logger.error(f"Gemini API request failed: {str(e)}")
            if 'response' in locals():
                logger.error(f"Response content: {response.text}")
            return None
    
    def parse_response(self, response: Dict[str, Any]) -> Optional[str]:
        """Parse Gemini API response and extract content."""
        try:
            candidates = response.get('candidates', [])
            if candidates:
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if parts:
                    return parts[0].get('text', '')
            return None
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return None

def estimate_token_count(text: str) -> int:
    """Estimate the number of tokens in a text."""
    return len(text) // 4

def truncate_content(content: str, max_tokens: int) -> str:
    """Truncate the content to fit within the maximum token limit."""
    tokens = content.split()
    truncated_content = []
    current_tokens = 0

    for token in tokens:
        current_tokens += len(token) // 4
        if current_tokens > max_tokens:
            break
        truncated_content.append(token)

    return ' '.join(truncated_content)

def ensure_proper_punctuation(text: str) -> str:
    """Ensure proper punctuation in the text."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    corrected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        corrected_sentences.append(sentence)

    return ' '.join(corrected_sentences)

def read_content_prefix(prefix_file_path: str) -> str:
    """Read content prefix from a file."""
    try:
        with open(prefix_file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (IOError, FileNotFoundError) as e:
        logger.error(f"Error reading content prefix file {prefix_file_path}: {e}")
        return ""

def process_json_file(filepath: str, api_config: Dict[str, Any], content_prefix: str, 
                     rewritten_folder: str) -> None:
    """Process a JSON file using the specified API."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            
        if isinstance(json_data, dict):
            json_data = [json_data]
        elif isinstance(json_data, str):
            logger.error(f"Expected list of dictionaries but got a string. File: {filepath}")
            return
            
        combined_content = content_prefix + "\n".join(
            f"[source {idx + 1}] {item.get('content', 'No content provided')}"
            for idx, item in enumerate(json_data)
        )

        if estimate_token_count(combined_content) > MAX_TOKENS:
            combined_content = truncate_content(combined_content, MAX_TOKENS)

        # Create appropriate API client
        client = APIClientFactory.create_client(
            provider=api_config['provider'],
            api_key=api_config['api_key'],
            api_url=api_config.get('api_url')
        )

        rewritten_content = client.call_api(combined_content, api_config['model'])

        if rewritten_content:
            save_rewritten_content(
                rewritten_content,
                json_data,
                filepath,
                rewritten_folder,
                api_config
            )
        else:
            logger.error("Failed to get rewritten content from API.")

    except Exception as e:
        logger.error(f"Error processing file {filepath}: {str(e)}")

def save_rewritten_content(content: str, original_data: List[Dict], filepath: str,
                         rewritten_folder: str, api_config: Dict[str, Any]) -> None:
    """Save the rewritten content to a new JSON file."""
    cleaned_content = re.sub(r'\*\*', '', content)
    cleaned_content = re.sub(r'\n\n+', ' ', cleaned_content)
    cleaned_content = re.sub(r'Fonti:.*$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'Fonte:.*$', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = ensure_proper_punctuation(cleaned_content)

    links = [item.get('link') for item in original_data if 'link' in item]

    new_data = {
        'title': original_data[0].get('title', 'No Title'),
        'content': cleaned_content,
        'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'links': links,
        'api': api_config['provider'],
        'model': api_config['model']
    }

    new_filename = Path(rewritten_folder) / (Path(filepath).stem + '_rewritten.json')
    try:
        with open(new_filename, 'w', encoding='utf-8') as outfile:
            json.dump(new_data, outfile, ensure_ascii=False, indent=4)
        logger.info(f"Rewritten file saved to {new_filename}")
    except IOError as e:
        logger.error(f"Error writing to {new_filename}: {e}")

def validate_config(api_config: Dict[str, Any]) -> None:
    """Validate the API configuration."""
    provider = api_config.get('provider', '').lower()
    
    # Check required keys based on provider
    if provider == 'ollama':
        # Ollama doesn't require API key
        required_keys = ['provider', 'model']
    else:
        # All other providers require API key
        required_keys = ['provider', 'api_key', 'model']
    
    missing_keys = [key for key in required_keys if not api_config.get(key)]
    
    if missing_keys:
        raise ValueError(f"Missing required configuration keys for {provider}: {', '.join(missing_keys)}")
    
    # Additional validation for specific providers
    if provider == 'gemini' and not api_config.get('api_key'):
        raise ValueError("Gemini API requires an API key")
    
    if provider == 'anthropic' and not api_config.get('api_key'):
        raise ValueError("Anthropic API requires an API key")
        
    if provider == 'openai' and not api_config.get('api_key'):
        raise ValueError("OpenAI API requires an API key")
        
    if provider == 'groq' and not api_config.get('api_key'):
        raise ValueError("Groq API requires an API key")

def map_api_config(config_api_config: Dict[str, Any]) -> Dict[str, Any]:
    """Map configuration from GUI format to processor format."""
    selected_api = config_api_config.get('selected_api', '').lower()
    
    # Mapping from GUI selected_api to internal provider names and their config keys
    api_mappings = {
        'openai': {
            'provider': 'openai',
            'api_key': config_api_config.get('openai_api_key'),
            'model': config_api_config.get('openai_model'),
            'api_url': config_api_config.get('openai_api_url')
        },
        'groq': {
            'provider': 'groq',
            'api_key': config_api_config.get('groq_api_key'),
            'model': config_api_config.get('groq_model'),
            'api_url': config_api_config.get('groq_api_url')
        },
        'anthropic': {
            'provider': 'anthropic',
            'api_key': config_api_config.get('anthropic_api_key'),
            'model': config_api_config.get('anthropic_model'),
            'api_url': config_api_config.get('anthropic_api_url')
        },
        'ollama': {
            'provider': 'ollama',
            'api_key': '',  # Ollama doesn't need API key
            'model': config_api_config.get('ollama_model'),
            'api_url': config_api_config.get('ollama_api_url')
        },
        'gemini': {
            'provider': 'gemini',
            'api_key': config_api_config.get('gemini_api_key'),
            'model': config_api_config.get('gemini_model'),
            'api_url': config_api_config.get('gemini_api_url')
        }
    }
    
    if selected_api in api_mappings:
        return api_mappings[selected_api]
    else:
        # Fallback for legacy configs or direct provider specification
        return {
            'provider': config_api_config.get('provider', selected_api),
            'api_key': config_api_config.get('api_key', ''),
            'model': config_api_config.get('model', ''),
            'api_url': config_api_config.get('api_url')
        }


def main(config_path: str, prompt_path: Optional[str] = None, api: Optional[str] = None,
         api_key: Optional[str] = None, model: Optional[str] = None, 
         api_url: Optional[str] = None, output_folder: Optional[str] = None,
         rewritten_folder: Optional[str] = None) -> None:
    """Main function to process JSON files with LLM API."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        logger.error(f"Error reading config file {config_path}: {e}")
        return

    api_config = config.get('api_config', {})
    folder_config = config.get('folders', {})
    prompt_file_path = prompt_path or config.get('prompt_file', "")

    # Map API configuration from GUI format to processor format
    mapped_api_config = map_api_config(api_config)

    # Override with environment variables and CLI arguments
    mapped_api_config.update({
        'provider': api or os.getenv('API_TYPE', mapped_api_config.get('provider')),
        'api_key': api_key or os.getenv('API_KEY', mapped_api_config.get('api_key')),
        'model': model or os.getenv('API_MODEL', mapped_api_config.get('model')),
        'api_url': api_url or os.getenv('API_URL', mapped_api_config.get('api_url'))
    })

    # Set up folders
    output_folder = output_folder or os.getenv('OUTPUT_FOLDER', folder_config.get('output_folder', 'output'))
    rewritten_folder = rewritten_folder or os.getenv('REWRITTEN_FOLDER', folder_config.get('rewritten_folder', 'rewritten'))
    
    # Get content prefix
    prompt_file_path = prompt_path or os.getenv('PROMPT_FILE', prompt_file_path)
    content_prefix = read_content_prefix(prompt_file_path) if prompt_file_path else config.get('content_prefix', "")

    try:
        # Validate configuration
        validate_config(mapped_api_config)

        # Create rewritten folder if it doesn't exist
        Path(rewritten_folder).mkdir(parents=True, exist_ok=True)

        # Process all JSON files in the output folder
        json_files = list(Path(output_folder).glob('*.json'))
        if not json_files:
            logger.warning(f"No JSON files found in {output_folder}")
            return

        for json_file in json_files:
            logger.info(f"Processing file: {json_file}")
            process_json_file(
                filepath=str(json_file),
                api_config=mapped_api_config,
                content_prefix=content_prefix,
                rewritten_folder=rewritten_folder
            )

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files with LLM API')
    parser.add_argument('--config', type=str, default='config.yaml',
                      help='Path to the configuration YAML file (default: config.yaml)')
    parser.add_argument('--prompt', type=str,
                      help='Path to the prompt file')
    parser.add_argument('--api', type=str,
                      help='API provider (OpenAI, Azure, Anthropic, Groq, Ollama, Together, Mistral, Gemini)')
    parser.add_argument('--api_key', type=str,
                      help='API key for the selected provider')
    parser.add_argument('--model', type=str,
                      help='Model to use for the selected provider')
    parser.add_argument('--api_url', type=str,
                      help='API URL for the selected provider')
    parser.add_argument('--output_folder', type=str,
                      help='Output folder containing JSON files to process')
    parser.add_argument('--rewritten_folder', type=str,
                      help='Folder to save the rewritten JSON files')

    args = parser.parse_args()

    try:
        main(
            config_path=args.config,
            prompt_path=args.prompt,
            api=args.api,
            api_key=args.api_key,
            model=args.model,
            api_url=args.api_url,
            output_folder=args.output_folder,
            rewritten_folder=args.rewritten_folder
        )
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
