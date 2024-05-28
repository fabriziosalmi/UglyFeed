# evaluate_against_reference.py

## Introduction
This script evaluates the quality of rewritten JSON files against reference JSON files using various metrics. It computes a range of similarity and readability metrics, aggregates the scores, and saves the results in JSON and HTML formats.

## Input/Output

### Input
- **Output Folder**: Directory containing the original JSON files (`output`).
- **Rewritten Folder**: Directory containing the rewritten JSON files (`rewritten`).

### Output
- **Evaluation Results**: JSON and HTML files containing the evaluation metrics for each rewritten file compared to its corresponding reference file.

## Functionality

### Features
1. **Evaluation Metrics**: Computes multiple metrics such as BLEU, Jaccard Similarity, ROUGE-L, TF-IDF Cosine Similarity, METEOR, Edit Distance, and more.
2. **Score Normalization**: Normalizes scores for aggregation.
3. **Aggregation**: Aggregates individual metric scores into a single score using predefined weights.
4. **Results Saving**: Saves the results in JSON and HTML formats for easy visualization and analysis.

## Code Structure

### Imports
```python
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
```
- **json**: For reading and writing JSON files.
- **os**: For file and directory operations.
- **difflib**: For sequence matching and edit distance calculation.
- **nltk**: For tokenization and METEOR score calculation.
- **collections.Counter**: For counting word occurrences.
- **sklearn.feature_extraction.text.TfidfVectorizer**: For transforming text data into TF-IDF features.
- **sklearn.metrics.pairwise.cosine_similarity**: For calculating cosine similarity.
- **pandas**: For creating dataframes.
- **math**: For mathematical operations.
- **functools.reduce**: For reducing operations.
- **sklearn.decomposition.TruncatedSVD**: For truncated singular value decomposition.
- **textblob**: For sentiment analysis.
- **textstat**: For readability scores.
- **spacy**: For advanced NLP processing.

### NLTK and spaCy Resources
```python
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

nlp = spacy.load("en_core_web_sm")
```
Downloads necessary NLTK resources and loads the spaCy model.

### Configuration
```python
output_folder = "output"
rewritten_folder = "rewritten"
results_json_path = "reports/evaluation_results.json"
results_html_path = "reports/evaluation_results.html"
```
Defines the directories and file paths for input and output.

### Normalizing Scores
```python
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
            normalized_scores[metric] = (1 - (scores[metric] / max_values.get(metric, 100))) * 100
        else:
            normalized_scores[metric] = scores[metric]

    return normalized_scores
```
Normalizes the scores for aggregation by defining maximum values and applying scaling.

### Comparing JSON Files
```python
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
        "LSA Similarity":

 0.02,
        "Sentiment Analysis": 0.02,
        "Lexical Density": 0.02,
        "Gunning Fog Index": 0.01,
        "Coleman Liau Index": 0.01,
        "Automated Readability Index": 0.01
    }

    aggregated_score = sum(weights[metric] * normalized_scores[metric] for metric in weights)
    scores["Aggregated Score"] = aggregated_score

    return scores
```
Compares a rewritten JSON file to its reference JSON file using various evaluation metrics, normalizes the scores, and computes an aggregated score.

### Saving Individual Metrics
```python
def save_individual_metrics(output_file, metrics):
    filename = os.path.basename(output_file).replace("_rewritten.json", "_metrics_comparison.json")
    path = os.path.join(rewritten_folder, filename)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=4)
```
Saves individual metrics for each rewritten file as a JSON file.

### Evaluation Metrics Functions
The script includes a variety of functions to calculate different evaluation metrics such as BLEU, Jaccard Similarity, ROUGE-L, TF-IDF Cosine Similarity, METEOR, Edit Distance, and more. Here are some examples:

#### BLEU Score
```python
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
```
Calculates the BLEU score for n-grams up to 4.

#### Jaccard Similarity
```python
def jaccard_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return len(set1.intersection(set2)) / len(set1.union(set2))
```
Calculates the Jaccard similarity between two lists.

#### ROUGE-L Similarity
```python
def rouge_l_similarity(reference, candidate):
    lcs = difflib.SequenceMatcher(None, reference, candidate).find_longest_match(
        0, len(reference), 0, len(candidate)
    )
    return (lcs.size * 2) / (len(reference) + len(candidate))
```
Calculates the ROUGE-L similarity between two texts.

### Saving Results
```python
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
```
Saves the evaluation results to JSON and HTML files.

### Main Execution
```python
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
```
Executes the comparison and evaluation of all rewritten files against their reference files, saving the results.

## Usage Example
1. Ensure the script is placed in the appropriate directory with access to the `output` and `rewritten` folders.
2. Run the script:
    ```bash
    python evaluate_against_reference.py
    ```
3. The evaluation results will be saved to `reports/evaluation_results.json` and `reports/evaluation_results.html`.
