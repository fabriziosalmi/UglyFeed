"""
Module for evaluating JSON file comparisons using various metrics.
"""

import json
import os
import difflib
import math
from collections import Counter
from functools import reduce

import nltk
import numpy as np
import pandas as pd
import spacy
import textstat
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from jiwer import wer

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Load spacy model
nlp = spacy.load("en_core_web_sm")

OUTPUT_FOLDER = "output"
REWRITTEN_FOLDER = "rewritten"
RESULTS_JSON_PATH = "reports/evaluation_results.json"
RESULTS_HTML_PATH = "reports/evaluation_results.html"

def normalize_for_aggregated_score(scores, reference):
    """
    Normalize scores for aggregated score calculation.
    """
    max_values = {
        "Edit Distance": len(reference),
        "WER": 1,
        "CIDEr": 10,
        "Hamming Distance": len(reference),
        "Levenshtein Distance": len(reference),
    }

    normalized_scores = {}

    for metric in scores:
        if metric in max_values:
            if metric in ["Edit Distance", "WER", "Hamming Distance", "Levenshtein Distance"]:
                normalized_scores[metric] = (1 - (scores[metric] / max_values[metric])) * 100
            else:
                normalized_scores[metric] = (scores[metric] / max_values[metric]) * 100
        elif metric in [
            "BLEU-1", "Jaccard Similarity", "ROUGE-L", "TF-IDF Cosine Similarity",
            "METEOR", "BoW Cosine Similarity", "F1 Score", "Overlap Coefficient",
            "Dice Coefficient", "Longest Common Subsequence", "Type-Token Ratio",
            "Lexical Diversity", "Sentiment Analysis"
        ]:
            normalized_scores[metric] = scores[metric] * 100
        elif metric in [
            "Gunning Fog Index", "Automated Readability Index", "Entropy",
            "Readability Score", "SMOG Index", "ARI Score", "NIST Score", "LSA Similarity",
            "Lexical Density", "Coleman Liau Index"
        ]:
            normalized_scores[metric] = (1 - (scores[metric] / max_values.get(metric, 100))) * 100
        else:
            normalized_scores[metric] = scores[metric]

    return normalized_scores

