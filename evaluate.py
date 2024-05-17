import json
import os
import difflib
from nltk.translate.bleu_score import SmoothingFunction
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math
from functools import reduce

output_folder = "output"
rewritten_folder = "rewritten"

def compare_json_files(output_file, rewritten_file):
    """Compares JSON files, calculates multiple metrics, and aggregates them."""

    with open(output_file, "r") as f1, open(rewritten_file, "r") as f2:
        try:
            data1 = json.load(f1)
            data2 = json.load(f2)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON format in {output_file} or {rewritten_file}")
            return

    # Flatten JSON to lists of strings
    reference = flatten_json(data1)
    candidate = flatten_json(data2)

    # Metrics
    bleu1 = calculate_bleu(reference, candidate, n=1, smoothing=SmoothingFunction())
    bleu2 = calculate_bleu(reference, candidate, n=2, smoothing=SmoothingFunction())
    jaccard = jaccard_similarity(reference, candidate)
    rouge_l = rouge_l_similarity(reference, candidate)
    tfidf_cosine = tfidf_cosine_similarity(reference, candidate)

    # Store metrics in a dictionary
    scores = {
        "Output File": output_file,
        "BLEU-1": bleu1,
        "BLEU-2": bleu2,
        "Jaccard Similarity": jaccard,  # Corrected key name
        "ROUGE-L": rouge_l,
        "TF-IDF Cosine Similarity": tfidf_cosine,
    }

    # Calculate Aggregated Score (weighted average, customizable)
    weights = {"BLEU-1": 0.2, "BLEU-2": 0.2, "Jaccard Similarity": 0.3, "ROUGE-L": 0.2, "TF-IDF Cosine Similarity": 0.1}  # Corrected key name
    aggregated_score = sum(weights[metric] * scores[metric] for metric in weights)
    scores['Aggregated Score'] = aggregated_score



    df = pd.DataFrame([scores])
    print(df.to_markdown(index=False, numalign="left", stralign="left"))





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
    ref_string = ' '.join(reference) # Joining the list of words into string
    cand_string = ' '.join(candidate)
    tfidf_matrix = vectorizer.fit_transform([ref_string, cand_string])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


# Get all JSON files in the rewritten folder (notice the change)
rewritten_files = [f for f in os.listdir(rewritten_folder) if f.endswith(".json")]

# Compare and evaluate each file
for rewritten_file in rewritten_files:
    rewritten_path = os.path.join(rewritten_folder, rewritten_file)

    # Remove the "_rewritten" part from the rewritten filename to get the original
    output_file = rewritten_file.replace("_rewritten.json", ".json")
    output_path = os.path.join(output_folder, output_file)

    if os.path.isfile(output_path):
        print("\nEvaluating:", output_file)  # Print the original filename
        compare_json_files(output_path, rewritten_path)
    else:
        print(f"WARNING: No corresponding file found in 'output' for {rewritten_file}")
