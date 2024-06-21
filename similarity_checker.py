import re
from typing import List, Dict, Any
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
import spacy
import nltk
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Instructions to download necessary NLTK resources
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

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer('italian')

def preprocess_text(text: str, config: Dict[str, Any]) -> str:
    """Preprocess the text based on the configuration settings."""
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

    stop_words = set(stopwords.words(config.get('stop_words', 'italian')))
    additional_stopwords = set(config.get('additional_stopwords', []))
    tokens = [word for word in tokens if word not in stop_words and word not in additional_stopwords]

    return " ".join(tokens)

def vectorize_texts(texts: List[str], config: Dict[str, Any]) -> Any:
    """Vectorize texts based on the specified method in the configuration."""
    method = config.get('method', 'tfidf')
    vectorizer_params = {
        'ngram_range': tuple(config.get('ngram_range', [1, 2])),
        'max_df': config.get('max_df', 0.85),
        'min_df': config.get('min_df', 0.01)
    }

    if method == 'tfidf':
        vectorizer = TfidfVectorizer(**vectorizer_params)
    elif method == 'count':
        vectorizer = CountVectorizer(**vectorizer_params)
    elif method == 'hashing':
        vectorizer = HashingVectorizer(ngram_range=vectorizer_params['ngram_range'])
    else:
        raise ValueError(f"Unsupported vectorization method: {method}")

    return vectorizer.fit_transform(texts)

def cluster_texts(vectors: Any, config: Dict[str, Any]) -> np.ndarray:
    """Cluster texts using the specified clustering method in the configuration."""
    method = config.get('method', 'dbscan')

    if method == 'dbscan':
        clustering = DBSCAN(
            metric='precomputed',
            eps=config.get('dbscan_params', {}).get('eps', 0.5),
            min_samples=config.get('dbscan_params', {}).get('min_samples', 2)
        )
    elif method == 'kmeans':
        clustering = KMeans(
            n_clusters=config.get('kmeans_params', {}).get('n_clusters', 5)
        )
    elif method == 'agglomerative':
        clustering = AgglomerativeClustering(
            n_clusters=config.get('agglomerative_params', {}).get('n_clusters', 5),
            linkage=config.get('agglomerative_params', {}).get('linkage', 'ward')
        )
    else:
        raise ValueError(f"Unsupported clustering method: {method}")

    if method == 'dbscan':
        # For DBSCAN, compute distance matrix based on cosine similarity
        cosine_sim_matrix = cosine_similarity(vectors)
        distance_matrix = np.maximum(1 - cosine_sim_matrix, 0)
        labels = clustering.fit_predict(distance_matrix)
    else:
        # For KMeans and Agglomerative, use vector data directly
        labels = clustering.fit_predict(vectors.toarray() if method != 'hashing' else vectors)

    return labels

def group_similar_articles(
    articles: List[Dict[str, str]], similarity_threshold: float, config: Dict[str, Any]
) -> List[List[Dict[str, str]]]:
    """Groups similar articles based on a similarity threshold and configuration options."""
    texts = [f"{article['title']} {article['content']}" for article in articles]

    # Preprocess texts
    preprocessed_texts = [preprocess_text(text, config.get('preprocessing', {})) for text in tqdm(texts, desc="Preprocessing texts")]

    # Vectorize texts
    vectors = vectorize_texts(preprocessed_texts, config.get('vectorization', {}))

    # Cluster texts
    cluster_labels = cluster_texts(vectors, config.get('clustering', {}))

    # Group articles based on cluster labels
    grouped_articles = []
    for label in set(cluster_labels):
        if label != -1:  # Ignore noise points
            group = [articles[i] for i in range(len(articles)) if cluster_labels[i] == label]
            grouped_articles.append(group)

    return grouped_articles
