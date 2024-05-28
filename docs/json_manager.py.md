# json_manager.py

## Introduction
This script, used by `main.py`, contains functions for processing and saving grouped articles into JSON files. It sanitizes filenames, calculates similarities, processes articles, and handles the saving of articles while ensuring uniqueness.

## Input/Output

### Input
- **Articles**: A list of article dictionaries to be processed and grouped.
- **Directory**: The output directory where the JSON files will be saved.

### Output
- **JSON Files**: Grouped articles saved as JSON files in the specified directory.

## Functionality

### Features
1. **Filename Sanitization**: Removes invalid characters from filenames.
2. **Title Generation**: Generates a group title based on the most common words in article titles.
3. **Similarity Calculation**: Calculates the average pairwise cosine similarity of articles.
4. **Article Processing**: Cleans up articles by removing HTML tags and unwanted fields.
5. **JSON Saving**: Saves unique articles into JSON files with informative filenames.

## Code Structure

### Imports
```python
import json
import os
import re
import datetime
from typing import List, Dict
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import hashlib
from tqdm import tqdm
import logging
```
- **json**: For reading and writing JSON files.
- **os**: For file and directory operations.
- **re**: For regular expressions.
- **datetime**: For date and time operations.
- **typing**: For type annotations.
- **collections.Counter**: For counting word occurrences.
- **sklearn.metrics.pairwise.cosine_similarity**: For calculating cosine similarity.
- **sklearn.feature_extraction.text.TfidfVectorizer**: For transforming text data into TF-IDF features.
- **numpy**: For numerical operations.
- **hashlib**: For generating MD5 hashes.
- **tqdm**: For displaying progress bars.
- **logging**: For logging information and errors.

### Logging Configuration
```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
Configures logging to display informational messages with timestamps.

### Filename Sanitization
```python
def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r'[<>:"/\\|?*\n\r\']+', '', filename).replace(',', '_').replace(' ', '_')
```
Removes invalid characters from filenames to ensure they are safe to use.

### Title Generation
```python
def generate_title(articles: List[Dict]) -> str:
    """Generate a title based on the most common words in article titles."""
    title_words = [word.lower() for article in articles for word in article['title'].split()]
    word_counts = Counter(title_words)
    common_words = [word for word, count in word_counts.most_common(10) if len(word) > 3][:3]
    return ' '.join(common_words)
```
Generates a title for a group of articles based on the most common words in their titles.

### Similarity Calculation
```python
def calculate_similarity(articles: List[Dict]) -> float:
    """Calculate the average pairwise cosine similarity of articles."""
    if len(articles) <= 1:
        return 0.0
    texts = [f"{article['title']} {article['content']}" for article in articles]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix)
    num_comparisons = len(articles) * (len(articles) - 1) / 2
    return np.tril(cosine_sim_matrix, -1).sum() / num_comparisons if num_comparisons > 0 else 0.0
```
Calculates the average pairwise cosine similarity of a list of articles.

### Article Processing
```python
def process_article(article: Dict) -> Dict:
    """Process an article by removing HTML tags and unwanted fields."""
    article_copy = article.copy()
    article_copy['title'] = re.sub(r"<[^<]+?>", "", article['title'])
    article_copy['content'] = re.sub(r"<[^<]+?>", "", article['content'])
    article_copy.pop('time', None)  # Use pop to safely remove the key
    return article_copy
```
Cleans up an article by removing HTML tags and unwanted fields.

### Saving Articles to JSON
```python
def save_articles_to_json(articles: List[Dict], directory: str = "output", seen_articles: set = None) -> None:
    """Save unique articles to a JSON file with sanitized filenames."""
    if seen_articles is None:
        seen_articles = set()

    os.makedirs(directory, exist_ok=True)
    unique_articles = []
    seen_in_this_group = set()

    for article in articles:
        article_copy = process_article(article)
        article_hash = hashlib.md5(
            (article_copy['title'] + article_copy['content']).encode()).hexdigest()
        if article_hash not in seen_articles and article_hash not in seen_in_this_group:
            unique_articles.append(article_copy)
            seen_articles.add(article_hash)
            seen_in_this_group.add(article_hash)

    if len(unique_articles) > 1:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M")
        group_title = generate_title(unique_articles)
        sanitized_title = sanitize_filename(group_title)
        similarity_score = calculate_similarity(unique_articles)
        num_items = len(unique_articles)
        filename = (
            f"{date_str}_{time_str}-{sanitized_title}-Q{num_items}-S{similarity_score:.2f}.json"
        )
        file_path = os.path.join(directory, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(unique_articles, file, ensure_ascii=False, indent=4)
            logging.info(
                "Saved %s with %d items and similarity score %.2f",
                file_path, num_items, similarity_score
            )
        except IOError as e:
            logging.error("Failed to save %s: %s", file_path, e)
```
Saves unique articles into a JSON file with a sanitized filename and logs the process.

### Saving Grouped Articles
```python
def save_grouped_articles(articles_groups: List[List[Dict]], directory: str = "output") -> List[int]:
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