def compare_json_files(output_file, rewritten_file):
    """
    Compare two JSON files using various metrics.
    """
    with open(output_file, "r", encoding="utf-8") as f1, open(rewritten_file, "r", encoding="utf-8") as f2:
        try:
            data1 = json.load(f1)
            data2 = json.load(f2)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON format in {output_file} or {rewritten_file}")
            return None

    reference = flatten_json(data1)
    candidate = flatten_json(data2)

    scores = {
        "Output File": output_file,
        "BLEU-1": calculate_bleu(reference, candidate, n=1),
        "Jaccard Similarity": jaccard_similarity(reference, candidate),
        "ROUGE-L": rouge_l_similarity(reference, candidate),
        "TF-IDF Cosine Similarity": tfidf_cosine_similarity(reference, candidate),
        "METEOR": calculate_meteor(reference, candidate),
        "Edit Distance": calculate_edit_distance(reference, candidate),
        "BoW Cosine Similarity": bow_cosine_similarity(reference, candidate),
        "WER": calculate_wer(reference, candidate),
        "CIDEr": calculate_cider(reference, candidate),
        "Hamming Distance": hamming_distance(reference, candidate),
        "F1 Score": f1_score(reference, candidate),
        "Overlap Coefficient": overlap_coefficient(reference, candidate),
        "Dice Coefficient": dice_coefficient(reference, candidate),
        "Longest Common Subsequence": longest_common_subsequence(reference, candidate),
        "Levenshtein Distance": levenshtein_distance(reference, candidate),
        "Readability Score": readability_score(" ".join(reference), " ".join(candidate)),
        "Sentence BLEU": custom_sentence_bleu(" ".join(reference), " ".join(candidate)),
        "SMOG Index": smog_index(" ".join(reference), " ".join(candidate)),
        "ARI Score": ari_score(" ".join(reference), " ".join(candidate)),
        "NIST Score": nist_score(reference, candidate),
        "LSA Similarity": lsa_similarity(" ".join(reference), " ".join(candidate)),
        "Sentiment Analysis": sentiment_analysis(" ".join(reference), " ".join(candidate)),
        "Lexical Density": lexical_density(" ".join(reference), " ".join(candidate)),
        "Gunning Fog Index": gunning_fog_index(" ".join(reference), " ".join(candidate)),
        "Coleman Liau Index": coleman_liau_index(" ".join(reference), " ".join(candidate)),
        "Automated Readability Index": automated_readability_index(" ".join(reference), " ".join(candidate))
    }

    normalized_scores = normalize_for_aggregated_score(scores, reference)

    weights = {
        "BLEU-1": 0.10,
        "Jaccard Similarity": 0.05,
        "ROUGE-L": 0.08,
        "TF-IDF Cosine Similarity": 0.10,
        "METEOR": 0.10,
        "Edit Distance": 0.07,
        "BoW Cosine Similarity": 0.06,
        "WER": 0.07,
        "CIDEr": 0.03,
        "Hamming Distance": 0.01,
        "F1 Score": 0.07,
        "Overlap Coefficient": 0.03,
        "Dice Coefficient": 0.03,
        "Longest Common Subsequence": 0.03,
        "Levenshtein Distance": 0.03,
        "Readability Score": 0.01,
        "Sentence BLEU": 0.02,
        "SMOG Index": 0.01,
        "ARI Score": 0.01,
        "NIST Score": 0.08,
        "LSA Similarity": 0.02,
        "Sentiment Analysis": 0.02,
        "Lexical Density": 0.02,
        "Gunning Fog Index": 0.01,
        "Coleman Liau Index": 0.01,
        "Automated Readability Index": 0.01
    }

    aggregated_score = sum(weights[metric] * normalized_scores[metric] for metric in weights)
    scores["Ugly Score"] = aggregated_score

    return scores

def save_individual_metrics(output_file, metrics):
    """
    Save individual metrics to a JSON file.
    """
    filename = os.path.basename(output_file).replace("_rewritten.json", "_metrics_comparison.json")
    path = os.path.join(REWRITTEN_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

def calculate_bleu(reference, candidate, n=4):
    """
    Calculate BLEU score for the given reference and candidate.
    """
    precisions = []
    for i in range(1, n + 1):
        ref_ngrams = Counter(zip(*[reference[j:] for j in range(i)]))
        cand_ngrams = Counter(zip(*[candidate[j:] for j in range(i)]))
        precision = sum((ref_ngrams & cand_ngrams).values()) / max(1, sum(cand_ngrams.values()))
        precisions.append(precision)

    if min(precisions) > 0:
        bp = brevity_penalty(reference, candidate)
        bleu_score = bp * geometric_mean(precisions)
    else:
        bleu_score = 0.0

    return bleu_score

def custom_sentence_bleu(references, hypothesis):
    """
    Custom BLEU score calculation for sentences.
    """
    references = references.split()
    hypothesis = hypothesis.split()
    return custom_bleu(references, hypothesis)

def custom_bleu(list_of_references, hypotheses):
    """
    Custom BLEU score calculation.
    """
    weights = [0.25, 0.25, 0.25, 0.25]
    p_n = [modified_precision(list_of_references, hypotheses, i) for i in range(1, 5)]
    s = (w * math.log(p_i) if p_i > 0 else 0 for w, p_i in zip(weights, p_n))
    return math.exp(sum(s))

def modified_precision(references, hypothesis, n):
    """
    Calculate modified precision for BLEU score.
    """
    ref_ngrams = Counter(ngram for reference in references for ngram in zip(*[reference[i:] for i in range(n)]))
    hyp_ngrams = Counter(ngram for ngram in zip(*[hypothesis[i:] for i in range(n)]))
    numerator = sum((hyp_ngrams & ref_ngrams).values())
    denominator = max(1, sum(hyp_ngrams.values()))
    return numerator / denominator

def geometric_mean(precisions):
    """
    Calculate geometric mean of precisions.
    """
    return (reduce(lambda x, y: x * y, precisions)) ** (1.0 / len(precisions))

def brevity_penalty(reference, candidate):
    """
    Calculate brevity penalty for BLEU score.
    """
    ref_length = len(reference)
    cand_length = len(candidate)
    if cand_length <= ref_length:
        return 1
    return math.exp(1 - (ref_length / cand_length))

def flatten_json(data, prefix=""):
    """
    Flatten a nested JSON structure.
    """
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
    """
    Calculate Jaccard similarity between two lists.
    """
    set1 = set(list1)
    set2 = set(list2)
    return len(set1.intersection(set2)) / len(set1.union(set2))

def rouge_l_similarity(reference, candidate):
    """
    Calculate ROUGE-L similarity between reference and candidate.
    """
    lcs = difflib.SequenceMatcher(None, reference, candidate).find_longest_match(
        0, len(reference), 0, len(candidate)
    )
    return (lcs.size * 2) / (len(reference) + len(candidate))

def tfidf_cosine_similarity(reference, candidate):
    """
    Calculate TF-IDF cosine similarity between reference and candidate.
    """
    vectorizer = TfidfVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    tfidf_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def calculate_meteor(reference, candidate):
    """
    Calculate METEOR score for reference and candidate.
    """
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    ref_tokens = word_tokenize(ref_string)
    cand_tokens = word_tokenize(cand_string)
    return meteor_score([ref_tokens], cand_tokens)

def calculate_edit_distance(reference, candidate):
    """
    Calculate edit distance between reference and candidate.
    """
    return difflib.SequenceMatcher(None, reference, candidate).ratio()

def bow_cosine_similarity(reference, candidate):
    """
    Calculate Bag-of-Words cosine similarity between reference and candidate.
    """
    vectorizer = CountVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    bow_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]

