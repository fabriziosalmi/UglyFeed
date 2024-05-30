"""
Module for evaluating noun and verb metrics in text using spaCy and NLTK.
"""

import json
import sys
from langdetect import detect
import nltk
import spacy
from spacy.cli import download

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

# Ensure spaCy models are downloaded
try:
    nlp_en = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp_en = spacy.load("en_core_web_sm")

try:
    nlp_it = spacy.load("it_core_news_sm")
except OSError:
    download("it_core_news_sm")
    nlp_it = spacy.load("it_core_news_sm")

def detect_language(text):
    """Detect the language of the provided text."""
    try:
        return detect(text)
    except Exception:
        return 'it'  # Default to Italian

def get_spacy_model(lang):
    """Get the appropriate spaCy model based on language."""
    return nlp_en if lang == 'en' else nlp_it

# Define extended lists of concrete and abstract nouns (examples)
concrete_nouns_en = [
    "dog", "cat", "car", "house", "tree", "book", "apple", "phone", "computer", "table",
    "chair", "window", "door", "road", "river", "mountain", "pen", "notebook", "bag", "shoe",
    "bicycle", "building", "garden", "bed", "cup", "plate", "spoon", "fork", "knife", "television",
    "lamp", "couch", "shirt", "dress", "hat", "watch", "wallet", "camera", "printer", "keyboard",
    "train", "airplane", "ship", "boat", "bridge", "tower", "statue", "painting", "sculpture", "desk",
    "backpack", "helmet", "glasses", "bottle", "lamp", "mirror", "sofa", "carpet", "pillow", "blanket",
    "curtain", "cabinet", "bench", "fireplace", "fountain", "garage", "ladder", "notepad", "pencil", "eraser"
]

abstract_nouns_en = [
    "freedom", "happiness", "justice", "thought", "idea", "love", "peace", "knowledge", "wisdom",
    "anger", "fear", "joy", "sorrow", "beauty", "truth", "courage", "faith", "honor", "trust",
    "patience", "pride", "humility", "envy", "greed", "charity", "gratitude", "sympathy",
    "empathy", "friendship", "hope", "compassion", "doubt", "belief", "determination",
    "imagination", "inspiration", "respect", "responsibility", "ambition", "curiosity", "creativity",
    "confidence", "despair", "enthusiasm", "freedom", "integrity", "intelligence", "loyalty", "mercy",
    "optimism", "persistence", "reliability", "sensitivity", "tolerance", "wisdom", "zeal"
]

concrete_nouns_it = [
    "cane", "gatto", "auto", "casa", "albero", "libro", "mela", "telefono", "computer", "tavolo",
    "sedia", "finestra", "porta", "strada", "fiume", "montagna", "penna", "quaderno", "borsa", "scarpa",
    "bicicletta", "edificio", "giardino", "letto", "tazza", "piatto", "cucchiaio", "forchetta", "coltello", "televisione",
    "lampada", "divano", "camicia", "vestito", "cappello", "orologio", "portafoglio", "fotocamera", "stampante", "tastiera",
    "treno", "aereo", "nave", "barca", "ponte", "torre", "statua", "dipinto", "scultura", "scrivania",
    "zaino", "casco", "occhiali", "bottiglia", "lampada", "specchio", "divano", "tappeto", "cuscino", "coperta",
    "tenda", "armadio", "panca", "caminetto", "fontana", "garage", "scala", "taccuino", "matita", "gomma"
]

abstract_nouns_it = [
    "libertà", "felicità", "giustizia", "pensiero", "idea", "amore", "pace", "conoscenza", "saggezza",
    "rabbia", "paura", "gioia", "tristezza", "bellezza", "verità", "coraggio", "fede", "onore", "fiducia",
    "pazienza", "orgoglio", "umiltà", "invidia", "avidità", "carità", "gratitudine", "simpatia",
    "empatia", "amicizia", "speranza", "compassione", "dubbio", "credenza", "determinazione",
    "immaginazione", "ispirazione", "rispetto", "responsabilità", "ambizione", "curiosità", "creatività",
    "fiducia", "disperazione", "entusiasmo", "libertà", "integrità", "intelligenza", "lealtà", "misericordia",
    "ottimismo", "perseveranza", "affidabilità", "sensibilità", "tolleranza", "saggezza", "zelo"
]

def calculate_concrete_noun_ratio(text, nlp, lang):
    """
    Calculate the concrete noun ratio in the text.
    """
    doc = nlp(text)
    concrete_nouns = concrete_nouns_en if lang == 'en' else concrete_nouns_it
    concrete_noun_tokens = [
        token for token in doc
        if token.lemma_ in concrete_nouns and token.pos_ == "NOUN"
    ]
    nouns = [token for token in doc if token.pos_ == "NOUN"]
    return len(concrete_noun_tokens) / len(nouns) if nouns else 0

def calculate_abstract_noun_ratio(text, nlp, lang):
    """
    Calculate the abstract noun ratio in the text.
    """
    doc = nlp(text)
    abstract_nouns = abstract_nouns_en if lang == 'en' else abstract_nouns_it
    abstract_noun_tokens = [
        token for token in doc
        if token.lemma_ in abstract_nouns and token.pos_ == "NOUN"
    ]
    nouns = [token for token in doc if token.pos_ == "NOUN"]
    return len(abstract_noun_tokens) / len(nouns) if nouns else 0

def evaluate_noun_verb_metrics(text, lang):
    """
    Evaluate noun and verb metrics in the provided text.
    """
    nlp = get_spacy_model(lang)
    metrics = {
        "Concrete Noun Ratio": calculate_concrete_noun_ratio(text, nlp, lang),
        "Abstract Noun Ratio": calculate_abstract_noun_ratio(text, nlp, lang)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper limits
    max_values = {
        "Concrete Noun Ratio": 0.5,  # Example normalization, adjust as needed
        "Abstract Noun Ratio": 0.5   # Example normalization, adjust as needed
    }

    normalized_metrics = {
        key: min(metrics[key] / max_values[key], 1) for key in metrics
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Concrete Noun Ratio": 0.5,
        "Abstract Noun Ratio": 0.5
    }

    aggregated_score = sum(
        normalized_metrics[metric] * weights[metric]
        for metric in normalized_metrics
    ) * 100

    return metrics, normalized_metrics, aggregated_score

def main(file_path):
    """
    Main function to process the input file and evaluate metrics.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = data.get("content", "")

    if not text:
        print("No content found in the provided JSON file.")
        return

    lang = detect_language(text)
    metrics, normalized_metrics, aggregated_score = evaluate_noun_verb_metrics(text, lang)

    output = {
        "Noun and Verb Metrics": metrics,
        "Aggregated Noun and Verb Score": aggregated_score
    }

    print("Text Noun and Verb Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Noun and Verb Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_noun_verb.json")
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_noun_verb_metrics.py <file_path>")
        sys.exit(1)

    main(sys.argv[1])
