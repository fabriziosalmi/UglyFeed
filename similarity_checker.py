import re
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from typing import List, Dict
from tqdm import tqdm

def preprocess_text(text):
    """Normalizes, removes punctuation, HTML tags, and applies stemming to a text string."""
    text = re.sub(r"<[^<]+?>", "", text)  # Remove HTML tags
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    stemmer = PorterStemmer()
    text = " ".join([stemmer.stem(word) for word in text.split()])
    return text

def group_similar_articles(articles: List[Dict], similarity_threshold: float = 0.5, use_dict=False) -> List[List[Dict]] or Dict[int, List[Dict]]:
    """
    Groups similar articles based on title and content similarity.

    Args:
        articles (List[Dict]): A list of article dictionaries with 'title' and 'content' keys.
        similarity_threshold (float, optional): The minimum cosine similarity for grouping. Defaults to 0.5.
        use_dict (bool, optional): If True, returns groups as a dictionary with group IDs as keys. Defaults to False.

    Returns:
        List[List[Dict]] or Dict[int, List[Dict]]: A list of groups (if use_dict=False) or a dictionary of groups with IDs (if use_dict=True).
    """
    texts = [preprocess_text(f"{article['title']} {article['content']}") for article in articles]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_sim = cosine_similarity(csr_matrix(tfidf_matrix))  # Use sparse matrix

    visited = set()
    groups = {} if use_dict else []

    def dfs(i, group_id=None):
        group = groups[group_id] if use_dict else [articles[i]]
        visited.add(i)
        for j in range(len(articles)):
            if j != i and j not in visited and cosine_sim[i][j] >= similarity_threshold:
                group.extend(dfs(j, group_id) if use_dict else dfs(j))
        return group

    for i in tqdm(range(len(articles)), desc="Grouping articles"):
        if i not in visited:
            if use_dict:
                group_id = len(groups)
                groups[group_id] = dfs(i, group_id)
            else:
                groups.append(dfs(i))

    return groups

