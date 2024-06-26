"""
Module for evaluating readability and complexity metrics in text using textstat and NLTK.
"""

import json
import sys
import nltk
import textstat
from langdetect import detect, LangDetectException

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

def detect_language(text):
    """
    Detect the language of the provided text.

    Parameters:
    text (str): The text to detect the language for.

    Returns:
    str: The detected language code (e.g., 'en', 'it').
    """
    try:
        return detect(text)
    except LangDetectException as err:
        print(f"Error detecting language: {err}")
        return 'it'  # Default to Italian

def calculate_syllable_count(text):
    """
    Calculate the syllable count of the text.

    Parameters:
    text (str): The text to calculate syllable count for.

    Returns:
    int: The syllable count.
    """
    return textstat.syllable_count(text)

def calculate_flesch_kincaid_grade(text):
    """
    Calculate the Flesch-Kincaid Grade Level of the text.

    Parameters:
    text (str): The text to calculate the Flesch-Kincaid Grade Level for.

    Returns:
    float: The Flesch-Kincaid Grade Level.
    """
    return textstat.flesch_kincaid_grade(text)

def calculate_smog_index(text):
    """
    Calculate the SMOG Index of the text.

    Parameters:
    text (str): The text to calculate the SMOG Index for.

    Returns:
    float: The SMOG Index.
    """
    return textstat.smog_index(text)

def calculate_readability_ease(text):
    """
    Calculate the Readability Ease Score of the text.

    Parameters:
    text (str): The text to calculate the Readability Ease Score for.

    Returns:
    float: The Readability Ease Score.
    """
    return textstat.flesch_reading_ease(text)

def evaluate_readability_complexity_metrics(text):
    """
    Evaluate readability and complexity metrics in the provided text.

    Parameters:
    text (str): The text to evaluate metrics for.

    Returns:
    tuple: A tuple containing:
        - metrics (dict): Dictionary of raw metric scores.
        - normalized_metrics (dict): Dictionary of normalized metric scores.
        - aggregated_score (float): The aggregated score.
    """
    metrics = {
        "Syllable Count": calculate_syllable_count(text),
        "Flesch-Kincaid Grade Level": calculate_flesch_kincaid_grade(text),
        "SMOG Index": calculate_smog_index(text),
        "Readability Ease Score": calculate_readability_ease(text)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable limits
    max_values = {
        "Syllable Count": 500,  # Example normalization, adjust as needed
        "Flesch-Kincaid Grade Level": 20,  # Example normalization, adjust as needed
        "SMOG Index": 20,  # Example normalization, adjust as needed
        "Readability Ease Score": 100  # Example normalization, adjust as needed
    }

    normalized_metrics = {
        key: min(metrics[key] / max_values[key], 1) for key in metrics
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Syllable Count": 0.2,
        "Flesch-Kincaid Grade Level": 0.3,
        "SMOG Index": 0.3,
        "Readability Ease Score": 0.2
    }

    aggregated_score = sum(
        normalized_metrics[metric] * weights[metric]
        for metric in normalized_metrics
    ) * 100

    return metrics, normalized_metrics, aggregated_score

def main(file_path):
    """
    Main function to process the input file and evaluate readability and complexity metrics.

    Parameters:
    file_path (str): The path to the JSON file containing the text to analyze.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            text = data.get("content", "")

        if not text:
            print("No content found in the provided JSON file.")
            return

        lang = detect_language(text)
        metrics, normalized_metrics, aggregated_score = (
            evaluate_readability_complexity_metrics(text)
        )

        output = {
            "Readability and Complexity Metrics": metrics,
            "Aggregated Readability and Complexity Score": aggregated_score
        }

        print("Text Readability and Complexity Metrics:")
        for metric, score in metrics.items():
            print(f"{metric}: {score:.4f}")
        print("\nNormalized Metrics:")
        for metric, score in normalized_metrics.items():
            print(f"{metric}: {score:.4f}")
        print(f"\nAggregated Readability and Complexity Score: "
              f"{aggregated_score:.4f}")

        # Export results to JSON
        output_file_path = file_path.replace(
            ".json", "_metrics_readability_complexity.json"
        )
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            json.dump(output, out_file, indent=4)
        print(f"Metrics exported to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The provided file is not a valid JSON file.")
    except Exception as err:  # Broad exception to catch unexpected errors
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_readability_complexity_metrics.py <file_path>")
        sys.exit(1)

    main(sys.argv[1])
