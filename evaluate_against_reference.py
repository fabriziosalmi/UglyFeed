import json
import os
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math
from functools import reduce
from sklearn.decomposition import TruncatedSVD
from textblob import TextBlob
import textstat
import spacy

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Load spacy model
nlp = spacy.load("en_core_web_sm")

output_folder = "output"
rewritten_folder = "rewritten"
results_json_path = "reports/evaluation_results.json"
results_html_path = "reports/evaluation_results.html"

def normalize_for_aggregated_score(scores, reference):
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
        elif metric in ["BLEU-1", "Jaccard Similarity", "ROUGE-L", "TF-IDF Cosine Similarity", "METEOR", "BoW Cosine Similarity", "F1 Score", "Overlap Coefficient", "Dice Coefficient", "Longest Common Subsequence", "Type-Token Ratio", "Lexical Diversity", "Sentiment Analysis"]:
            normalized_scores[metric] = scores[metric] * 100
        elif metric in ["Gunning Fog Index", "Automated Readability Index", "Entropy", "Readability Score", "SMOG Index", "ARI Score", "NIST Score", "LSA Similarity", "Lexical Density", "Gunning Fog Index", "Coleman Liau Index", "Automated Readability Index"]:
            normalized_scores[metric] = (1 - (scores[metric] / max_values.get(metric, 100))) * 100  # Default max value to 100 if not specified
        else:
            normalized_scores[metric] = scores[metric]

    return normalized_scores

def compare_json_files(output_file, rewritten_file):
    with open(output_file, "r") as f1, open(rewritten_file, "r") as f2:
        try:
            data1 = json.load(f1)
            data2 = json.load(f2)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON format in {output_file} or {rewritten_file}")
            return None

    reference = flatten_json(data1)
    candidate = flatten_json(data2)

    # Existing metrics
    bleu1 = calculate_bleu(reference, candidate, n=1)
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
    readability = readability_score(" ".join(reference), " ".join(candidate))
    sent_bleu = custom_sentence_bleu(" ".join(reference), " ".join(candidate))
    smog = smog_index(" ".join(reference), " ".join(candidate))
    ari = ari_score(" ".join(reference), " ".join(candidate))
    nist = nist_score(reference, candidate)
    lsa_sim = lsa_similarity(" ".join(reference), " ".join(candidate))
    sentiment_sim = sentiment_analysis(" ".join(reference), " ".join(candidate))
    lexical_density_score = lexical_density(" ".join(reference), " ".join(candidate))
    gunning_fog = gunning_fog_index(" ".join(reference), " ".join(candidate))
    coleman_liau = coleman_liau_index(" ".join(reference), " ".join(candidate))
    automated_readability = automated_readability_index(" ".join(reference), " ".join(candidate))

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
        "Readability Score": readability,
        "Sentence BLEU": sent_bleu,
        "SMOG Index": smog,
        "ARI Score": ari,
        "NIST Score": nist,
        "LSA Similarity": lsa_sim,
        "Sentiment Analysis": sentiment_sim,
        "Lexical Density": lexical_density_score,
        "Gunning Fog Index": gunning_fog,
        "Coleman Liau Index": coleman_liau,
        "Automated Readability Index": automated_readability
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
    scores["Aggregated Score"] = aggregated_score

    return scores


def save_individual_metrics(output_file, metrics):
    filename = os.path.basename(output_file).replace("_rewritten.json", "_metrics_comparison.json")
    path = os.path.join(rewritten_folder, filename)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=4)

def calculate_bleu(reference, candidate, n=4, smoothing=None):
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

def custom_sentence_bleu(references, hypothesis):
    references = references.split()
    hypothesis = hypothesis.split()
    return custom_bleu(references, hypothesis)

def custom_bleu(list_of_references, hypotheses):
    weights = [0.25, 0.25, 0.25, 0.25]
    p_n = [modified_precision(list_of_references, hypotheses, i) for i in range(1, 5)]
    s = (w * math.log(p_i) if p_i > 0 else 0 for w, p_i in zip(weights, p_n))
    return math.exp(sum(s))

def modified_precision(references, hypothesis, n):
    ref_ngrams = Counter(ngram for reference in references for ngram in zip(*[reference[i:] for i in range(n)]))
    hyp_ngrams = Counter(ngram for ngram in zip(*[hypothesis[i:] for i in range(n)]))
    numerator = sum((hyp_ngrams & ref_ngrams).values())
    denominator = max(1, sum(hyp_ngrams.values()))
    return numerator / denominator

def geometric_mean(precisions):
    return (reduce(lambda x, y: x * y, precisions)) ** (1.0 / len(precisions))

def brevity_penalty(reference, candidate):
    ref_length = len(reference)
    cand_length = len(candidate)
    if cand_length <= ref_length:
        return 1
    else:
        return math.exp(1 - (ref_length / cand_length))

def flatten_json(data, prefix=""):
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
    set1 = set(list1)
    set2 = set(list2)
    return len(set1.intersection(set2)) / len(set1.union(set2))

