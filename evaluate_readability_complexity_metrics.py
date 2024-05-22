import json
import nltk
import sys
from langdetect import detect
import textstat

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")

# Define function to detect language
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian

# Function to calculate Syllable Count
def calculate_syllable_count(text):
    return textstat.syllable_count(text)

# Function to calculate Flesch-Kincaid Grade Level
def calculate_flesch_kincaid_grade(text):
    return textstat.flesch_kincaid_grade(text)

# Function to calculate SMOG Index
def calculate_smog_index(text):
    return textstat.smog_index(text)

# Function to calculate Readability Ease Score
def calculate_readability_ease(text):
    return textstat.flesch_reading_ease(text)

def evaluate_readability_complexity_metrics(text, lang):
    # Calculate raw metrics
    metrics = {
        "Syllable Count": calculate_syllable_count(text),
        "Flesch-Kincaid Grade Level": calculate_flesch_kincaid_grade(text),
        "SMOG Index": calculate_smog_index(text),
        "Readability Ease Score": calculate_readability_ease(text)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper and lower limits
    max_values = {
        "Syllable Count": 500,  # Example normalization, adjust as needed
        "Flesch-Kincaid Grade Level": 20,  # Example normalization, adjust as needed
        "SMOG Index": 20,  # Example normalization, adjust as needed
        "Readability Ease Score": 100  # Example normalization, adjust as needed
    }

    normalized_metrics = {
        key: min(metrics[key] / max_values[key], 1) if key != "Readability Ease Score" else metrics[key] / max_values[key]
        for key in metrics
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Syllable Count": 0.2,
        "Flesch-Kincaid Grade Level": 0.3,
        "SMOG Index": 0.3,
        "Readability Ease Score": 0.2
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
        metrics, normalized_metrics, aggregated_score = evaluate_readability_complexity_metrics(text, lang)

        print("Text Readability and Complexity Metrics:")
        for metric, score in metrics.items():
            print(f"{metric}: {score:.4f}")
        print("\nNormalized Metrics:")
        for metric, score in normalized_metrics.items():
            print(f"{metric}: {score:.4f}")
        print(f"\nAggregated Readability and Complexity Score: {aggregated_score:.4f}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The provided file is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_readability_complexity_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
