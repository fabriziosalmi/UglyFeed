import re
from typing import List, Dict, Union
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy

# Instructions to download necessary NLTK and spaCy resources
import nltk
nltk.download('stopwords')
nltk.download('omw-1.4')  # For multi-language support

# Download spaCy model if not already downloaded
try:
    nlp = spacy.load("it_core_news_sm")
except OSError:
    from spacy.cli import download
    download("it_core_news_sm")
    nlp = spacy.load("it_core_news_sm")

# Initialize other NLP tools
lemmatizer = WordNetLemmatizer()
italian_stop_words = list(stopwords.words('italian'))  # Convert set to list

def preprocess_text(text: str) -> str:
    """Normalizes, removes punctuation, HTML tags, and applies lemmatization to a text string."""
    text = re.sub(r"<[^<]+?>", "", text)  # Remove HTML tags
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join(lemmatizer.lemmatize(word) for word in text.split() if word not in italian_stop_words)
    return text

def group_similar_articles(
    articles: List[Dict[str, str]], 
    similarity_threshold: float = 0.5, 
    use_dict: bool = False,
) -> Union[List[List[Dict[str, str]]], Dict[int, List[Dict[str, str]]]]:
    """
    Groups similar articles based on title and content similarity.

    Args:
        articles (List[Dict[str, str]]): A list of article dictionaries with 'title' and 'content' keys.
        similarity_threshold (float, optional): The minimum cosine similarity for grouping. Defaults to 0.5.
        use_dict (bool, optional): If True, returns groups as a dictionary with group IDs as keys. Defaults to False.

    Returns:
        Union[List[List[Dict[str, str]]], Dict[int, List[Dict[str, str]]]]: A list of groups (if use_dict=False) or a dictionary of groups with IDs (if use_dict=True).
    """
    if not articles:
        return {} if use_dict else []

    # Preprocess text for each article
    texts = [preprocess_text(f"{article['title']} {article['content']}") for article in articles]

    # Convert the corpus into a TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words=italian_stop_words)
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix)

    visited = set()
    groups = {} if use_dict else []

    def iterative_dfs(start_idx, group_id=None):
        stack = [start_idx]
        group = [] if not use_dict else groups[group_id]
        while stack:
            i = stack.pop()
            if i not in visited:
                visited.add(i)
                group.append(articles[i])
                for j in range(len(articles)):
                    if j != i and j not in visited and cosine_sim[i][j] >= similarity_threshold:
                        stack.append(j)
        return group

    for i in tqdm(range(len(articles)), desc="Grouping articles"):
        if i not in visited:
            if use_dict:
                group_id = len(groups)
                groups[group_id] = iterative_dfs(i, group_id)
            else:
                groups.append(iterative_dfs(i))

    return groups
