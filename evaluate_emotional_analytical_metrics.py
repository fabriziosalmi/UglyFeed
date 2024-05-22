import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from collections import Counter
from langdetect import detect
import spacy
from textblob import TextBlob

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")

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

# Define extended keywords for emotional and analytical thinking in both languages
emotional_keywords_en = [
    "happy", "sad", "angry", "joy", "fear", "love", "hate", "excited", "depressed", "anxious", 
    "grateful", "hopeful", "nervous", "scared", "relieved", "proud", "ashamed", "frustrated",
    "content", "delighted", "miserable", "furious", "terrified", "ecstatic", "heartbroken", "melancholy",
    "peaceful", "jealous", "enthusiastic", "guilty", "affectionate", "lonely", "bored", "resentful",
    "shocked", "confident", "fearful", "humiliated", "optimistic", "pessimistic", "wistful", "inspired",
    "calm", "stressed", "excited", "eager", "apathetic", "disgusted", "irritated", "curious",
    "dismayed", "elated", "enraged", "worried", "sympathetic", "touched", "moved", "thrilled",
    "startled", "sorrowful", "disheartened", "outraged", "gleeful", "horrified", "bewildered", "amused",
    "regretful", "insecure", "secure", "overwhelmed", "serene", "cheerful", "hopeful", "passionate"
]

analytical_keywords_en = [
    "analyze", "logic", "reason", "evidence", "data", "rationale", "study", "investigate", 
    "examine", "evaluate", "systematic", "objective", "methodical", "quantitative", "qualitative",
    "deduce", "hypothesis", "theory", "experiment", "survey", "statistics", "model", "framework",
    "paradigm", "approach", "analysis", "conclusion", "inference", "interpret", "variable", "algorithm",
    "formula", "procedure", "calculate", "measure", "assess", "criterion", "benchmark", "parameter",
    "logically", "deductive", "empirical", "correlate", "simulate", "hypothetical", "propositional",
    "analytical", "statistical", "cognitive", "discriminant", "experimental", "operational", "methodological",
    "heuristic", "predictive", "formulate", "synthesize", "derive", "systematize", "testable"
]

emotional_keywords_it = [
    "felice", "triste", "arrabbiato", "gioia", "paura", "amore", "odio", "eccitato", "depresso", "ansioso", 
    "grato", "speranzoso", "nervoso", "spaventato", "sollevato", "orgoglioso", "vergognoso", "frustrato",
    "contento", "deliziato", "miserabile", "furioso", "terrorizzato", "estatico", "struggente", "melanconico",
    "sereno", "geloso", "entusiasta", "colpevole", "affettuoso", "solitario", "annoiato", "risentito",
    "scioccato", "sicuro", "pauroso", "umiliato", "ottimista", "pessimista", "nostalgico", "ispirato",
    "calmo", "stressato", "eccitato", "desideroso", "apatetico", "disgustato", "irritato", "curioso",
    "costernato", "euforico", "infuriato", "preoccupato", "simpatico", "toccato", "commosso", "entusiasmato",
    "sorpreso", "addolorato", "scoraggiato", "indignato", "gioioso", "orripilato", "perplesso", "divertito",
    "rammaricato", "insicuro", "sicuro", "sopraffatto", "sereno", "allegro", "speranzoso", "appassionato"
]

analytical_keywords_it = [
    "analizzare", "logica", "ragione", "prova", "dati", "ragionamento", "studio", "indagare", 
    "esaminare", "valutare", "sistematico", "obiettivo", "metodico", "quantitativo", "qualitativo",
    "dedurre", "ipotesi", "teoria", "esperimento", "sondaggio", "statistiche", "modello", "quadro",
    "paradigma", "approccio", "analisi", "conclusione", "inferenza", "interpretare", "variabile", "algoritmo",
    "formula", "procedura", "calcolare", "misurare", "valutare", "criterio", "benchmark", "parametro",
    "logico", "deduttivo", "empirico", "correlare", "simulare", "ipotetico", "proposizionale",
    "analitico", "statistico", "cognitivo", "discriminante", "sperimentale", "operazionale", "metodologico",
    "euristico", "predittivo", "formulare", "sintetizzare", "derivare", "sistematizzare", "verificabile"
]

# Function to calculate Emotional Tone Score
def calculate_emotional_tone_score(text, lang):
    words = word_tokenize(text.lower())
    emotional_keywords = emotional_keywords_en if lang == 'en' else emotional_keywords_it
    emotional_count = sum(1 for word in words if word in emotional_keywords)
    return emotional_count / len(words) if len(words) > 0 else 0

# Function to calculate Analytical Thinking Score
def calculate_analytical_thinking_score(text, lang):
    words = word_tokenize(text.lower())
    analytical_keywords = analytical_keywords_en if lang == 'en' else analytical_keywords_it
    analytical_count = sum(1 for word in words if word in analytical_keywords)
    return analytical_count / len(words) if len(words) > 0 else 0

def evaluate_emotional_analytical_metrics(text, lang):
    metrics = {
        "Emotional Tone Score": calculate_emotional_tone_score(text, lang),
        "Analytical Thinking Score": calculate_analytical_thinking_score(text, lang)
    }

    # Normalize the metrics to a range of 0 to 1 based on reasonable upper limits
    max_values = {
        "Emotional Tone Score": 0.1,  # Example normalization, adjust as needed
        "Analytical Thinking Score": 0.1  # Example normalization, adjust as needed
    }

    normalized_metrics = {key: min(metrics[key] / max_values[key], 1) for key in metrics}

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Emotional Tone Score": 0.5,
        "Analytical Thinking Score": 0.5
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
    metrics, normalized_metrics, aggregated_score = evaluate_emotional_analytical_metrics(text, lang)

    output = {
        "Emotional and Analytical Metrics": metrics,
        "Aggregated Emotional and Analytical Score": aggregated_score
    }

    print("Text Emotional and Analytical Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print("\nNormalized Metrics:")
    for metric, score in normalized_metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"\nAggregated Emotional and Analytical Score: {aggregated_score:.4f}")

    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_emotional_analytical.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_emotional_analytical_metrics.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
