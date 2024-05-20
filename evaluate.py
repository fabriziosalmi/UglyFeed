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
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

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

    # Metrics
    bleu1 = calculate_bleu(reference, candidate, n=1, smoothing=SmoothingFunction())
    # bleu2 = calculate_bleu(reference, candidate, n=2, smoothing=SmoothingFunction())
    # bleu4 = calculate_bleu(reference, candidate, n=4, smoothing=SmoothingFunction())
    jaccard = jaccard_similarity(reference, candidate)
    rouge_l = rouge_l_similarity(reference, candidate)
    tfidf_cosine = tfidf_cosine_similarity(reference, candidate)
    meteor = calculate_meteor(reference, candidate)
    edit_distance = calculate_edit_distance(reference, candidate)
    bow_cosine = bow_cosine_similarity(reference, candidate)

    # Store metrics in a dictionary
    scores = {
        "Output File": output_file,
        "BLEU-1": bleu1,
        # "BLEU-2": bleu2,
        # "BLEU-4": bleu4,
        "Jaccard Similarity": jaccard,
        "ROUGE-L": rouge_l,
        "TF-IDF Cosine Similarity": tfidf_cosine,
        "METEOR": meteor,
        "Edit Distance": edit_distance,
        "BoW Cosine Similarity": bow_cosine,
    }

    # Calculate Aggregated Score (weighted average, customizable)
    weights = {
        "BLEU-1": 0.12,
        # "BLEU-2": 0.12,
        # "BLEU-4": 0.12,
        "Jaccard Similarity": 0.12,
        "ROUGE-L": 0.12,
        "TF-IDF Cosine Similarity": 0.1,
        "METEOR": 0.1,
        "Edit Distance": 0.1,
        "BoW Cosine Similarity": 0.1,
    }
    aggregated_score = sum(weights[metric] * scores[metric] for metric in weights)
    scores['Aggregated Score'] = aggregated_score

    return scores

def calculate_bleu(reference, candidate, n=4, smoothing=None):
    """Calculates BLEU score for the given n-gram order."""
    precisions = []
    for i in range(1, n+1):
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

def geometric_mean(precisions):
    """Calculates the geometric mean of a list of precisions."""
    return (reduce(lambda x, y: x*y, precisions))**(1.0/len(precisions))

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
    lcs = difflib.SequenceMatcher(None, reference, candidate).find_longest_match(0, len(reference), 0, len(candidate))
    return (lcs.size * 2) / (len(reference) + len(candidate))

def tfidf_cosine_similarity(reference, candidate):
    """Calculates cosine similarity using TF-IDF vectors."""
    vectorizer = TfidfVectorizer()
    ref_string = ' '.join(reference)
    cand_string = ' '.join(candidate)
    tfidf_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def calculate_meteor(reference, candidate):
    """Calculates METEOR score."""
    ref_string = ' '.join(reference)
    cand_string = ' '.join(candidate)
    ref_tokens = word_tokenize(ref_string)
    cand_tokens = word_tokenize(cand_string)
    return meteor_score([ref_tokens], cand_tokens)

def calculate_edit_distance(reference, candidate):
    """Calculates Edit Distance."""
    return difflib.SequenceMatcher(None, reference, candidate).ratio()

def bow_cosine_similarity(reference, candidate):
    """Calculates cosine similarity using Bag of Words (BoW) vectors."""
    vectorizer = CountVectorizer()
    ref_string = ' '.join(reference)
    cand_string = ' '.join(candidate)
    bow_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(bow_matrix[0:1], bow_matrix[1:2])[0][0]

def save_results_to_json(results, path):
    """Saves the evaluation results to a JSON file."""
    with open(path, "w") as f:
        json.dump(results, f, indent=4)

def save_results_to_html(results, path):
    """Saves the evaluation results to an HTML file."""
    df = pd.DataFrame(results)
    html = df.to_html(index=False, classes='table table-striped table-hover table-bordered')

    with open(path, "w") as f:
        f.write('''
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
        ''')
        f.write(html)
        f.write('''
                </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        ''')

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
