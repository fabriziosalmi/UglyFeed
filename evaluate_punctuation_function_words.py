import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from collections import Counter
from langdetect import detect

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")

# Define function to detect language
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian

# Define punctuation and function word lists
punctuations = [".", ",", "!", "?", ":", ";", "-", "(", ")", "[", "]", "{", "}", "'", "\"", "..."]
conjunctions_en = ["and", "or", "but", "nor", "for", "yet", "so"]
conjunctions_it = ["e", "o", "ma", "né", "perché", "siccome", "poiché", "quindi"]
prepositions_en = ["in", "on", "at", "by", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "out", "off", "over", "under", "again", "further", "then", "once"]
prepositions_it = ["in", "su", "a", "da", "con", "di", "tra", "fra", "per", "contro", "verso", "durante", "prima", "dopo", "sopra", "sotto", "fino", "oltre", "dentro", "fuori", "attraverso", "circa", "entro", "dietro", "davanti"]

# Function to calculate Punctuation Frequency
def calculate_punctuation_frequency(text):
    words = word_tokenize(text)
    punctuation_count = Counter(word for word in words if word in punctuations)
    return punctuation_count

# Function to calculate Ellipsis Frequency
def calculate_ellipsis_frequency(text):
    words = word_tokenize(text)
    ellipsis_count = words.count("...")
    return ellipsis_count / len(words) if words else 0

# Function to calculate Conjunction Usage Frequency
def calculate_conjunction_usage_frequency(text, lang):
    words = word_tokenize(text.lower())
    conjunctions = conjunctions_en if lang == 'en' else conjunctions_it
    conjunction_count = Counter(word for word in words if word in conjunctions)
    return sum(conjunction_count.values()) / len(words) if words else 0

# Function to calculate Preposition Usage Frequency
def calculate_preposition_usage_frequency(text, lang):
    words = word_tokenize(text.lower())
    prepositions = prepositions_en if lang == 'en' else prepositions_it
    preposition_count = Counter(word for word in words if word in prepositions)
    return sum(preposition_count.values()) / len(words) if words else 0

def evaluate_punctuation_function_word_metrics(text, lang):
    metrics = {
        "Punctuation Frequency": calculate_punctuation_frequency(text),
        "Ellipsis Frequency": calculate_ellipsis_frequency(text),
        "Conjunction Usage Frequency": calculate_conjunction_usage_frequency(text, lang),
        "Preposition Usage Frequency": calculate_preposition_usage_frequency(text, lang)
    }

    total_words = len(word_tokenize(text))
    normalized_metrics = {
        "Punctuation Frequency": sum(metrics["Punctuation Frequency"].values()) / total_words if total_words else 0,
        "Ellipsis Frequency": metrics["Ellipsis Frequency"],
        "Conjunction Usage Frequency": metrics["Conjunction Usage Frequency"],
        "Preposition Usage Frequency": metrics["Preposition Usage Frequency"]
    }

    # Normalize metrics to the range 0-1 based on reasonable upper limits for each metric
    max_values = {
        "Punctuation Frequency": 0.3,  # Assuming that up to 30% punctuation is reasonable
        "Ellipsis Frequency": 0.01,   # Assuming ellipsis is rare
        "Conjunction Usage Frequency": 0.1,  # Assuming up to 10% conjunctions is reasonable
        "Preposition Usage Frequency": 0.15  # Assuming up to 15% prepositions is reasonable
    }

    for key in normalized_metrics:
        normalized_metrics[key] = min(normalized_metrics[key] / max_values[key], 1)

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Punctuation Frequency": 0.25,
        "Ellipsis Frequency": 0.25,
        "Conjunction Usage Frequency": 0.25,
        "Preposition Usage Frequency": 0.25
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
    metrics, normalized_metrics, aggregated_score = evaluate_punctuation_function_word_metrics(text, lang)

    print("Text Punctuation and Function Word Metrics:")
    for metric, score in metrics.items():
        if isinstance(score, dict):
            print(f"{metric}: {dict(score)}")
        else:
            print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Punctuation and Function Word Score: {aggregated_score:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_punctuation_function_words.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
