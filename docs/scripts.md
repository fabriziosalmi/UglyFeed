# Scripts documentation

- [evaluate_cohesion_concreteness.py](https://github.com/fabriziosalmi/UglyFeed/new/main/docs#evaluate_cohesion_concretenesspy)

Welcome to the Scripts Documentation section. This comprehensive guide provides detailed information and instructions for each script in our project. 
Each script's documentation includes the following sections:

- **Overview**
A brief introduction to the script, explaining its purpose and the specific problem it aims to solve.

- **Installation**
Detailed instructions on how to install any necessary dependencies and set up the script in your environment.

- **Usage**
Step-by-step instructions on how to run the script, including command-line arguments, configuration options, and practical examples.

- **Functionality**
A deep dive into the core functionality of the script, describing key functions and modules, and how they work together.

- **Input/Output**
Information about the expected input formats and the structure of the output data, ensuring users understand what the script requires and what it produces.

- **Code Structure**
An overview of the script's architecture, highlighting major components and their interactions, to give users a clear understanding of how the script is built.

---

## evaluate_cohesion_concreteness.py

This Python script evaluates the cohesion and information density metrics of a text extracted from a JSON file. It uses several libraries, including `json`, `nltk`, `langdetect`, and `spacy`. Here is an explanation of each section of the code:

### Imports and Setup
```python
import json
import nltk
import sys
from langdetect import detect
import spacy
from collections import Counter
```
- **json**: To handle JSON files.
- **nltk**: For natural language processing tasks such as tokenization.
- **sys**: To handle command-line arguments.
- **langdetect**: To detect the language of the input text.
- **spacy**: For advanced NLP tasks using pre-trained models.
- **Counter**: To count token occurrences.

### Download NLTK Resources
```python
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
```
- Downloads the necessary NLTK resources for tokenization and stop words.

### Load spaCy Models
```python
nlp_en = spacy.load("en_core_web_sm")
nlp_it = spacy.load("it_core_news_sm")
```
- Loads spaCy models for English and Italian.

### Define Language Detection and Model Selection Functions
```python
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian
```
- Detects the language of the text using `langdetect`. Defaults to Italian if detection fails.

```python
def get_spacy_model(lang):
    if lang == 'en':
        return nlp_en
    else:
        return nlp_it
```
- Returns the appropriate spaCy model based on the detected language.

### Placeholder Function for Coh-Metrix Scores
```python
def calculate_coh_metrix_scores(text):
    return 0.5
```
- A placeholder function for Coh-Metrix Scores. It returns a dummy score of 0.5.

### Define Metric Calculation Functions
```python
def calculate_cohesion_score(text):
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return 0
    overlaps = 0
    for i in range(len(sentences) - 1):
        tokens1 = set(nltk.word_tokenize(sentences[i].lower()))
        tokens2 = set(nltk.word_tokenize(sentences[i+1].lower()))
        overlaps += len(tokens1.intersection(tokens2))
    return overlaps / (len(sentences) - 1)
```
- Calculates the cohesion score by analyzing overlapping tokens between consecutive sentences.

```python
def calculate_cohesive_harmony_index(text, nlp):
    doc = nlp(text)
    harmony_score = 0
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('nsubj', 'dobj', 'iobj', 'pobj'):
                harmony_score += 1
    return harmony_score / len(list(doc.sents)) if len(list(doc.sents)) > 0 else 0
```
- Calculates the cohesive harmony index by counting the occurrences of specific syntactic dependencies.

```python
def calculate_referential_density(text, nlp):
    doc = nlp(text)
    referential_count = sum(1 for token in doc if token.pos_ in ('NOUN', 'PRON'))
    return referential_count / len(doc) if len(doc) > 0 else 0
```
- Calculates referential density based on the occurrence of nouns and pronouns.

```python
def calculate_information_density(text):
    words = nltk.word_tokenize(text)
    unique_words = set(words)
    return len(unique_words) / len(words) if len(words) > 0 else 0
```
- Calculates information density as the ratio of unique words to total words.

### Evaluation Function
```python
def evaluate_cohesion_information_density_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Coh-Metrix Scores": calculate_coh_metrix_scores(text),
        "Cohesion Score": calculate_cohesion_score(text),
        "Cohesive Harmony Index": calculate_cohesive_harmony_index(text, nlp),
        "Referential Density": calculate_referential_density(text, nlp),
        "Information Density": calculate_information_density(text)
    }

    max_values = {
        "Coh-Metrix Scores": 1,
        "Cohesion Score": 1,
        "Cohesive Harmony Index": 1,
        "Referential Density": 1,
        "Information Density": 1
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    weights = {
        "Coh-Metrix Scores": 0.2,
        "Cohesion Score": 0.2,
        "Cohesive Harmony Index": 0.2,
        "Referential Density": 0.2,
        "Information Density": 0.2
    }

    aggregated_score = sum(normalized_metrics[metric] * weights[metric] for metric in normalized_metrics) * 100
    
    return metrics, normalized_metrics, aggregated_score
```
- Evaluates the cohesion and information density metrics, normalizes them, and calculates an aggregated score.

### Main Function and Execution
```python
def main(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            text = data.get("content", "")

        if not text:
            print("No content found in the provided JSON file.")
            return

        lang = detect_language(text)
        metrics, normalized_metrics, aggregated_score = evaluate_cohesion_information_density_metrics(text, lang)

        output = {
            "Cohesion Information Density Metrics": metrics,
            "Aggregated Cohesion Information Density Score": aggregated_score
        }

        print("Text Cohesion and Information Density Metrics:")
        for metric, score in metrics.items():
            print(f"{metric}: {score:.4f}")
        print("\nNormalized Metrics:")
        for metric, score in normalized_metrics.items():
            print(f"{metric}: {score:.4f}")
        print(f"\nAggregated Cohesion and Information Density Score: {aggregated_score:.4f}")

        output_file_path = file_path.replace(".json", "_metrics_cohesion_information_density.json")
        with open(output_file_path, 'w') as out_file:
            json.dump(output, out_file, indent=4)
        print(f"Metrics exported to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The provided file is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_cohesion_information_density_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
```
- Reads the input JSON file, extracts the text, detects its language, calculates various metrics, normalizes them, and prints/export the results.
