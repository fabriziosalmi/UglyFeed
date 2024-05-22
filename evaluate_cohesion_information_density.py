import json
import nltk
import sys
from langdetect import detect
import spacy
from collections import Counter

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

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

# Placeholder function for Coh-Metrix Scores
def calculate_coh_metrix_scores(text):
    # In a real implementation, this would use the actual Coh-Metrix tool or a similar tool
    # This is a placeholder returning a dummy score for demonstration purposes
    return 0.5

# Function to calculate Cohesion Score
def calculate_cohesion_score(text):
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return 0
    overlaps = 0
    for i in range(len(sentences) - 1):
        tokens1 = set(nltk.word_tokenize(sentences[i].lower()))
        tokens2 = set(nltk.word_tokenize(sentences[i+1].lower()))
        overlaps += len(tokens1.intersection(tokens2))
    return overlaps / (len(sentences) - 1)

# Function to calculate Cohesive Harmony Index
def calculate_cohesive_harmony_index(text, nlp):
    doc = nlp(text)
    harmony_score = 0
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('nsubj', 'dobj', 'iobj', 'pobj'):
                harmony_score += 1
    return harmony_score / len(list(doc.sents)) if len(list(doc.sents)) > 0 else 0

# Function to calculate Referential Density
def calculate_referential_density(text, nlp):
    doc = nlp(text)
    referential_count = sum(1 for token in doc if token.pos_ in ('NOUN', 'PRON'))
    return referential_count / len(doc) if len(doc) > 0 else 0

# Function to calculate Information Density
def calculate_information_density(text):
    words = nltk.word_tokenize(text)
    unique_words = set(words)
    return len(unique_words) / len(words) if len(words) > 0 else 0

def evaluate_cohesion_information_density_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Coh-Metrix Scores": calculate_coh_metrix_scores(text),
        "Cohesion Score": calculate_cohesion_score(text),
        "Cohesive Harmony Index": calculate_cohesive_harmony_index(text, nlp),
        "Referential Density": calculate_referential_density(text, nlp),
        "Information Density": calculate_information_density(text)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper limits
    max_values = {
        "Coh-Metrix Scores": 1,  # Example normalization, adjust as needed
        "Cohesion Score": 1,  # Example normalization, adjust as needed
        "Cohesive Harmony Index": 1,  # Example normalization, adjust as needed
        "Referential Density": 1,  # Example normalization, adjust as needed
        "Information Density": 1  # Example normalization, adjust as needed
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Coh-Metrix Scores": 0.2,
        "Cohesion Score": 0.2,
        "Cohesive Harmony Index": 0.2,
        "Referential Density": 0.2,
        "Information Density": 0.2
    }

    aggregated_score = sum(normalized_metrics[metric] * weights[metric] for metric in normalized_metrics) * 100
    
    return metrics, normalized_metrics, aggregated_score

def main(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            text = data.get("content", "")

        if not text:
            print("No content found in the provided JSON file.")
            return

        lang = detect_language(text)
        metrics, normalized_metrics, aggregated_score = evaluate_cohesion_information_density_metrics(text, lang)

        output = {
            "Cohesion Information Density Metrics": metrics,
            "Aggregated Cohesion Information Density Score": aggregated_score
        }

        print("Text Cohesion and Information Density Metrics:")
        for metric, score in metrics.items():
            print(f"{metric}: {score:.4f}")
        print("\nNormalized Metrics:")
        for metric, score in normalized_metrics.items():
            print(f"{metric}: {score:.4f}")
        print(f"\nAggregated Cohesion and Information Density Score: {aggregated_score:.4f}")

        # Export results to JSON
        output_file_path = file_path.replace(".json", "_metrics_cohesion_information_density.json")
        with open(output_file_path, 'w') as out_file:
            json.dump(output, out_file, indent=4)
        print(f"Metrics exported to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The provided file is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_cohesion_information_density_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
