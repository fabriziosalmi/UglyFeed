import json
import os
import re
import datetime
import logging
import hashlib
from typing import List, Dict
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import numpy as np
from tqdm import tqdm
import feedparser
from joblib import Parallel, delayed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TAG_RE = re.compile(r"<[^<]+?>")


def fetch_feeds_from_file(file_path: str) -> List[Dict]:
    """Fetch and parse RSS feeds from a file containing URLs with progress display."""
    articles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for url in tqdm(urls, desc="Fetching and parsing RSS feeds"):
        feed = feedparser.parse(url.strip())
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'content': entry.description if hasattr(entry, 'description') else '',
                'link': entry.link
            })
    return articles


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters and spaces from filenames."""
    return re.sub(r'[<>:"/\\|?*\n\r\']+', '', filename).replace(',', '_').replace(' ', '_')


def generate_title(articles: List[Dict]) -> str:
    """Generate a title based on the most common significant words in article titles."""
    title_words = [word.lower() for article in articles for word in article['title'].split()]
    word_counts = Counter(title_words)
    significant_words = [word for word, count in word_counts.most_common(10) if len(word) > 3][:3]
    return ' '.join(significant_words)


def concatenate_article(article: Dict[str, str]) -> str:
    """Concatenate title and content of an article."""
    return f"{article['title']} {article['content']}"


def compute_tfidf(texts: List[str]) -> np.ndarray:
    """Compute the TF-IDF matrix for a list of texts."""
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(texts)


def calculate_pairwise_similarities(tfidf_matrix: np.ndarray) -> np.ndarray:
    """Calculate the cosine similarity matrix for the TF-IDF matrix."""
    return cosine_similarity(tfidf_matrix)


def cluster_articles(cosine_sim_matrix: np.ndarray) -> List[int]:
    """Cluster articles using DBSCAN based on the cosine similarity matrix."""
    clustering = DBSCAN(metric='precomputed', min_samples=2, eps=0.5).fit(1 - cosine_sim_matrix)
    return clustering.labels_


def merge_cluster_articles(cluster_labels: List[int], articles: List[Dict[str, str]]) -> List[str]:
    """Merge articles within each cluster."""
    cluster_dict = {}
    for label, article in zip(cluster_labels, articles):
        if label == -1:  # Noise points, keep them as separate articles
            cluster_dict[len(cluster_dict)] = [concatenate_article(article)]
        else:
            if label not in cluster_dict:
                cluster_dict[label] = []
            cluster_dict[label].append(concatenate_article(article))

    merged_texts = [" ".join(cluster) for cluster in cluster_dict.values()]
    return merged_texts


def calculate_average_similarity(merged_texts: List[str]) -> float:
    """Calculate the average pairwise cosine similarity of merged texts."""
    if len(merged_texts) <= 1:
        return 0.0

    tfidf_matrix = compute_tfidf(merged_texts)
    cosine_sim_matrix = calculate_pairwise_similarities(tfidf_matrix)

    tril_indices = np.tril_indices_from(cosine_sim_matrix, -1)
    similarities = cosine_sim_matrix[tril_indices]

    num_comparisons = len(similarities)
    return np.sum(similarities) / num_comparisons if num_comparisons > 0 else 0.0


def calculate_similarity(articles: List[Dict[str, str]]) -> float:
    """
    Calculate the average pairwise cosine similarity of articles, merging those that tell the same fact.

    Parameters:
    articles (List[Dict[str, str]]): A list of dictionaries, where each dictionary represents an article
                                     with 'title' and 'content' keys.

    Returns:
    float: The average pairwise cosine similarity of the merged articles.
    """
    if not articles or len(articles) <= 1:
        return 0.0

    try:
        # Concatenate title and content for each article in parallel
        texts = Parallel(n_jobs=-1)(delayed(concatenate_article)(article) for article in articles)

        # Compute the TF-IDF matrix
        tfidf_matrix = compute_tfidf(texts)

        # Compute the cosine similarity matrix
        cosine_sim_matrix = calculate_pairwise_similarities(tfidf_matrix)

        # Cluster articles
        cluster_labels = cluster_articles(cosine_sim_matrix)

        # Merge articles in clusters
        merged_texts = merge_cluster_articles(cluster_labels, articles)

        # Compute the average similarity of merged texts
        average_similarity = calculate_average_similarity(merged_texts)

        return average_similarity
    except Exception as e:
        logging.error("An error occurred while calculating similarity: %s", e)
        return 0.0


def process_article(article: Dict) -> Dict:
    """Remove HTML tags and unwanted fields from articles."""
    article_copy = article.copy()
    article_copy['title'] = TAG_RE.sub("", article['title'])
    article_copy['content'] = TAG_RE.sub("", article['content'])
    article_copy.pop('time', None)
    return article_copy


def save_articles_to_json(articles: List[Dict], directory: str, seen_articles: set) -> None:
    """Save unique articles to a JSON file."""
    os.makedirs(directory, exist_ok=True)
    unique_articles = [
        article for article in articles if hashlib.md5(
            (article['title'] + article['content']).encode()).hexdigest() not in seen_articles
    ]
    seen_articles.update({
        hashlib.md5((article['title'] + article['content']).encode()).hexdigest() for article in unique_articles
    })

    if unique_articles:
        now = datetime.datetime.now()
        filename = (
            f"{now.strftime('%Y%m%d_%H%M')}_{sanitize_filename(generate_title(unique_articles))}_Q"
            f"{len(unique_articles)}_S{calculate_similarity(unique_articles):.2f}.json"
        )
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(unique_articles, file, ensure_ascii=False, indent=4)
            logging.info("Saved %s with %d items.", file_path, len(unique_articles))
        except IOError as e:
            logging.error("Failed to save %s: %s", file_path, e)


def save_grouped_articles(articles_groups: List[List[Dict]], directory: str) -> List[int]:
    """Save groups of articles to JSON files."""
    seen_articles = set()
    group_sizes = []
    for group in tqdm(articles_groups, desc="Saving groups"):
        if len(group) > 2:
            save_articles_to_json(group, directory, seen_articles)
            group_sizes.append(len(group))
    return group_sizes