def calculate_wer(reference, candidate):
    """
    Calculate Word Error Rate (WER) between reference and candidate.
    """
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    return wer(ref_string, cand_string)

def calculate_cider(reference, candidate):
    """
    Calculate CIDEr score for reference and candidate.
    """
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

def hamming_distance(reference, candidate):
    """
    Calculate Hamming distance between reference and candidate.
    """
    return sum(el1 != el2 for el1, el2 in zip(reference, candidate)) + abs(
        len(reference) - len(candidate)
    )

def f1_score(reference, candidate):
    """
    Calculate F1 score for reference and candidate.
    """
    ref_tokens = set(reference)
    cand_tokens = set(candidate)

    tp = len(ref_tokens & cand_tokens)
    fp = len(cand_tokens - ref_tokens)
    fn = len(ref_tokens - cand_tokens)

    if tp + fp == 0 or tp + fn == 0:
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)

def overlap_coefficient(reference, candidate):
    """
    Calculate overlap coefficient between reference and candidate.
    """
    ref_set = set(reference)
    cand_set = set(candidate)
    return len(ref_set & cand_set) / min(len(ref_set), len(cand_set))

def dice_coefficient(reference, candidate):
    """
    Calculate Dice coefficient between reference and candidate.
    """
    ref_set = set(reference)
    cand_set = set(candidate)
    return 2 * len(ref_set & cand_set) / (len(ref_set) + len(cand_set))

def longest_common_subsequence(reference, candidate):
    """
    Calculate longest common subsequence between reference and candidate.
    """
    matcher = difflib.SequenceMatcher(None, reference, candidate)
    match = matcher.find_longest_match(0, len(reference), 0, len(candidate))
    return match.size

def levenshtein_distance(reference, candidate):
    """
    Calculate Levenshtein distance between reference and candidate.
    """
    d = [[i + j for j in range(len(candidate) + 1)] for i in range(len(reference) + 1)]
    for i in range(1, len(reference) + 1):
        for j in range(1, len(candidate) + 1):
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + (reference[i - 1] != candidate[j - 1]),
            )
    return d[len(reference)][len(candidate)]

