import re
from typing import List, Dict, Union
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy
import nltk
from sklearn.cluster import DBSCAN

# Instructions to download necessary NLTK and spaCy resources
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('omw-1.4', quiet=True)  # For multi-language support

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
    text = " ".join(
        lemmatizer.lemmatize(word) for word in text.split() if word not in italian_stop_words
    )
    return text

def group_similar_articles(
    articles: List[Dict[str, str]], similarity_threshold: float, similarity_options: dict
) -> List[List[Dict[str, str]]]:
    """Groups similar articles based on a similarity threshold and options."""
    texts = [f"{article['title']} {article['content']}" for article in articles]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    cosine_sim_matrix = cosine_similarity(tfidf_matrix)

    distance_matrix = 1 - cosine_sim_matrix
    distance_matrix[distance_matrix < 0] = 0

    clustering = DBSCAN(metric='precomputed', **similarity_options).fit(distance_matrix)
    cluster_labels = clustering.labels_

    grouped_articles = []
    for label in set(cluster_labels):
        if label != -1:
            group = [articles[i] for i in range(len(articles)) if cluster_labels[i] == label]
            grouped_articles.append(group)

    return grouped_articles
