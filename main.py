import os
import argparse
import time
import yaml
import logging
import sys
import feedparser
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from tqdm import tqdm
import nltk
from langdetect import detect
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
from typing import List, Dict, Any
from logging_setup import setup_logging

# Setup logging
logger = setup_logging()

# Download NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            logger.info(f"Loading configuration from {config_path}")
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_path}: {e}")
        sys.exit(1)

def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        logger.info(f"Creating missing directory: {directory}")
        os.makedirs(directory)

def get_env_variable(key, default=None):
    """Retrieve environment variable or use default if not set."""
    value = os.getenv(key.upper(), default)
    if value is None:
        logger.info(f"Environment variable {key.upper()} is not set; using default value.")
    return value

def merge_configs(yaml_config, env_config, cli_config):
    """Merge configurations with priority: CLI > ENV > YAML."""
    final_config = yaml_config.copy()

    # Update with environment variables if they are set
    for key, value in env_config.items():
        if value is not None:
            final_config[key] = value

    # Update with command-line arguments if they are set
    for key, value in cli_config.items():
        if value is not None:
            final_config[key] = value

    return final_config

def fetch_feeds_from_file(file_path: str) -> List[Dict]:
    """Fetch and parse RSS feeds from a file containing URLs."""
    articles = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [url.strip() for url in file.readlines()]

        for url in urls:
            logger.info(f"Fetching feed from {url}")
            feed = feedparser.parse(url)
            articles.extend([{
                'title': entry.title,
                'content': entry.description if hasattr(entry, 'description') else '',
                'link': entry.link
            } for entry in feed.entries])

        logger.info(f"Total articles fetched and parsed: {len(articles)}")
    except Exception as e:
        logger.error(f"Error fetching feeds: {e}")

    return articles

def detect_language(text: str) -> str:
    """Detect the language of a given text."""
    try:
        return detect(text)
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return 'unknown'

def preprocess_text(text: str, language: str, config: dict) -> str:
    """Preprocess the text based on the configuration settings and language."""
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer(language if language in SnowballStemmer.languages else 'english')

    if config.get('remove_html', True):
        text = re.sub(r"<[^<]+?>", "", text)  # Remove HTML tags
    if config.get('lowercase', True):
        text = text.lower()
    if config.get('remove_punctuation', True):
        text = re.sub(r'[^\w\s]', '', text)

    tokens = text.split()
    if config.get('lemmatization', True):
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
    if config.get('use_stemming', False):
        tokens = [stemmer.stem(word) for word in tokens]

    stop_words = set(stopwords.words(language if language in stopwords.fileids() else 'english'))
    additional_stopwords = set(config.get('additional_stopwords', []))
    tokens = [word for word in tokens if word not in stop_words and word not in additional_stopwords]

    preprocessed_text = " ".join(tokens)
    return preprocessed_text

def vectorize_texts(texts: List[str], config: Dict[str, Any]) -> Any:
    """Vectorize texts based on the specified method in the configuration."""
    vectorizer_params = {
        'ngram_range': tuple(config.get('ngram_range', [1, 2])),
        'max_df': config.get('max_df', 0.85),
        'min_df': config.get('min_df', 0.01),
        'max_features': config.get('max_features', None)
    }

    method = config.get('method', 'tfidf').lower()
    if method == 'tfidf':
        vectorizer = TfidfVectorizer(**vectorizer_params)
    elif method == 'count':
        vectorizer = CountVectorizer(**vectorizer_params)
    elif method == 'hashing':
        vectorizer = HashingVectorizer(ngram_range=vectorizer_params['ngram_range'])
    else:
        raise ValueError(f"Unsupported vectorization method: {method}")

    vectors = vectorizer.fit_transform(texts)
    return vectors

def cluster_texts(vectors: Any, config: Dict[str, Any]) -> np.ndarray:
    """Cluster texts using the specified clustering method in the configuration."""
    method = config.get('method', 'dbscan').lower()

    if method == 'dbscan':
        clustering = DBSCAN(
            metric='precomputed',
            eps=config.get('eps', 0.5),
            min_samples=config.get('min_samples', 2)
        )
        cosine_sim_matrix = cosine_similarity(vectors)
        distance_matrix = np.maximum(1 - cosine_sim_matrix, 0)
        labels = clustering.fit_predict(distance_matrix)
    elif method == 'kmeans':
        clustering = KMeans(
            n_clusters=config.get('n_clusters', 5)
        )
        labels = clustering.fit_predict(vectors.toarray())
    elif method == 'agglomerative':
        clustering = AgglomerativeClustering(
            n_clusters=config.get('n_clusters', 5),
            linkage=config.get('linkage', 'average')
        )
        labels = clustering.fit_predict(vectors.toarray())
    else:
        raise ValueError(f"Unsupported clustering method: {method}")

    return labels