def readability_score(reference, candidate):
    """
    Calculate readability score for reference and candidate.
    """
    return (textstat.flesch_reading_ease(reference) + textstat.flesch_reading_ease(candidate)) / 2

def smog_index(reference, candidate):
    """
    Calculate SMOG index for reference and candidate.
    """
    return (textstat.smog_index(reference) + textstat.smog_index(candidate)) / 2

def ari_score(reference, candidate):
    """
    Calculate ARI score for reference and candidate.
    """
    return (textstat.automated_readability_index(reference) + textstat.automated_readability_index(candidate)) / 2

def nist_score(reference, candidate):
    """
    Calculate NIST score for reference and candidate.
    """
    return nltk.translate.nist_score.sentence_nist([reference], candidate)

def lsa_similarity(reference, candidate):
    """
    Calculate LSA similarity between reference and candidate.
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([reference, candidate])
    svd = TruncatedSVD(n_components=1)
    X_lsa = svd.fit_transform(X)
    return cosine_similarity(X_lsa[0:1], X_lsa[1:2])[0][0]

def sentiment_analysis(reference, candidate):
    """
    Perform sentiment analysis on reference and candidate.
    """
    ref_sentiment = TextBlob(reference).sentiment.polarity
    cand_sentiment = TextBlob(candidate).sentiment.polarity
    return 1 - abs(ref_sentiment - cand_sentiment)

def lexical_density(reference, candidate):
    """
    Calculate lexical density for reference and candidate.
    """
    def calculate_lexical_density(text):
        words = word_tokenize(text)
        lexical_words = [word for word in words if word.isalpha()]
        return len(lexical_words) / len(words) if words else 0

    ref_lexical_density = calculate_lexical_density(reference)
    cand_lexical_density = calculate_lexical_density(candidate)
    return (ref_lexical_density + cand_lexical_density) / 2

def gunning_fog_index(reference, candidate):
    """
    Calculate Gunning Fog index for reference and candidate.
    """
    return (textstat.gunning_fog(reference) + textstat.gunning_fog(candidate)) / 2

def coleman_liau_index(reference, candidate):
    """
    Calculate Coleman-Liau index for reference and candidate.
    """
    return (textstat.coleman_liau_index(reference) + textstat.coleman_liau_index(candidate)) / 2

def automated_readability_index(reference, candidate):
    """
    Calculate Automated Readability Index for reference and candidate.
    """
    return (textstat.automated_readability_index(reference) + textstat.automated_readability_index(candidate)) / 2

def save_results_to_json(results, path):
    """
    Save evaluation results to a JSON file.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

def save_results_to_html(results, path):
    """
    Save evaluation results to an HTML file.
    """
    df = pd.DataFrame(results)
    html = df.to_html(
        index=False, classes="table table-striped table-hover table-bordered"
    )

    with open(path, "w", encoding="utf-8") as f:
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

def main():
    """
    Main function to evaluate JSON files and save results.
    """
    rewritten_files = [f for f in os.listdir(REWRITTEN_FOLDER) if f.endswith("_rewritten.json")]

    all_results = []
    for rewritten_file in rewritten_files:
        rewritten_path = os.path.join(REWRITTEN_FOLDER, rewritten_file)

        output_file = rewritten_file.replace("_rewritten.json", ".json")
        output_path = os.path.join(OUTPUT_FOLDER, output_file)

        if os.path.isfile(output_path):
            print("\nEvaluating:", output_file)
            result = compare_json_files(output_path, rewritten_path)
            if result:
                all_results.append(result)
                save_individual_metrics(output_path, result)
        else:
            print(f"WARNING: No corresponding file found in 'output' for {rewritten_file}")

    save_results_to_json(all_results, RESULTS_JSON_PATH)
    save_results_to_html(all_results, RESULTS_HTML_PATH)

    print(f"Results saved to {RESULTS_JSON_PATH} and {RESULTS_HTML_PATH}")

if __name__ == "__main__":
    main()
