# similarity_checker.py

## Introduction
This script, used by `main.py`, contains functions to preprocess text, compute similarities between articles, and group similar articles using clustering algorithms. It uses various NLP tools and libraries like NLTK and spaCy for text normalization and lemmatization, and scikit-learn for vectorization and clustering.

## Input/Output

### Input
- **Articles**: A list of article dictionaries, each containing `title` and `content`.
- **Similarity Threshold**: A float value used to determine the similarity threshold for clustering.
- **Similarity Options**: A dictionary of options for the DBSCAN clustering algorithm.

### Output
- **Grouped Articles**: A list of lists where each inner list contains grouped articles based on their similarity.

## Functionality

### Features
1. **Text Preprocessing**: Normalizes text by removing punctuation, HTML tags, and applying lemmatization.
2. **TF-IDF Vectorization**: Converts text data into TF-IDF features for similarity calculations.
3. **Cosine Similarity Calculation**: Computes the cosine similarity matrix for articles.
4. **Clustering**: Uses DBSCAN clustering to group similar articles based on their similarity.
5. **Debug Information**: Prints debug information about cluster labels and group sizes.

## Code Structure

### Imports
```python
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
```
- **re**: For regular expressions.
- **typing**: For type annotations.
- **tqdm**: For displaying progress bars.
- **numpy**: For numerical operations.
- **sklearn.feature_extraction.text.TfidfVectorizer**: For transforming text data into TF-IDF features.
- **sklearn.metrics.pairwise.cosine_similarity**: For calculating cosine similarity.
- **nltk.stem.WordNetLemmatizer**: For lemmatizing words.
- **nltk.corpus.stopwords**: For removing stop words.
- **spacy**: For advanced NLP processing.
- **nltk**: For downloading necessary NLTK resources.

### NLTK and spaCy Resources
```python
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('omw-1.4', quiet=True)

try:
    nlp = spacy.load("it_core_news_sm")
except OSError:
    from spacy.cli import download
    download("it_core_news_sm")
    nlp = spacy.load("it_core_news_sm")
```
Downloads necessary NLTK and spaCy resources and loads the spaCy model for Italian.

### NLP Tools Initialization
```python
lemmatizer = WordNetLemmatizer()
italian_stop_words = list(stopwords.words('italian'))
```
Initializes the lemmatizer and loads Italian stop words.

### Text Preprocessing
```python
def preprocess_text(text: str) -> str:
    """Normalizes, removes punctuation, HTML tags, and applies lemmatization to a text string."""
    text = re.sub(r"<[^<]+?>", "", text)  # Remove HTML tags
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join(lemmatizer.lemmatize(word) for word in text.split() if word not in italian_stop_words)
    return text
```
Normalizes text by removing HTML tags, converting to lowercase, removing punctuation, and applying lemmatization.

### Grouping Similar Articles
```python
def group_similar_articles(articles: List[Dict[str, str]], similarity_threshold: float, similarity_options: dict) -> List[List[Dict[str, str]]]:
    """Group similar articles based on a similarity threshold and options."""
    texts = [f"{article['title']} {article['content']}" for article in articles]

    tfidf_matrix = TfidfVectorizer().fit_transform(texts)

    cosine_sim_matrix = cosine_similarity(tfidf_matrix)

    distance_matrix = 1 - cosine_sim_matrix
    distance_matrix[distance_matrix < 0] = 0

    clustering = DBSCAN(metric='precomputed', **similarity_options).fit(distance_matrix)
    cluster_labels = clustering.labels_

    print(f"Cluster labels: {np.unique(cluster_labels)}")

    grouped_articles = []
    for label in set(cluster_labels):
        if label != -1:
            group = [articles[i] for i in range(len(articles)) if cluster_labels[i] == label]
            print(f"Group size for label {label}: {len(group)}")
            grouped_articles.append(group)
    return grouped_articles
```
Groups similar articles based on the similarity threshold and options provided. It performs TF-IDF vectorization, computes cosine similarity, and uses DBSCAN for clustering.

## Usage Example
This script is used by `main.py`.