def aggregate_similar_articles(articles: List[Dict[str, str]], similarity_matrix: np.ndarray, threshold: float) -> List[List[Dict[str, str]]]:
    """Aggregate articles into groups based on similarity matrix and threshold."""
    clustering = AgglomerativeClustering(
        metric='precomputed',  # Updated from 'affinity' to 'metric'
        linkage='average',
        distance_threshold=threshold,
        n_clusters=None
    )
    labels = clustering.fit_predict(1 - similarity_matrix)

    grouped_articles = []
    for label in set(labels):
        group = [articles[i] for i in range(len(articles)) if labels[i] == label]
        grouped_articles.append(group)

    return grouped_articles

def save_grouped_articles(grouped_articles: List[List[Dict]], output_dir: str) -> None:
    """Save grouped articles to JSON files."""
    ensure_directory_exists(output_dir)
    for i, group in enumerate(grouped_articles):
        if len(group) > 1:  # Only save groups with more than one article
            filename = f"group_{i}.json"
            file_path = os.path.join(output_dir, filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(group, file, ensure_ascii=False, indent=4)
                logger.info(f"Saved group {i} with {len(group)} articles to {file_path}")
            except Exception as e:
                logger.error(f"Error saving group {i} to JSON: {e}")

def main(config: dict):
    """Main function to process RSS feeds and group similar articles."""
    logger.info("Starting RSS feed processing...")
    input_file_path = 'input/feeds.txt'
    output_directory = config.get('output', {}).get('output_dir', 'output')
    start_time = time.time()

    logger.info("Ensuring output directory exists...")
    ensure_directory_exists(output_directory)

    try:
        logger.info("Fetching and parsing RSS feeds...")
        articles = fetch_feeds_from_file(input_file_path)
        logger.info(f"Total articles fetched and parsed: {len(articles)}")
    except Exception as e:
        logger.error(f"Error fetching or parsing RSS feeds: {e}")
        return

    logger.info("Preprocessing texts...")
    languages = [detect_language(f"{article['title']} {article['content']}") for article in articles]
    preprocessed_texts = [
        preprocess_text(f"{article['title']} {article['content']}", lang, config.get('preprocessing', {}))
        for article, lang in zip(articles, languages)
    ]

    logger.info("Vectorizing texts...")
    vectors = vectorize_texts(preprocessed_texts, config.get('vectorization', {}))

    logger.info("Computing similarity matrix...")
    similarity_matrix = cosine_similarity(vectors)

    logger.info("Clustering texts...")
    grouped_articles = aggregate_similar_articles(articles, similarity_matrix, config.get('similarity_threshold', 0.66))

    logger.info("Saving grouped articles to JSON files...")
    save_grouped_articles(grouped_articles, output_directory)

    elapsed_time = time.time() - start_time
    logger.info(f"RSS feed processing complete in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process RSS feeds and group similar articles based on a similarity threshold.'
    )
    parser.add_argument(
        '-c', '--config', type=str, default='config.yaml',
        help='Path to the configuration file (default: config.yaml).'
    )
    parser.add_argument(
        '--similarity_threshold', type=float, help='Similarity threshold for grouping articles.'
    )
    parser.add_argument(
        '--min_samples', type=int, help='Minimum number of samples for DBSCAN clustering.'
    )
    parser.add_argument(
        '--eps', type=float, help='Maximum distance between samples for one to be considered as in the neighborhood of the other in DBSCAN.'
    )
    parser.add_argument(
        '--output_dir', type=str, help='Output directory for saving grouped articles.'
    )
    args = parser.parse_args()

    # Load default configuration from the YAML file
    yaml_config = load_config(args.config)

    # Override with environment variables if they exist
    env_config = {
        'similarity_threshold': float(get_env_variable('SIMILARITY_THRESHOLD', yaml_config.get('similarity_threshold'))),
        'min_samples': int(get_env_variable('MIN_SAMPLES', yaml_config.get('similarity_options', {}).get('min_samples', None))),
        'eps': float(get_env_variable('EPS', yaml_config.get('similarity_options', {}).get('eps', None))),
        'output_dir': get_env_variable('OUTPUT_DIR', yaml_config.get('output', {}).get('output_dir', 'output'))
    }

    # Override with command-line arguments if provided
    cli_config = {
        'similarity_threshold': args.similarity_threshold,
        'min_samples': args.min_samples,
        'eps': args.eps,
        'output_dir': args.output_dir
    }

    # Merge all configurations with priority: CLI > ENV > YAML
    final_config = merge_configs(yaml_config, env_config, cli_config)

    # Update config dictionary with merged options
    if 'similarity_options' not in final_config:
        final_config['similarity_options'] = {}
    final_config['similarity_options']['min_samples'] = final_config.pop('min_samples', None)
    final_config['similarity_options']['eps'] = final_config.pop('eps', None)
    if 'output' not in final_config:
        final_config['output'] = {}
    final_config['output']['output_dir'] = final_config.pop('output_dir', 'output')

    # Run the main function with the final merged configuration
    main(final_config)
