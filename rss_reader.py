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
import numpy as np
from tqdm import tqdm
import feedparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TAG_RE = re.compile(r"<[^<]+?>")

def fetch_feeds_from_file(file_path: str) -> List[Dict]:
    """Fetch and parse RSS feeds from a file containing URLs with progress display."""
    articles = []
    with open(file_path, 'r') as file:
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

def calculate_similarity(articles: List[Dict]) -> float:
    """Calculate the average pairwise cosine similarity of articles based on content."""
    if len(articles) < 2:
        return 0.0
    texts = [f"{article['title']} {article['content']}" for article in articles]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix)
    return np.tril(cosine_sim_matrix, -1).sum() / (len(articles) * (len(articles) - 1) / 2)

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
    unique_articles = [article for article in articles if hashlib.md5((article['title'] + article['content']).encode()).hexdigest() not in seen_articles]
    seen_articles.update({hashlib.md5((article['title'] + article['content']).encode()).hexdigest() for article in unique_articles})

    if unique_articles:
        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y%m%d_%H%M')}_{sanitize_filename(generate_title(unique_articles))}_Q{len(unique_articles)}_S{calculate_similarity(unique_articles):.2f}.json"
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(unique_articles, file, ensure_ascii=False, indent=4)
            logging.info(f"Saved {file_path} with {len(unique_articles)} items.")
        except IOError as e:
            logging.error(f"Failed to save {file_path}: {e}")

def save_grouped_articles(articles_groups: List[List[Dict]], directory: str) -> List[int]:
    """Save groups of articles to JSON files."""
    seen_articles = set()
    group_sizes = []
    for group in tqdm(articles_groups, desc="Saving groups"):
        if len(group) > 2:
            save_articles_to_json(group, directory, seen_articles)
            group_sizes.append(len(group))
    return group_sizes
