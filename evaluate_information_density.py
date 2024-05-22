import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from collections import Counter
from langdetect import detect
import spacy

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

# Load the spaCy models for both English and Italian
nlp_en = spacy.load("en_core_web_sm")
nlp_it = spacy.load("it_core_news_sm")

# Define function to detect language
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian

# Define function to get appropriate spaCy model based on language
def get_spacy_model(lang):
    if lang == 'en':
        return nlp_en
    else:
        return nlp_it

# Function to calculate Information Density
def calculate_information_density(text, nlp):
    doc = nlp(text)
    content_words = [token for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}]
    return len(content_words) / len(doc) if len(doc) > 0 else 0

# Function to calculate Referential Density
def calculate_referential_density(text, nlp):
    doc = nlp(text)
    references = [token for token in doc if token.dep_ in {"nsubj", "dobj", "pobj", "nsubjpass"}]
    return len(references) / len(doc) if len(doc) > 0 else 0

# Function to calculate Cohesive Harmony Index
def calculate_cohesive_harmony_index(text, nlp):
    doc = nlp(text)
    cohesive_elements = [token for token in doc if token.dep_ in {"cc", "conj", "mark", "advmod", "prep"}]
    return len(cohesive_elements) / len(doc) if len(doc) > 0 else 0

def evaluate_information_density_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Information Density": calculate_information_density(text, nlp),
        "Referential Density": calculate_referential_density(text, nlp),
        "Cohesive Harmony Index": calculate_cohesive_harmony_index(text, nlp)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper limits
    max_values = {
        "Information Density": 0.7,  # Example normalization, adjust as needed
        "Referential Density": 0.5,  # Example normalization, adjust as needed
        "Cohesive Harmony Index": 0.5  # Example normalization, adjust as needed
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Information Density": 0.4,
        "Referential Density": 0.3,
        "Cohesive Harmony Index": 0.3
    }

    aggregated_score = sum(normalized_metrics[metric] * weights[metric] for metric in normalized_metrics) * 100
    
    return metrics, normalized_metrics, aggregated_score

def main(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        text = data.get("content", "")

    if not text:
        print("No content found in the provided JSON file.")
        return

    lang = detect_language(text)
    metrics, normalized_metrics, aggregated_score = evaluate_information_density_metrics(text, lang)

    print("Text Information and Density Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Information and Density Score: {aggregated_score:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_information_density.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
