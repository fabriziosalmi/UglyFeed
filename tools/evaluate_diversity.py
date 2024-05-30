import sys
import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

# use
# python evaluate_diversity.py rewritten/xxx_rewritten.json output/xxx.json
#
# example output:
# Semantic Similarity Metrics:
# TF-IDF Cosine Similarity: 0.3693
# BoW Cosine Similarity: 0.5159
# Embedding Cosine Similarity: 0.3586
# Jaccard Similarity: 0.1140
# ROUGE-L Similarity: 0.2413
# Aggregated Semantic Score: 0.3316

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)

# Load pre-trained SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def tfidf_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

def bow_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

def embedding_cosine_similarity(text1, text2):
    embeddings = model.encode([text1, text2])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

def jaccard_similarity(text1, text2):
    words1 = set(word_tokenize(text1))
    words2 = set(word_tokenize(text2))
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0

def rouge_l_similarity(text1, text2):
    def lcs(X, Y):
        m = len(X)
        n = len(Y)
        L = [[0] * (n + 1) for i in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i - 1] == Y[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])
        return L[m][n]

    words1 = word_tokenize(text1)
    words2 = word_tokenize(text2)
    lcs_length = lcs(words1, words2)
    return (2 * lcs_length) / (len(words1) + len(words2))

def calculate_semantic_metrics(text1, text2):
    metrics = {
        "TF-IDF Cosine Similarity": tfidf_cosine_similarity(text1, text2),
        "BoW Cosine Similarity": bow_cosine_similarity(text1, text2),
        "Embedding Cosine Similarity": embedding_cosine_similarity(text1, text2),
        "Jaccard Similarity": jaccard_similarity(text1, text2),
        "ROUGE-L Similarity": rouge_l_similarity(text1, text2),
    }

    # Calculate aggregated score (customizable weights)
    weights = {
        "TF-IDF Cosine Similarity": 0.2,
        "BoW Cosine Similarity": 0.2,
        "Embedding Cosine Similarity": 0.3,
        "Jaccard Similarity": 0.2,
        "ROUGE-L Similarity": 0.1,
    }

    aggregated_score = sum(metrics[metric] * weights[metric] for metric in metrics)

    return metrics, aggregated_score

def main(generated_file, reference_file):
    with open(generated_file, 'r') as gf, open(reference_file, 'r') as rf:
        generated = gf.read()
        reference = rf.read()

    metrics, aggregated_score = calculate_semantic_metrics(generated, reference)

    print("Semantic Similarity Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"Aggregated Semantic Score: {aggregated_score:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evaluate_semantics.py <generated_file> <reference_file>")
        sys.exit(1)

    generated_file = sys.argv[1]
    reference_file = sys.argv[2]
    main(generated_file, reference_file)
