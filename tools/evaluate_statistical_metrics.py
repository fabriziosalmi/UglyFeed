"""
Module for evaluating statistical text metrics.
"""

import json
import math
import sys
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize
from nltk.metrics.distance import jaro_winkler_similarity
from lexical_diversity import lex_div as ld

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

def calculate_jaro_winkler_distance(text1, text2):
    """
    Calculate Jaro-Winkler Distance.
    """
    return 1 - jaro_winkler_similarity(text1, text2)

def calculate_honore_statistic(text):
    """
    Calculate Honore’s Statistic.
    """
    words = word_tokenize(text.lower())
    freq = Counter(words)
    v1 = sum(1 for word in freq if freq[word] == 1)
    n = len(words)
    return 100 * math.log(n) / (1 - (v1 / n)) if n > 0 else 0

def calculate_sichel_measure(text):
    """
    Calculate Sichel’s Measure.
    """
    words = word_tokenize(text.lower())
    freq = Counter(words)
    v2 = sum(1 for word in freq if freq[word] == 2)
    v = len(freq)
    return v2 / v if v > 0 else 0

def calculate_brunet_measure(text):
    """
    Calculate Brunet’s Measure.
    """
    words = word_tokenize(text.lower())
    freq = Counter(words)
    v = len(freq)
    n = len(words)
    return n ** (v ** -0.165) if v > 0 and n > 0 else 0

def calculate_yule_characteristic_k(text):
    """
    Calculate Yule’s Characteristic K.
    """
    words = word_tokenize(text.lower())
    freq = Counter(words)
    m1 = sum(freq.values())
    m2 = sum(freq[word] ** 2 for word in freq)
    return 10000 * (m2 - m1) / (m1 ** 2) if m1 > 0 else 0

def calculate_mtld(text):
    """
    Calculate MTLD (Measure of Textual Lexical Diversity).
    """
    words = word_tokenize(text.lower())
    return ld.mtld(words)

def calculate_hdd(text):
    """
    Calculate HD-D (Hypergeometric Distribution D).
    """
    words = word_tokenize(text.lower())
    return ld.hdd(words)

def calculate_variability_index(text):
    """
    Calculate Variability Index.
    """
    words = word_tokenize(text.lower())
    freq = Counter(words)
    v = len(freq)
    n = len(words)
    return v / n if n > 0 else 0

def normalize_metric(value, min_value, max_value):
    """
    Normalize metrics to a range of 0 to 1.
    """
    return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

def evaluate_statistical_metrics(text):
    """
    Evaluate various statistical metrics for the provided text.
    """
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

    normalized_metrics = {
        "Jaro-Winkler Distance": normalize_metric(metrics["Jaro-Winkler Distance"], 0, 1),
        "Honore’s Statistic": normalize_metric(metrics["Honore’s Statistic"], 0, 2000),
        "Sichel’s Measure": normalize_metric(metrics["Sichel’s Measure"], 0, 1),
        "Brunet’s Measure": normalize_metric(metrics["Brunet’s Measure"], 0, 20),
        "Yule’s Characteristic K": normalize_metric(metrics["Yule’s Characteristic K"], 0, 200),
        "MTLD (Measure of Textual Lexical Diversity)": normalize_metric(metrics["MTLD (Measure of Textual Lexical Diversity)"], 0, 200),
        "HD-D (Hypergeometric Distribution D)": normalize_metric(metrics["HD-D (Hypergeometric Distribution D)"], 0, 1),
        "Variability Index": normalize_metric(metrics["Variability Index"], 0, 1)
    }

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
    """
    Main function to read JSON file, evaluate metrics, and save results.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
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

    output_file_path = file_path.replace(".json", "_metrics_statistical.json")
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_statistical_metrics.py <file_path>")
        sys.exit(1)

    FILE_PATH = sys.argv[1]
    main(FILE_PATH)