def rouge_l_similarity(reference, candidate):
    lcs = difflib.SequenceMatcher(None, reference, candidate).find_longest_match(
        0, len(reference), 0, len(candidate)
    )
    return (lcs.size * 2) / (len(reference) + len(candidate))

def tfidf_cosine_similarity(reference, candidate):
    vectorizer = TfidfVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    tfidf_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def calculate_meteor(reference, candidate):
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    ref_tokens = word_tokenize(ref_string)
    cand_tokens = word_tokenize(cand_string)
    return meteor_score([ref_tokens], cand_tokens)

def calculate_edit_distance(reference, candidate):
    return difflib.SequenceMatcher(None, reference, candidate).ratio()

def bow_cosine_similarity(reference, candidate):
    vectorizer = CountVectorizer()
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    bow_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]

from jiwer import wer
import numpy as np

def calculate_wer(reference, candidate):
    ref_string = " ".join(reference)
    cand_string = " ".join(candidate)
    return wer(ref_string, cand_string)

def calculate_cider(reference, candidate):
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
    return sum(el1 != el2 for el1, el2 in zip(reference, candidate)) + abs(
        len(reference) - len(candidate)
    )

def f1_score(reference, candidate):
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
    ref_set = set(reference)
    cand_set = set(candidate)
    return len(ref_set & cand_set) / min(len(ref_set), len(cand_set))

def dice_coefficient(reference, candidate):
    ref_set = set(reference)
    cand_set = set(candidate)
    return 2 * len(ref_set & cand_set) / (len(ref_set) + len(cand_set))

def longest_common_subsequence(reference, candidate):
    matcher = difflib.SequenceMatcher(None, reference, candidate)
    match = matcher.find_longest_match(0, len(reference), 0, len(candidate))
    return match.size

def levenshtein_distance(reference, candidate):
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
    return (textstat.flesch_reading_ease(reference) + textstat.flesch_reading_ease(candidate)) / 2

def smog_index(reference, candidate):
    return (textstat.smog_index(reference) + textstat.smog_index(candidate)) / 2

def ari_score(reference, candidate):
    return (textstat.automated_readability_index(reference) + textstat.automated_readability_index(candidate)) / 2

def nist_score(reference, candidate):
    return nltk.translate.nist_score.sentence_nist([reference], candidate)

def lsa_similarity(reference, candidate):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([reference, candidate])
    svd = TruncatedSVD(n_components=1)
    X_lsa = svd.fit_transform(X)
    return cosine_similarity(X_lsa[0:1], X_lsa[1:2])[0][0]

def sentiment_analysis(reference, candidate):
    ref_sentiment = TextBlob(reference).sentiment.polarity
    cand_sentiment = TextBlob(candidate).sentiment.polarity
    return 1 - abs(ref_sentiment - cand_sentiment)

def coherence_score(reference, candidate):
    reference = " ".join(reference)  # Join the list into a single string
    candidate = " ".join(candidate)  # Join the list into a single string
    ref_tokens = [word_tokenize(sent) for sent in nltk.sent_tokenize(reference)]
    cand_tokens = [word_tokenize(sent) for sent in nltk.sent_tokenize(candidate)]
    return (calculate_coherence(ref_tokens) + calculate_coherence(cand_tokens)) / 2

def calculate_coherence(tokens):
    # Dummy coherence calculation function, replace with actual implementation
    return sum(len(sent) for sent in tokens) / len(tokens)

def lexical_density(reference, candidate):
    def calculate_lexical_density(text):
        words = word_tokenize(text)
        lexical_words = [word for word in words if word.isalpha()]
        return len(lexical_words) / len(words) if words else 0

    ref_lexical_density = calculate_lexical_density(reference)
    cand_lexical_density = calculate_lexical_density(candidate)
    return (ref_lexical_density + cand_lexical_density) / 2


def gunning_fog_index(reference, candidate):
    return (textstat.gunning_fog(reference) + textstat.gunning_fog(candidate)) / 2

def coleman_liau_index(reference, candidate):
    return (textstat.coleman_liau_index(reference) + textstat.coleman_liau_index(candidate)) / 2

def automated_readability_index(reference, candidate):
    return (textstat.automated_readability_index(reference) + textstat.automated_readability_index(candidate)) / 2

def save_results_to_json(results, path):
    with open(path, "w") as f:
        json.dump(results, f, indent=4)

def save_results_to_html(results, path):
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

rewritten_files = [f for f in os.listdir(rewritten_folder) if f.endswith("_rewritten.json")]

all_results = []
for rewritten_file in rewritten_files:
    rewritten_path = os.path.join(rewritten_folder, rewritten_file)

    output_file = rewritten_file.replace("_rewritten.json", ".json")
    output_path = os.path.join(output_folder, output_file)

    if os.path.isfile(output_path):
        print("\nEvaluating:", output_file)
        result = compare_json_files(output_path, rewritten_path)
        if result:
            all_results.append(result)
            save_individual_metrics(rewritten_file, result)
    else:
        print(f"WARNING: No corresponding file found in 'output' for {rewritten_file}")

save_results_to_json(all_results, results_json_path)
save_results_to_html(all_results, results_html_path)

print(f"Results saved to {results_json_path} and {results_html_path}")
