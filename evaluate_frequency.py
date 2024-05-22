import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from collections import Counter
import sys
import numpy as np
import textstat

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("stopwords", quiet=True)

def bigram_frequency(text):
    words = word_tokenize(text)
    bigrams = list(ngrams(words, 2))
    bigram_counts = Counter(bigrams)
    return bigram_counts

def trigram_frequency(text):
    words = word_tokenize(text)
    trigrams = list(ngrams(words, 3))
    trigram_counts = Counter(trigrams)
    return trigram_counts

def stopword_ratio(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = word_tokenize(text)
    stopword_count = sum(1 for word in words if word in stopwords)
    return stopword_count / len(words) if words else 0

def function_word_frequency(text):
    function_words = set(nltk.corpus.stopwords.words('english'))
    words = word_tokenize(text)
    function_word_count = Counter(word for word in words if word in function_words)
    return function_word_count

def hapax_legomena_ratio(text):
    words = word_tokenize(text)
    word_counts = Counter(words)
    hapax_legomena = sum(1 for word in word_counts if word_counts[word] == 1)
    return hapax_legomena / len(words) if words else 0

def hapax_dislegomena_ratio(text):
    words = word_tokenize(text)
    word_counts = Counter(words)
    hapax_dislegomena = sum(1 for word in word_counts if word_counts[word] == 2)
    return hapax_dislegomena / len(words) if words else 0

def mean_sentence_length(text):
    sentences = sent_tokenize(text)
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
    return np.mean(sentence_lengths) if sentence_lengths else 0

def mean_word_length(text):
    words = word_tokenize(text)
    word_lengths = [len(word) for word in words]
    return np.mean(word_lengths) if word_lengths else 0

def syllable_per_word(text):
    words = word_tokenize(text)
    syllable_count = sum(textstat.syllable_count(word) for word in words)
    return syllable_count / len(words) if words else 0

def clause_per_sentence(text):
    sentences = sent_tokenize(text)
    clause_count = sum(sentence.count(',') + 1 for sentence in sentences)  # Approximation
    return clause_count / len(sentences) if sentences else 0

def punctuation_frequency(text):
    words = word_tokenize(text)
    punctuation = set(['.', ',', '!', '?', ':', ';', '-', '(', ')', '"', "'"])
    punctuation_count = Counter(word for word in words if word in punctuation)
    return punctuation_count

def evaluate_frequency_metrics(text):
    metrics = {
        "Stopword Ratio": stopword_ratio(text),
        "Hapax Legomena Ratio": hapax_legomena_ratio(text),
        "Hapax Dislegomena Ratio": hapax_dislegomena_ratio(text),
        "Mean Sentence Length": mean_sentence_length(text),
        "Mean Word Length": mean_word_length(text),
        "Syllable per Word": syllable_per_word(text),
        "Clause per Sentence": clause_per_sentence(text),
    }

    # Calculate aggregated score (customizable weights)
    weights = {
        "Stopword Ratio": 0.1,
        "Hapax Legomena Ratio": 0.1,
        "Hapax Dislegomena Ratio": 0.1,
        "Mean Sentence Length": 0.1,
        "Mean Word Length": 0.1,
        "Syllable per Word": 0.1,
        "Clause per Sentence": 0.1,
    }

    aggregated_score = sum(metrics[metric] * weights.get(metric, 0) for metric in metrics)

    return metrics, aggregated_score

def main(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        text = data.get("content", "")

    if not text:
        print("No content found in the provided JSON file.")
        return

    metrics, aggregated_score = evaluate_frequency_metrics(text)

    output = {
        "Text Frequency Metrics": metrics,
        "Aggregated Frequency Score": aggregated_score
    }

    print("Text Frequency Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"Aggregated Frequency Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_frequency.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_frequency.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
