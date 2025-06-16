"""
This script processes RSS feeds and groups similar articles based on a similarity threshold.
"""

import os
import argparse
import time
import sys
import json
import re


from typing import List, Dict, Any, Optional, Tuple
import yaml
import feedparser
import numpy as np
import nltk
from langdetect import detect

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
from logging_setup import setup_logging

# Setup logging
logger = setup_logging()

# Download NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            logger.info("Loading configuration from %s", config_path)
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error("YAML error loading configuration from %s: %s", config_path, e)
        sys.exit(1)
    except Exception as e:
        logger.error("Error loading configuration from %s: %s", config_path, e)
        sys.exit(1)


def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        logger.info("Creating missing directory: %s", directory)
        os.makedirs(directory)


def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve environment variable or use default if not set."""
    value = os.getenv(key.upper(), default)
    if value is None:
        logger.info("Environment variable %s is not set; using default value.", key.upper())
    return value


def merge_configs(yaml_cfg: Dict[str, Any], env_cfg: Dict[str, Any], cli_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Merge configurations with priority: CLI > ENV > YAML."""

    def update_recursive(d: Dict[str, Any], u: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = update_recursive(d.get(k, {}), v)
            elif v is not None:
                d[k] = v
        return d

    final_config = yaml_cfg.copy()
    final_config = update_recursive(final_config, env_cfg)
    final_config = update_recursive(final_config, cli_cfg)

    return final_config


def fetch_feeds_from_file(file_path: str) -> List[Dict[str, str]]:
    """Fetch and parse RSS feeds from a file containing URLs with enhanced error handling."""
    articles = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]

        if not urls:
            logger.warning("No URLs found in %s", file_path)
            return articles

        logger.info("Found %d URLs to process", len(urls))

        for i, url in enumerate(urls, 1):
            logger.info("Fetching feed %d/%d from %s", i, len(urls), url)
            try:
                feed = feedparser.parse(url)
                
                # Check if feed parsing was successful
                if feed.bozo:
                    logger.warning("Feed %s has parsing warnings: %s", url, feed.bozo_exception)
                
                if not feed.entries:
                    logger.warning("No entries found in feed: %s", url)
                    continue
                
                # Extract articles with better error handling
                feed_articles = []
                for entry in feed.entries:
                    title = getattr(entry, 'title', '')
                    description = getattr(entry, 'description', '') or getattr(entry, 'summary', '')
                    link = getattr(entry, 'link', '')
                    
                    # Skip entries with missing critical data
                    if not title and not description:
                        logger.warning("Skipping entry with no title or description from %s", url)
                        continue
                    
                    # Use fallback values for missing data
                    article = {
                        'title': title or 'No Title',
                        'content': description or 'No Content',
                        'link': link or url
                    }
                    feed_articles.append(article)
                
                articles.extend(feed_articles)
                logger.info("Successfully fetched %d articles from %s", len(feed_articles), url)
                
            except Exception as e:
                logger.error("Failed to fetch feed from %s: %s", url, e)
                continue

        logger.info("Total articles fetched and parsed: %d", len(articles))
        
        if len(articles) == 0:
            logger.error("CRITICAL: No articles were fetched from any feeds! This will cause 'No Title' issues.")
            logger.error("Please check your RSS feed URLs using: python tools/rss_debug.py %s", file_path)
            
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
    except Exception as e:
        logger.error("Error fetching feeds: %s", e)

    return articles


def detect_language(text: str) -> str:
    """Detect the language of a given text."""
    try:
        return detect(text)
    except Exception as e:
        logger.warning("Language detection failed: %s", e)
        return 'unknown'


def preprocess_text(text: str, language: str, config: Dict[str, Any]) -> str:
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


def aggregate_similar_articles(articles: List[Dict[str, str]], similarity_matrix: np.ndarray, threshold: float) -> List[Tuple[List[Dict[str, str]], float]]:
    """Aggregate articles into groups based on similarity matrix and threshold."""
    clustering = AgglomerativeClustering(
        metric='precomputed',
        linkage='average',
        distance_threshold=threshold,
        n_clusters=None
    )
    labels = clustering.fit_predict(1 - similarity_matrix)

    grouped_articles_with_scores = []
    for label in set(labels):
        group = [articles[i] for i in range(len(articles)) if labels[i] == label]
        group_similarities = [similarity_matrix[i][j] for i in range(len(articles)) for j in range(len(articles)) if labels[i] == label and labels[j] == label and i != j]
        average_similarity = np.mean(group_similarities) if group_similarities else 0
        grouped_articles_with_scores.append((group, average_similarity))

    return grouped_articles_with_scores


