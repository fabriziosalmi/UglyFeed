import json
import os
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math
from functools import reduce

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")

output_folder = "output"
rewritten_folder = "rewritten"
results_json_path = "evaluation_results.json"
results_html_path = "evaluation_results.html"


def compare_json_files(output_file, rewritten_file):
    """Compares JSON files, calculates multiple metrics, and aggregates them."""

    with open(output_file, "r") as f1, open(rewritten_file, "r") as f2:
        try:
            data1 = json.load(f1)
            data2 = json.load(f2)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON format in {output_file} or {rewritten_file}")
            return None

    # Flatten JSON to lists of strings
    reference = flatten_json(data1)
    candidate = flatten_json(data2)

    # Calculate metrics
    bleu1 = calculate_bleu(reference, candidate, n=1, smoothing=SmoothingFunction())
    jaccard = jaccard_similarity(reference, candidate)
    rouge_l = rouge_l_similarity(reference, candidate)
    tfidf_cosine = tfidf_cosine_similarity(reference, candidate)
    meteor = calculate_meteor(reference, candidate)
    edit_distance = calculate_edit_distance(reference, candidate)
    bow_cosine = bow_cosine_similarity(reference, candidate)
    wer_score = calculate_wer(reference, candidate)
    cider_score = calculate_cider(reference, candidate)
    hamming = hamming_distance(reference, candidate)
    f1 = f1_score(reference, candidate)
    overlap = overlap_coefficient(reference, candidate)
    dice = dice_coefficient(reference, candidate)
    lcs = longest_common_subsequence(reference, candidate)
    levenshtein = levenshtein_distance(reference, candidate)
    avg_token_len = average_token_length(reference)
    ttr = type_token_ratio(reference)
    gunning_fog = gunning_fog_index(reference)
    ari = automated_readability_index(reference)
    lex_div = lexical_diversity(reference)
    synt_comp = syntactic_complexity(reference)
    perplexity = calculate_perplexity(reference)
    readability = readability_consensus(reference)
    ent = entropy(reference)
    sub_score = subjectivity_score(reference)

    # Store metrics in a dictionary
    scores = {
        "Output File": output_file,
        "BLEU-1": bleu1,
        "Jaccard Similarity": jaccard,
        "ROUGE-L": rouge_l,
        "TF-IDF Cosine Similarity": tfidf_cosine,
        "METEOR": meteor,
        "Edit Distance": edit_distance,
        "BoW Cosine Similarity": bow_cosine,
        "WER": wer_score,
        "CIDEr": cider_score,
        "Hamming Distance": hamming,
        "F1 Score": f1,
        "Overlap Coefficient": overlap,
        "Dice Coefficient": dice,
        "Longest Common Subsequence": lcs,
        "Levenshtein Distance": levenshtein,
        "Average Token Length": avg_token_len,
        "Type-Token Ratio": ttr,
        "Gunning Fog Index": gunning_fog,
        "Automated Readability Index": ari,
        "Lexical Diversity": lex_div,
        "Syntactic Complexity": synt_comp,
        "Perplexity": perplexity,
        "Readability Consensus": readability,
        "Entropy": ent,
        "Subjectivity Score": sub_score,
    }

    # Calculate Aggregated Score (weighted average, customizable)
    weights = {
        "BLEU-1": 0.1,  # Higher weight for n-gram precision
        "Jaccard Similarity": 0.05,  # Moderate weight for token overlap
        "ROUGE-L": 0.1,  # Higher weight for sequence matching
        "TF-IDF Cosine Similarity": 0.1,  # High weight for semantic similarity
        "METEOR": 0.1,  # High weight for overall content quality
        "Edit Distance": 0.05,  # Moderate weight for precise character-level matching
        "BoW Cosine Similarity": 0.1,  # High weight for word occurrence similarity
        "WER": 0.05,  # Moderate weight for word error rate
        "CIDEr": 0.05,  # Moderate weight for detail relevance
        "Hamming Distance": 0.03,  # Lower weight for binary differences
        "F1 Score": 0.1,  # High weight for combined precision and recall
        "Overlap Coefficient": 0.05,  # Moderate weight for set overlap
        "Dice Coefficient": 0.05,  # Moderate weight similar to F1
        "Longest Common Subsequence": 0.05,  # Moderate weight for sequence similarity
        "Levenshtein Distance": 0.05,  # Moderate weight for minimal edits
        "Average Token Length": 0.02,  # Lower weight for readability
        "Type-Token Ratio": 0.02,  # Lower weight for lexical diversity
        "Gunning Fog Index": 0.03,  # Lower weight for readability
        "Automated Readability Index": 0.03,  # Lower weight for readability
        "Lexical Diversity": 0.05,  # Moderate weight for vocabulary variety
        "Syntactic Complexity": 0.05,  # Moderate weight for sentence structure complexity
        "Perplexity": 0.05,  # Moderate weight for predictability of text
        "Readability Consensus": 0.05,  # Moderate weight for aggregated readability score
        "Entropy": 0.05,  # Moderate weight for text complexity
        "Subjectivity Score": 0.05,  # Moderate weight for subjectivity level
    }

    aggregated_score = sum(weights[metric] * scores[metric] for metric in weights)
    scores["Aggregated Score"] = aggregated_score

    return scores


