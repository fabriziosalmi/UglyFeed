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
    text = " ".join(lemmatizer.lemmatize(word) for word in text.split() if word not in italian_stop_words)
    return text



from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import numpy as np


from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import numpy as np

from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import numpy as np

from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import numpy as np

def group_similar_articles(articles: List[Dict[str, str]], similarity_threshold: float, similarity_options: dict) -> List[List[Dict[str, str]]]:
    """Group similar articles based on a similarity threshold and options."""
    # Convert articles to texts for TF-IDF vectorization
    texts = [f"{article['title']} {article['content']}" for article in articles]

    # Compute TF-IDF matrix
    tfidf_matrix = TfidfVectorizer().fit_transform(texts)

    # Compute cosine similarity matrix
    cosine_sim_matrix = cosine_similarity(tfidf_matrix)

    # Ensure distance matrix has non-negative values
    distance_matrix = 1 - cosine_sim_matrix
    distance_matrix[distance_matrix < 0] = 0

    # Cluster articles using DBSCAN
    clustering = DBSCAN(metric='precomputed', **similarity_options).fit(distance_matrix)
    cluster_labels = clustering.labels_

    # Debug information
    print(f"Cluster labels: {np.unique(cluster_labels)}")

    # Group articles based on cluster labels
    grouped_articles = []
    for label in set(cluster_labels):
        if label != -1:
            group = [articles[i] for i in range(len(articles)) if cluster_labels[i] == label]
            # Debug information
            print(f"Group size for label {label}: {len(group)}")
            grouped_articles.append(group)
    return grouped_articles