def save_grouped_articles(grouped_articles_with_scores: List[Tuple[List[Dict[str, str]], float]], output_dir: str) -> int:
    """Save grouped articles to JSON files and return the number of saved files."""
    ensure_directory_exists(output_dir)
    saved_files_count = 0
    for i, (group, avg_similarity) in enumerate(grouped_articles_with_scores):
        if len(group) > 1:  # Only save groups with more than one article
            filename = f"group_{i}.json"
            file_path = os.path.join(output_dir, filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump({'articles': group, 'average_similarity': avg_similarity}, file, ensure_ascii=False, indent=4)
                logger.info("Group %d: Saved %d articles to %s, Avg Similarity: %.2f", i, len(group), file_path, avg_similarity)
                saved_files_count += 1
            except Exception as e:
                logger.error("Error saving group %d to JSON: %s", i, e)
    return saved_files_count


def deduplicate_articles(articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate articles based on content and link."""
    seen = set()
    unique_articles = []
    for article in articles:
        identifier = (article['content'], article['link'])
        if identifier not in seen:
            seen.add(identifier)
            unique_articles.append(article)
    logger.info("Total unique articles after deduplication: %d", len(unique_articles))
    return unique_articles


def main(config: Dict[str, Any]) -> None:
    """Main function to process RSS feeds and group similar articles."""
    logger.info("Starting RSS feed processing...")
    input_feeds_path = config.get('input_feeds_path', 'input/feeds.txt')
    output_directory = config.get('output', {}).get('output_dir', 'output')
    start_time = time.time()

    logger.info("Ensuring output directory exists...")
    ensure_directory_exists(output_directory)

    try:
        logger.info("Fetching and parsing RSS feeds...")
        articles = fetch_feeds_from_file(input_feeds_path)
        logger.info("Total articles fetched and parsed: %d", len(articles))

        logger.info("Deduplicating articles...")
        articles = deduplicate_articles(articles)
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        return
    except Exception as e:
        logger.error("Error fetching or parsing RSS feeds: %s", e)
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
    grouped_articles_with_scores = aggregate_similar_articles(articles, similarity_matrix, config.get('similarity_threshold', 0.66))

    logger.info("Saving grouped articles to JSON files...")
    saved_files_count = save_grouped_articles(grouped_articles_with_scores, output_directory)
    logger.info("Total number of JSON files generated: %d", saved_files_count)

    elapsed_time = time.time() - start_time
    logger.info("RSS feed processing complete in %.2f seconds", elapsed_time)


def build_env_config(yaml_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Build configuration from environment variables."""
    env_config = {}
    for key, value in yaml_cfg.items():
        if isinstance(value, dict):
            env_config[key] = build_env_config(value)
        else:
            env_key = key.upper()
            env_value = get_env_variable(env_key, value)
            env_config[key] = type(value)(env_value) if env_value is not None else value
    return env_config


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
    parser.add_argument(
        '--input_feeds_path', type=str, help='Path to the input file containing RSS feed URLs.'
    )
    args = parser.parse_args()

    # Load default configuration from the YAML file
    yaml_cfg = load_config(args.config)

    # Build environment configuration based on environment variables
    env_cfg = build_env_config(yaml_cfg)

    # Override with command-line arguments if provided
    cli_cfg = {
        'similarity_threshold': args.similarity_threshold,
        'min_samples': args.min_samples,
        'eps': args.eps,
        'output': {'output_dir': args.output_dir},
        'input_feeds_path': args.input_feeds_path
    }

    # Merge all configurations with priority: CLI > ENV > YAML
    final_cfg = merge_configs(yaml_cfg, env_cfg, cli_cfg)

    # Run the main function with the final merged configuration
    main(final_cfg)
