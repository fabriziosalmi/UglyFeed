# Script Documentation

## Introduction
This script, used by `main.py`, contains functions for fetching and processing RSS feeds, clustering similar articles, and saving grouped articles into JSON files. It leverages parallel processing to enhance performance and uses clustering algorithms to group articles based on their similarity.

## Input/Output

### Input
- **RSS Feeds File**: A text file containing URLs of RSS feeds, one URL per line.
- **Articles**: A list of article dictionaries to be processed and grouped.

### Output
- **Grouped Articles**: JSON files saved in the specified output directory, each containing a group of similar articles.

## Functionality

### Features
1. **RSS Feeds Fetching**: Fetches and parses RSS feeds from a file containing URLs.
2. **Filename Sanitization**: Removes invalid characters from filenames.
3. **Title Generation**: Generates a group title based on the most common words in article titles.
4. **Article Concatenation**: Combines title and content of articles for processing.
5. **TF-IDF Computation**: Converts text data into TF-IDF features for similarity calculations.
6. **Cosine Similarity Calculation**: Computes the cosine similarity matrix for articles.
7. **Clustering**: Uses DBSCAN clustering to group similar articles.
8. **Similarity Calculation**: Calculates the average pairwise cosine similarity of articles.
9. **Article Processing**: Cleans up articles by removing HTML tags and unwanted fields.
10. **JSON Saving**: Saves unique articles into JSON files with informative filenames.

## Code Structure

### Imports
```python
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
```
- **json**: For reading and writing JSON files.
- **os**: For file and directory operations.
- **re**: For regular expressions.
- **datetime**: For date and time operations.
- **logging**: For logging information and errors.
- **hashlib**: For generating MD5 hashes.
- **typing**: For type annotations.
- **collections.Counter**: For counting word occurrences.
- **sklearn.feature_extraction.text.TfidfVectorizer**: For transforming text data into TF-IDF features.
- **sklearn.metrics.pairwise.cosine_similarity**: For calculating cosine similarity.
- **sklearn.cluster.DBSCAN**: For clustering articles.
- **numpy**: For numerical operations.
- **tqdm**: For displaying progress bars.
- **feedparser**: For parsing RSS feeds.
- **joblib**: For parallel processing.

### Logging Configuration
```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
Configures logging to display informational messages with timestamps.

### HTML Tag Removal Regex
```python
TAG_RE = re.compile(r"<[^<]+?>")
```
Defines a regular expression to remove HTML tags from strings.

### Fetching and Parsing RSS Feeds
```python
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
```
Fetches and parses RSS feeds from a file containing URLs, returning a list of article dictionaries.

### Filename Sanitization
```python
def sanitize_filename(filename: str) -> str:
    """Remove invalid characters and spaces from filenames."""
    return re.sub(r'[<>:"/\\|?*\n\r\']+', '', filename).replace(',', '_').replace(' ', '_')
```
Removes invalid characters from filenames to ensure they are safe to use.

### Title Generation
```python
def generate_title(articles: List[Dict]) -> str:
    """Generate a title based on the most common significant words in article titles."""
    title_words = [word.lower() for article in articles for word in article['title'].split()]
    word_counts = Counter(title_words)
    significant_words = [word for word, count in word_counts.most_common(10) if len(word) > 3][:3]
    return ' '.join(significant_words)
```
Generates a title for a group of articles based on the most common significant words in their titles.

### Article Concatenation
```python
def concatenate_article(article: Dict[str, str]) -> str:
    """Concatenate title and content of an article."""
    return f"{article['title']} {article['content']}"
```
Concatenates the title and content of an article into a single string.

### TF-IDF Computation
```python
def compute_tfidf(texts: List[str]) -> np.ndarray:
    """Compute the TF-IDF matrix for a list of texts."""
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(texts)
```
Converts a list of texts into a TF-IDF matrix.

### Cosine Similarity Calculation
```python
def calculate_pairwise_similarities(tfidf_matrix: np.ndarray) -> np.ndarray:
    """Calculate the cosine similarity matrix for the TF-IDF matrix."""
    return cosine_similarity(tfidf_matrix)
```
Computes the cosine similarity matrix for a given TF-IDF matrix.

### Clustering Articles
```python
def cluster_articles(cosine_sim_matrix: np.ndarray) -> List[int]:
    """Cluster articles using DBSCAN based on the cosine similarity matrix."""
    clustering = DBSCAN(metric='precomputed', min_samples=2, eps=0.5).fit(1 - cosine_sim_matrix)
    return clustering.labels_
```
Clusters articles using the DBSCAN algorithm based on their cosine similarity matrix.

### Merging Clustered Articles
```python
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
```
Merges articles within each cluster, returning a list of merged texts.

### Calculating Average Similarity
```python
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
```
Calculates the average pairwise cosine similarity of merged texts.

### Calculating Similarity of Articles
```python
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
```
Calculates the average pairwise cosine similarity of articles, merging those that tell the same fact.

### Processing Articles
```python
def process_article(article: Dict) -> Dict:
    """Remove HTML tags and unwanted fields from articles."""
    article_copy = article.copy()
    article_copy['title'] = TAG_RE.sub("", article['title'])
    article_copy['content'] = TAG_RE.sub("", article['content'])
    article_copy.pop('time', None)
    return article_copy


```
Cleans up an article by removing HTML tags and unwanted fields.

### Saving Articles to JSON
```python
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
```
Saves unique articles into a JSON file with a sanitized filename and logs the process.

### Saving Grouped Articles
```python
def save_grouped_articles(articles_groups: List[List[Dict]], directory: str) -> List[int]:
    """Save groups of articles to JSON files."""
    seen_articles = set()
    group_sizes = []
    for group in tqdm(articles_groups, desc="Saving groups"):
        if len(group) > 2:
            save_articles_to_json(group, directory, seen_articles)
            group_sizes.append(len(group))
    return group_sizes
```
Saves groups of articles into separate JSON files and returns the sizes of the groups.

## Usage Example
This script is used by `main.py`.