def calculate_bleu(reference, candidate, n=4, smoothing=None):
    """Calculates BLEU score for the given n-gram order."""
    precisions = []
    for i in range(1, n + 1):
        ref_ngrams = Counter(zip(*[reference[j:] for j in range(i)]))
        cand_ngrams = Counter(zip(*[candidate[j:] for j in range(i)]))
        precision = sum((ref_ngrams & cand_ngrams).values()) / max(
            1, sum(cand_ngrams.values())
        )
        precisions.append(precision)

    if min(precisions) > 0:
        bp = brevity_penalty(reference, candidate)
        bleu_score = bp * geometric_mean(precisions)
    else:
        bleu_score = 0.0

    return bleu_score


def geometric_mean(precisions):
    """Calculates the geometric mean of a list of precisions."""
    return (reduce(lambda x, y: x * y, precisions)) ** (1.0 / len(precisions))


def brevity_penalty(reference, candidate):
    """Calculates the brevity penalty for BLEU."""
    ref_length = len(reference)
    cand_length = len(candidate)
    if cand_length <= ref_length:
        return 1
    else:
        return math.exp(1 - (ref_length / cand_length))


def flatten_json(data, prefix=""):
    """Flattens a nested JSON structure into a list of strings."""
    flattened = []
    if isinstance(data, dict):
        for key, value in data.items():
            flattened.extend(flatten_json(value, prefix + key + "."))
    elif isinstance(data, list):
        for i, value in enumerate(data):
            flattened.extend(flatten_json(value, prefix + str(i) + "."))
    else:
        flattened.append(str(data))
    return flattened


def jaccard_similarity(list1, list2):
    """Calculates Jaccard similarity between two lists."""
    set1 = set(list1)
    set2 = set(list2)
    return len(set1.intersection(set2)) / len(set1.union(set2))


def rouge_l_similarity(reference, candidate):
    """Calculates ROUGE-L similarity (Longest Common Subsequence)."""
    lcs = difflib.SequenceMatcher(None, reference, candidate).find_longest_match(
        0, len(reference), 0, len(candidate)
    )
    return (lcs.size * 2) / (len(reference) + len(candidate))


def tfidf_cosine_similarity(reference, candidate):
    """Calculates cosine similarity using TF-IDF vectors."""
    vectorizer = TfidfVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    tfidf_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def calculate_meteor(reference, candidate):
    """Calculates METEOR score."""
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    ref_tokens = word_tokenize(ref_string)
    cand_tokens = word_tokenize(cand_string)
    return meteor_score([ref_tokens], cand_tokens)


def calculate_edit_distance(reference, candidate):
    """Calculates Edit Distance."""
    return difflib.SequenceMatcher(None, reference, candidate).ratio()


def bow_cosine_similarity(reference, candidate):
    """Calculates cosine similarity using Bag of Words (BoW) vectors."""
    vectorizer = CountVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    bow_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]


# ADDITIONAL METRICS
from jiwer import wer
import numpy as np


def calculate_wer(reference, candidate):
    """Calculates Word Error Rate (WER)."""
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    return wer(ref_string, cand_string)


