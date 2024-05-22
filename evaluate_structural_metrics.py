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

# Define enhanced discourse markers for both languages
discourse_markers_en = [
    "however", "therefore", "moreover", "furthermore", "thus", "consequently", "meanwhile", 
    "additionally", "nevertheless", "nonetheless", "for example", "for instance", "in other words",
    "on the other hand", "in contrast", "similarly", "likewise"
]

discourse_markers_it = [
    "tuttavia", "quindi", "inoltre", "pertanto", "così", "conseguentemente", "nel frattempo", 
    "addizionalmente", "nonostante", "comunque", "per esempio", "ad esempio", "in altre parole", 
    "d'altra parte", "in contrasto", "similmente", "analogamente"
]

# Function to calculate Subordination Index
def calculate_subordination_index(text, nlp):
    doc = nlp(text)
    subord_conjunctions = [token for token in doc if token.dep_ == "mark"]
    clauses = [sent for sent in doc.sents]
    return len(subord_conjunctions) / len(clauses) if len(clauses) > 0 else 0

# Function to calculate Coordination Index
def calculate_coordination_index(text, nlp):
    doc = nlp(text)
    coord_conjunctions = [token for token in doc if token.dep_ == "cc"]
    clauses = [sent for sent in doc.sents]
    return len(coord_conjunctions) / len(clauses) if len(clauses) > 0 else 0

# Function to calculate Discourse Marker Frequency
def calculate_discourse_marker_frequency(text, lang):
    words = word_tokenize(text.lower())
    discourse_markers = discourse_markers_en if lang == 'en' else discourse_markers_it
    marker_count = Counter(word for word in words if word in discourse_markers)
    return sum(marker_count.values()) / len(words) if len(words) > 0 else 0

def evaluate_structural_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Subordination Index": calculate_subordination_index(text, nlp),
        "Coordination Index": calculate_coordination_index(text, nlp),
        "Discourse Marker Frequency": calculate_discourse_marker_frequency(text, lang)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper limits
    max_values = {
        "Subordination Index": 0.5,  # Example normalization, adjust as needed
        "Coordination Index": 0.5,  # Example normalization, adjust as needed
        "Discourse Marker Frequency": 0.1  # Example normalization, adjust as needed
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Subordination Index": 0.4,
        "Coordination Index": 0.3,
        "Discourse Marker Frequency": 0.3
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
    metrics, normalized_metrics, aggregated_score = evaluate_structural_metrics(text, lang)

    output = {
        "Text Structural Metrics": metrics,
        "Aggregated Text Structural Score": aggregated_score
    }

    print("Text Structural Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Structural Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_structural.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_structural_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
