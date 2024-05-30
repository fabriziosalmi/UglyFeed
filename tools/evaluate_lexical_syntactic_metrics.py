import sys
import json
from collections import Counter
from langdetect import detect
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# Load the spaCy models for both English and Italian
nlp_en = spacy.load("en_core_web_sm")
nlp_it = spacy.load("it_core_news_sm")

# Define function to detect language
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian

# Define function to get appropriate spaCy model based on language
def get_spacy_model(lang):
    if lang == 'en':
        return nlp_en
    else:
        return nlp_it

# Function to calculate Named Entity Recognition (NER) Coverage
def calculate_ner_coverage(text, nlp):
    doc = nlp(text)
    ner_tokens = set([ent.text for ent in doc.ents])
    words = set(word_tokenize(text.lower()))
    return len(ner_tokens.intersection(words)) / len(words) if words else 0

# Function to calculate Dependency Tree Depth
def calculate_dependency_tree_depth(text, nlp):
    doc = nlp(text)
    max_depth = 0

    def get_depth(token):
        if not list(token.children):
            return 1
        else:
            return 1 + max(get_depth(child) for child in token.children)

    for sent in doc.sents:
        for token in sent:
            max_depth = max(max_depth, get_depth(token))
    
    return max_depth

# Function to calculate Syntactic Variability
def calculate_syntactic_variability(text, nlp):
    sentences = sent_tokenize(text)
    pos_patterns = [tuple(token.pos_ for token in nlp(sentence)) for sentence in sentences]
    unique_patterns = set(pos_patterns)
    return len(unique_patterns) / len(sentences) if sentences else 0

# Function to calculate Lexical Density
def calculate_lexical_density(text, lang):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english')) if lang == 'en' else set(stopwords.words('italian'))
    content_words = [word for word in words if word not in stop_words and word.isalpha()]
    return len(content_words) / len(words) if words else 0

# Function to calculate Passive Voice Percentage
def calculate_passive_voice_percentage(text, nlp):
    doc = nlp(text)
    passive_sentences = 0

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "nsubjpass" or token.dep_ == "auxpass":
                passive_sentences += 1
                break
    
    return passive_sentences / len(list(doc.sents)) if list(doc.sents) else 0

# Function to calculate Longest Increasing Subsequence
def calculate_longest_increasing_subsequence(text):
    words = word_tokenize(text.lower())
    if not words:
        return 0

    lengths = [1] * len(words)
    for i in range(1, len(words)):
        for j in range(i):
            if words[i] > words[j]:
                lengths[i] = max(lengths[i], lengths[j] + 1)
    
    return max(lengths)

def evaluate_lexical_syntactic_metrics(text, lang):
    nlp = get_spacy_model(lang)
    
    metrics = {
        "Named Entity Recognition (NER) Coverage": calculate_ner_coverage(text, nlp),
        "Dependency Tree Depth": calculate_dependency_tree_depth(text, nlp),
        "Syntactic Variability": calculate_syntactic_variability(text, nlp),
        "Lexical Density": calculate_lexical_density(text, lang),
        "Passive Voice Percentage": calculate_passive_voice_percentage(text, nlp),
        "Longest Increasing Subsequence": calculate_longest_increasing_subsequence(text)
    }

    # Normalize the metrics to a range of 0 to 1
    normalized_metrics = {
        "Named Entity Recognition (NER) Coverage": metrics["Named Entity Recognition (NER) Coverage"],  # already 0-1
        "Dependency Tree Depth": metrics["Dependency Tree Depth"] / 100,  # Example normalization, adjust as needed
        "Syntactic Variability": metrics["Syntactic Variability"],  # already 0-1
        "Lexical Density": metrics["Lexical Density"],  # already 0-1
        "Passive Voice Percentage": metrics["Passive Voice Percentage"],  # already 0-1
        "Longest Increasing Subsequence": metrics["Longest Increasing Subsequence"] / 100  # Example normalization, adjust as needed
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Named Entity Recognition (NER) Coverage": 0.1667,
        "Dependency Tree Depth": 0.1667,
        "Syntactic Variability": 0.1667,
        "Lexical Density": 0.1667,
        "Passive Voice Percentage": 0.1667,
        "Longest Increasing Subsequence": 0.1667
    }

    aggregated_score = sum(normalized_metrics[metric] * weights[metric] for metric in normalized_metrics) * 100
    
    return metrics, normalized_metrics, aggregated_score

def main(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        text = data.get("content", "")

    if not text:
        print("No content found in the provided JSON file.")
        return

    lang = detect_language(text)
    metrics, normalized_metrics, aggregated_score = evaluate_lexical_syntactic_metrics(text, lang)

    output = {
        "Lexical and Syntactic Metrics": metrics,
        "Aggregated Lexical and Syntactic Score": aggregated_score
    }

    print("Text Lexical and Syntactic Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Lexical and Syntactic Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_lexical_syntactic.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_lexical_syntactic_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