def calculate_cider(reference, candidate):
    """Calculates CIDEr score."""

    def tokenize(text):
        return [word_tokenize(sent) for sent in nltk.sent_tokenize(text)]

    def compute_tf(text):
        tf = Counter()
        for sent in text:
            tf.update(sent)
        return tf

    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)

    reference_tokens = tokenize(ref_string)
    candidate_tokens = tokenize(cand_string)

    ref_tf = compute_tf(reference_tokens)
    cand_tf = compute_tf(candidate_tokens)

    all_tokens = set(ref_tf.keys()).union(set(cand_tf.keys()))

    ref_vector = np.array([ref_tf[token] for token in all_tokens])
    cand_vector = np.array([cand_tf[token] for token in all_tokens])

    ref_norm = np.linalg.norm(ref_vector)
    cand_norm = np.linalg.norm(cand_vector)

    if ref_norm == 0 or cand_norm == 0:
        return 0.0

    tf_cosine = np.dot(ref_vector, cand_vector) / (ref_norm * cand_norm)

    idf = {
        token: np.log((len(reference_tokens) + 1) / (1 + ref_tf[token])) + 1
        for token in all_tokens
    }

    ref_idf_vector = np.array([idf[token] * ref_tf[token] for token in all_tokens])
    cand_idf_vector = np.array([idf[token] * cand_tf[token] for token in all_tokens])

    idf_norm = np.linalg.norm(ref_idf_vector)

    if idf_norm == 0:
        return 0.0

    cider_score = np.dot(ref_idf_vector, cand_idf_vector) / idf_norm

    return cider_score


import difflib
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")


def hamming_distance(reference, candidate):
    """Calculates the Hamming distance between two lists."""
    return sum(el1 != el2 for el1, el2 in zip(reference, candidate)) + abs(
        len(reference) - len(candidate)
    )


def f1_score(reference, candidate):
    """Calculates the F1 score based on token overlap."""
    ref_tokens = set(reference)
    cand_tokens = set(candidate)

    tp = len(ref_tokens & cand_tokens)
    fp = len(cand_tokens - ref_tokens)
    fn = len(ref_tokens - cand_tokens)

    if tp + fp == 0 or tp + fn == 0:
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    return 2 * (precision * recall) / (precision + recall)


def overlap_coefficient(reference, candidate):
    """Calculates the overlap coefficient between two lists."""
    ref_set = set(reference)
    cand_set = set(candidate)
    return len(ref_set & cand_set) / min(len(ref_set), len(cand_set))


def dice_coefficient(reference, candidate):
    """Calculates the Dice coefficient between two lists."""
    ref_set = set(reference)
    cand_set = set(candidate)
    return 2 * len(ref_set & cand_set) / (len(ref_set) + len(cand_set))


def longest_common_subsequence(reference, candidate):
    """Calculates the length of the longest common subsequence."""
    matcher = difflib.SequenceMatcher(None, reference, candidate)
    match = matcher.find_longest_match(0, len(reference), 0, len(candidate))
    return match.size


def levenshtein_distance(reference, candidate):
    """Calculates the Levenshtein distance between two lists."""
    d = [[i + j for j in range(len(candidate) + 1)] for i in range(len(reference) + 1)]
    for i in range(1, len(reference) + 1):
        for j in range(1, len(candidate) + 1):
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + (reference[i - 1] != candidate[j - 1]),
            )
    return d[len(reference)][len(candidate)]


def average_token_length(text):
    """Calculates the average token length in a list."""
    return sum(len(token) for token in text) / len(text) if text else 0


def type_token_ratio(text):
    """Calculates the type-token ratio (TTR) of a list."""
    return len(set(text)) / len(text) if text else 0


def gunning_fog_index(text):
    """Calculates the Gunning Fog index of a list."""
    text_str = " ".join(text)
    words = word_tokenize(text_str)
    num_words = len(words)
    num_sentences = text_str.count(".") + text_str.count("!") + text_str.count("?")
    num_complex_words = len([word for word in words if len(word) > 7])
    if num_sentences == 0 or num_words == 0:
        return 0
    return 0.4 * ((num_words / num_sentences) + 100 * (num_complex_words / num_words))


