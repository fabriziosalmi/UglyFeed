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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r'[<>:"/\\|?*\n\r\']+', '', filename).replace(',', '_').replace(' ', '_')

def generate_title(articles: List[Dict]) -> str:
    """Generate a title based on the most common words in article titles."""
    title_words = [word.lower() for article in articles for word in article['title'].split()]
    word_counts = Counter(title_words)
    common_words = [word for word, count in word_counts.most_common(10) if len(word) > 3][:3]
    return ' '.join(common_words)

def calculate_similarity(articles: List[Dict],
                         ngram_range: tuple = (1, 1),
                         min_df: int = 1,
                         max_df: float = 1.0,
                         max_features: int = None,
                         stop_words: List[str] = None) -> float:
    """
    Calculate the average pairwise cosine similarity of articles.

    Parameters:
        articles (List[Dict]): List of articles, each with 'title' and 'content'.
        ngram_range (tuple): The range of n-values for different n-grams to be extracted. Defaults to (1, 1).
        min_df (int): Minimum document frequency for terms. Defaults to 1.
        max_df (float): Maximum document frequency for terms. Defaults to 1.0.
        max_features (int): Maximum number of features to consider. Defaults to None (consider all features).
        stop_words (List[str]): List of words to be ignored in the TF-IDF vectorization. Defaults to None.

    Returns:
        float: The average pairwise cosine similarity.
    """
    num_articles = len(articles)

    if num_articles <= 1:
        logging.info("Insufficient articles for similarity calculation.")
        return 0.0

    try:
        # Combine titles and content for each article to form the text corpus
        texts = [f"{article['title']} {article['content']}" for article in articles]

        # Create the TF-IDF vectorizer with specified parameters and transform the texts
        vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            max_features=max_features,
            stop_words=stop_words
        )
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Check if the TF-IDF matrix is empty
        if tfidf_matrix.shape[0] == 0 or tfidf_matrix.shape[1] == 0:
            logging.warning("TF-IDF matrix is empty, returning zero similarity.")
            return 0.0

        # Compute the cosine similarity matrix
        cosine_sim_matrix = cosine_similarity(tfidf_matrix, dense_output=False)

        # Extract the lower triangular values excluding the diagonal
        lower_triangular_indices = np.tril_indices(num_articles, -1)
        lower_triangular_values = cosine_sim_matrix[lower_triangular_indices]

        num_comparisons = lower_triangular_values.size

        if num_comparisons == 0:
            logging.info("No valid comparisons found, returning zero similarity.")
            return 0.0

        # Calculate the mean of the lower triangular values of the cosine similarity matrix
        average_similarity = lower_triangular_values.mean()

        logging.info("Calculated average similarity: %.4f", average_similarity)
        return average_similarity

    except Exception as e:
        logging.error("Error in calculating similarity: %s", e)
        return 0.0





def process_article(article: Dict) -> Dict:
    """Process an article by removing HTML tags and unwanted fields."""
    article_copy = article.copy()
    article_copy['title'] = re.sub(r"<[^<]+?>", "", article['title'])
    article_copy['content'] = re.sub(r"<[^<]+?>", "", article['content'])
    article_copy.pop('time', None)  # Use pop to safely remove the key
    return article_copy

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

def save_grouped_articles(articles_groups: List[List[Dict]], directory: str = "output") -> List[int]:
    """Save groups of articles to JSON files."""
    seen_articles = set()
    group_sizes = []
    for group in articles_groups:
        if len(group) > 2:
            save_articles_to_json(group, directory, seen_articles)
            group_sizes.append(len(group))
    return group_sizes
