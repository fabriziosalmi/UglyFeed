import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from nltk.corpus import stopwords
from nltk.metrics.distance import jaro_winkler_similarity
import math
from collections import Counter
from lexical_diversity import lex_div as ld

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# Function to calculate Jaro-Winkler Distance
def calculate_jaro_winkler_distance(text1, text2):
    return 1 - jaro_winkler_similarity(text1, text2)

# Function to calculate Honore’s Statistic
def calculate_honore_statistic(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    V1 = sum(1 for word in freq if freq[word] == 1)
    N = len(words)
    return 100 * math.log(N) / (1 - (V1 / N)) if N > 0 else 0

# Function to calculate Sichel’s Measure
def calculate_sichel_measure(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    V2 = sum(1 for word in freq if freq[word] == 2)
    V = len(freq)
    return V2 / V if V > 0 else 0

# Function to calculate Brunet’s Measure
def calculate_brunet_measure(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    V = len(freq)
    N = len(words)
    return N ** (V ** -0.165) if V > 0 and N > 0 else 0

# Function to calculate Yule’s Characteristic K
def calculate_yule_characteristic_k(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    M1 = sum(freq.values())
    M2 = sum(freq[word] ** 2 for word in freq)
    return 10000 * (M2 - M1) / (M1 ** 2) if M1 > 0 else 0

# Function to calculate MTLD (Measure of Textual Lexical Diversity)
def calculate_mtld(text):
    words = word_tokenize(text.lower())
    return ld.mtld(words)

# Function to calculate HD-D (Hypergeometric Distribution D)
def calculate_hdd(text):
    words = word_tokenize(text.lower())
    return ld.hdd(words)

# Function to calculate Variability Index
def calculate_variability_index(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    V = len(freq)
    N = len(words)
    return V / N if N > 0 else 0

# Normalize metrics to a range of 0 to 1
def normalize_metric(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

def evaluate_statistical_metrics(text):
    # Placeholder text for comparison for Jaro-Winkler Distance
    placeholder_text = "This is a placeholder text for comparison."

    metrics = {
        "Jaro-Winkler Distance": calculate_jaro_winkler_distance(text, placeholder_text),
        "Honore’s Statistic": calculate_honore_statistic(text),
        "Sichel’s Measure": calculate_sichel_measure(text),
        "Brunet’s Measure": calculate_brunet_measure(text),
        "Yule’s Characteristic K": calculate_yule_characteristic_k(text),
        "MTLD (Measure of Textual Lexical Diversity)": calculate_mtld(text),
        "HD-D (Hypergeometric Distribution D)": calculate_hdd(text),
        "Variability Index": calculate_variability_index(text)
    }

    # Normalize the metrics to a range of 0 to 1
    normalized_metrics = {
        "Jaro-Winkler Distance": normalize_metric(metrics["Jaro-Winkler Distance"], 0, 1),
        "Honore’s Statistic": normalize_metric(metrics["Honore’s Statistic"], 0, 2000),  # Example range
        "Sichel’s Measure": normalize_metric(metrics["Sichel’s Measure"], 0, 1),
        "Brunet’s Measure": normalize_metric(metrics["Brunet’s Measure"], 0, 20),  # Example range
        "Yule’s Characteristic K": normalize_metric(metrics["Yule’s Characteristic K"], 0, 200),  # Example range
        "MTLD (Measure of Textual Lexical Diversity)": normalize_metric(metrics["MTLD (Measure of Textual Lexical Diversity)"], 0, 200),  # Example range
        "HD-D (Hypergeometric Distribution D)": normalize_metric(metrics["HD-D (Hypergeometric Distribution D)"], 0, 1),
        "Variability Index": normalize_metric(metrics["Variability Index"], 0, 1)
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Jaro-Winkler Distance": 0.125,
        "Honore’s Statistic": 0.125,
        "Sichel’s Measure": 0.125,
        "Brunet’s Measure": 0.125,
        "Yule’s Characteristic K": 0.125,
        "MTLD (Measure of Textual Lexical Diversity)": 0.125,
        "HD-D (Hypergeometric Distribution D)": 0.125,
        "Variability Index": 0.125
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

    metrics, normalized_metrics, aggregated_score = evaluate_statistical_metrics(text)

    output = {
        "Text Statistical Metrics": metrics,
        "Aggregated Text Statistical Score": aggregated_score
    }

    print("Text Statistical Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Statistical Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_statistical.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_statistical_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