def automated_readability_index(text):
    """Calculates the Automated Readability Index (ARI) of a list."""
    text_str = " ".join(text)
    num_chars = sum(len(word) for word in word_tokenize(text_str))
    num_words = len(word_tokenize(text_str))
    num_sentences = text_str.count(".") + text_str.count("!") + text_str.count("?")
    if num_words == 0 or num_sentences == 0:
        return 0
    return 4.71 * (num_chars / num_words) + 0.5 * (num_words / num_sentences) - 21.43


# ADDITIONAL METRICS 2
from nltk.tokenize import sent_tokenize
from textstat import textstat
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as cosine_sim

# from transformers import pipeline

# Ensure nltk resources are downloaded
nltk.download("averaged_perceptron_tagger")

# Load sentiment analysis pipeline
# sentiment_pipeline = pipeline("sentiment-analysis")


def lexical_diversity(text):
    """Calculates lexical diversity of the text."""
    return len(set(text)) / len(text) if text else 0


def syntactic_complexity(text):
    """Calculates syntactic complexity based on average sentence length and POS tags."""
    sentences = sent_tokenize(" ".join(text))
    if not sentences:
        return 0
    avg_sentence_length = sum(
        len(word_tokenize(sentence)) for sentence in sentences
    ) / len(sentences)
    pos_tags = [nltk.pos_tag(word_tokenize(sentence)) for sentence in sentences]
    num_complex_sentences = sum(
        1 for tags in pos_tags if any(tag in ["JJ", "RB", "VB"] for _, tag in tags)
    )
    return avg_sentence_length + num_complex_sentences / len(sentences)


def calculate_perplexity(text):
    """Calculates the perplexity of the text using a language model."""
    # Dummy implementation, requires a language model to compute perplexity
    return len(text)  # Placeholder


def readability_consensus(text):
    """Calculates a readability consensus score using multiple readability indices."""
    text_str = " ".join(text)
    return (
        textstat.flesch_reading_ease(text_str)
        + textstat.smog_index(text_str)
        + textstat.flesch_kincaid_grade(text_str)
        + textstat.coleman_liau_index(text_str)
        + textstat.automated_readability_index(text_str)
        + textstat.dale_chall_readability_score(text_str)
        + textstat.difficult_words(text_str)
        + textstat.linsear_write_formula(text_str)
        + textstat.gunning_fog(text_str)
    )


def entropy(text):
    """Calculates the entropy of the text."""
    freq = Counter(text)
    probs = [freq[key] / len(text) for key in freq]
    return -sum(p * math.log(p, 2) for p in probs)


def subjectivity_score(text):
    """Calculates the subjectivity score of the text."""
    text_str = " ".join(text)
    # Dummy implementation, a real implementation would use a subjectivity model
    return textstat.text_standard(text_str, float_output=True) / 100  # Placeholder


def save_results_to_json(results, path):
    """Saves the evaluation results to a JSON file."""
    with open(path, "w") as f:
        json.dump(results, f, indent=4)


def save_results_to_html(results, path):
    """Saves the evaluation results to an HTML file."""
    df = pd.DataFrame(results)
    html = df.to_html(
        index=False, classes="table table-striped table-hover table-bordered"
    )

    with open(path, "w") as f:
        f.write(
            """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Evaluation Results</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body { margin: 20px; }
                .table-container { margin-top: 20px; }
                h1 { text-align: center; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Evaluation Results</h1>
                <div class="table-container">
        """
        )
        f.write(html)
        f.write(
            """
                </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        """
        )


# Get all JSON files in the rewritten folder
rewritten_files = [f for f in os.listdir(rewritten_folder) if f.endswith(".json")]

# Collect all evaluation results
all_results = []
for rewritten_file in rewritten_files:
    rewritten_path = os.path.join(rewritten_folder, rewritten_file)

    # Remove the "_rewritten" part from the rewritten filename to get the original
    output_file = rewritten_file.replace("_rewritten.json", ".json")
    output_path = os.path.join(output_folder, output_file)

    if os.path.isfile(output_path):
        print("\nEvaluating:", output_file)  # Print the original filename
        result = compare_json_files(output_path, rewritten_path)
        if result:
            all_results.append(result)
    else:
        print(f"WARNING: No corresponding file found in 'output' for {rewritten_file}")

# Save results to JSON and HTML
save_results_to_json(all_results, results_json_path)
save_results_to_html(all_results, results_html_path)

print(f"Results saved to {results_json_path} and {results_html_path}")
