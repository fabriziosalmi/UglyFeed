import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
import sys
import numpy as np

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('words')

# lexicon (initial tentative)
# you would replace these with actual data from a lexicon
concreteness_lexicon = {
    'en': {
        "dog": 5, "cat": 5, "happiness": 1, "justice": 1, "car": 5, "tree": 5, "freedom": 2,
        "love": 3, "music": 4, "peace": 2, "house": 5, "water": 4, "book": 5, "friendship": 3,
        "food": 5, "mountain": 5, "river": 4, "beauty": 2, "science": 3, "computer": 5,
        "teacher": 4, "doctor": 4, "idea": 2, "art": 3, "knowledge": 2, "happiness": 3,
        "sadness": 3, "truth": 2, "strength": 3, "energy": 3, "memory": 2, "history": 3,
        "city": 5, "village": 5, "forest": 5, "garden": 5, "flower": 5, "school": 5, "road": 5,
        "bridge": 5, "sky": 5, "star": 5, "sun": 5, "moon": 5, "animal": 4, "bird": 5, "fish": 5,
        "tree": 5, "plant": 5, "leaf": 5, "wind": 4, "storm": 4, "rain": 4, "snow": 4, "fire": 5,
        "earth": 5, "stone": 5, "sand": 5, "rock": 5, "beach": 5, "ocean": 5, "sea": 5, "lake": 5
    },
    'it': {
        "cane": 5, "gatto": 5, "felicità": 1, "giustizia": 1, "auto": 5, "albero": 5, "libertà": 2,
        "amore": 3, "musica": 4, "pace": 2, "casa": 5, "acqua": 4, "libro": 5, "amicizia": 3,
        "cibo": 5, "montagna": 5, "fiume": 4, "bellezza": 2, "scienza": 3, "computer": 5,
        "insegnante": 4, "dottore": 4, "idea": 2, "arte": 3, "conoscenza": 2, "felicità": 3,
        "tristezza": 3, "verità": 2, "forza": 3, "energia": 3, "memoria": 2, "storia": 3,
        "città": 5, "villaggio": 5, "foresta": 5, "giardino": 5, "fiore": 5, "scuola": 5, "strada": 5,
        "ponte": 5, "cielo": 5, "stella": 5, "sole": 5, "luna": 5, "animale": 4, "uccello": 5, "pesce": 5,
        "pianta": 5, "foglia": 5, "vento": 4, "tempesta": 4, "pioggia": 4, "neve": 4, "fuoco": 5,
        "terra": 5, "pietra": 5, "sabbia": 5, "roccia": 5, "spiaggia": 5, "oceano": 5, "mare": 5, "lago": 5
    }
}

imageability_lexicon = {
    'en': {
        "dog": 5, "cat": 5, "happiness": 3, "justice": 2, "car": 5, "tree": 5, "freedom": 3,
        "love": 4, "music": 4, "peace": 3, "house": 5, "water": 4, "book": 5, "friendship": 4,
        "food": 5, "mountain": 5, "river": 4, "beauty": 3, "science": 4, "computer": 5,
        "teacher": 4, "doctor": 4, "idea": 3, "art": 4, "knowledge": 3, "happiness": 4,
        "sadness": 4, "truth": 3, "strength": 4, "energy": 4, "memory": 3, "history": 4,
        "city": 5, "village": 5, "forest": 5, "garden": 5, "flower": 5, "school": 5, "road": 5,
        "bridge": 5, "sky": 5, "star": 5, "sun": 5, "moon": 5, "animal": 4, "bird": 5, "fish": 5,
        "tree": 5, "plant": 5, "leaf": 5, "wind": 4, "storm": 4, "rain": 4, "snow": 4, "fire": 5,
        "earth": 5, "stone": 5, "sand": 5, "rock": 5, "beach": 5, "ocean": 5, "sea": 5, "lake": 5
    },
    'it': {
        "cane": 5, "gatto": 5, "felicità": 3, "giustizia": 2, "auto": 5, "albero": 5, "libertà": 3,
        "amore": 4, "musica": 4, "pace": 3, "casa": 5, "acqua": 4, "libro": 5, "amicizia": 4,
        "cibo": 5, "montagna": 5, "fiume": 4, "bellezza": 3, "scienza": 4, "computer": 5,
        "insegnante": 4, "dottore": 4, "idea": 3, "arte": 4, "conoscenza": 3, "felicità": 4,
        "tristezza": 4, "verità": 3, "forza": 4, "energia": 4, "memoria": 3, "storia": 4,
        "città": 5, "villaggio": 5, "foresta": 5, "giardino": 5, "fiore": 5, "scuola": 5, "strada": 5,
        "ponte": 5, "cielo": 5, "stella": 5, "sole": 5, "luna": 5, "animale": 4, "uccello": 5, "pesce": 5,
        "pianta": 5, "foglia": 5, "vento": 4, "tempesta": 4, "pioggia": 4, "neve": 4, "fuoco": 5,
        "terra": 5, "pietra": 5, "sabbia": 5, "roccia": 5, "spiaggia": 5, "oceano": 5, "mare": 5, "lago": 5
    }
}

aoa_lexicon = {
    'en': {
        "dog": 3, "cat": 3, "happiness": 5, "justice": 6, "car": 3, "tree": 4, "freedom": 6,
        "love": 5, "music": 4, "peace": 6, "house": 3, "water": 3, "book": 4, "friendship": 6,
        "food": 3, "mountain": 5, "river": 4, "beauty": 5, "science": 6, "computer": 5,
        "teacher": 6, "doctor": 6, "idea": 6, "art": 5, "knowledge": 6, "happiness": 5,
        "sadness": 5, "truth": 6, "strength": 6, "energy": 6, "memory": 6, "history": 6,
        "city": 4, "village": 5, "forest": 6, "garden": 4, "flower": 5, "school": 3, "road": 3,
        "bridge": 4, "sky": 4, "star": 4, "sun": 3, "moon": 3, "animal": 3, "bird": 3, "fish": 3,
        "tree": 4, "plant": 4, "leaf": 4, "wind": 6, "storm": 6, "rain": 6, "snow": 5, "fire": 3,
        "earth": 4, "stone": 5, "sand": 5, "rock": 5, "beach": 4, "ocean": 6, "sea": 4, "lake": 4
        },
        'it': {
        "cane": 3, "gatto": 3, "felicità": 5, "giustizia": 6, "auto": 3, "albero": 4, "libertà": 6,
        "amore": 5, "musica": 4, "pace": 6, "casa": 3, "acqua": 3, "libro": 4, "amicizia": 6,
        "cibo": 3, "montagna": 5, "fiume": 4, "bellezza": 5, "scienza": 6, "computer": 5,
        "insegnante": 6, "dottore": 6, "idea": 6, "arte": 5, "conoscenza": 6, "felicità": 5,
        "tristezza": 5, "verità": 6, "forza": 6, "energia": 6, "memoria": 6, "storia": 6,
        "città": 4, "villaggio": 5, "foresta": 6, "giardino": 4, "fiore": 5, "scuola": 3, "strada": 3,
        "ponte": 4, "cielo": 4, "stella": 4, "sole": 3, "luna": 3, "animale": 3, "uccello": 3, "pesce": 3,
        "pianta": 4, "foglia": 4, "vento": 6, "tempesta": 6, "pioggia": 6, "neve": 5, "fuoco": 3,
        "terra": 4, "pietra": 5, "sabbia": 5, "roccia": 5, "spiaggia": 4, "oceano": 6, "mare": 4, "lago": 4
    }
}

# Define a list of familiar words for simplicity

familiar_words_en = set(nltk.corpus.words.words())
familiar_words_it = set([
        "cane", "gatto", "felicità", "giustizia", "mela", "auto", "casa", "libro", "albero", "acqua",
        "amore", "scuola", "bambino", "pane", "strada", "fiore", "gente", "mare", "montagna", "fiume",
        "famiglia", "amico", "lavoro", "giorno", "notte", "anno", "tempo", "musica", "arte", "cibo",
        "macchina", "giardino", "città", "villaggio", "bosco", "sole", "luna", "stella", "nuvola", "pioggia",
        "neve", "vento", "tempesta", "fuoco", "terra", "roccia", "sabbia", "oceano", "spiaggia", "lago"
])  # Example familiar words in Italian


def detect_language(text):
    # Simple heuristic to detect the language based on common stopwords
    words = word_tokenize(text.lower())
    if any(word in words for word in nltk.corpus.stopwords.words('english')):
        return 'en'
    elif any(word in words for word in nltk.corpus.stopwords.words('italian')):
        return 'it'
    else:
        return 'it'  # Default to Italian

def calculate_cohesion_score(text):
    # Placeholder for a more sophisticated cohesion calculation
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    cohesion_score = sum(1 for sentence in sentences if any(word in words for word in word_tokenize(sentence.lower())))
    return cohesion_score / len(sentences) if sentences else 0

def calculate_concreteness_score(text, lang):
    words = word_tokenize(text)
    concreteness_scores = [concreteness_lexicon[lang].get(word.lower(), 0) for word in words]
    return np.mean(concreteness_scores) if concreteness_scores else 0

def calculate_imageability_score(text, lang):
    words = word_tokenize(text)
    imageability_scores = [imageability_lexicon[lang].get(word.lower(), 0) for word in words]
    return np.mean(imageability_scores) if imageability_scores else 0

def calculate_aoa_score(text, lang):
    words = word_tokenize(text)
    aoa_scores = [aoa_lexicon[lang].get(word.lower(), 0) for word in words]
    return np.mean(aoa_scores) if aoa_scores else 0

def calculate_text_familiarity_index(text, lang):
    words = word_tokenize(text)
    familiar_words = familiar_words_en if lang == 'en' else familiar_words_it
    familiar_word_count = sum(1 for word in words if word.lower() in familiar_words)
    return familiar_word_count / len(words) if words else 0

def evaluate_cohesion_concreteness_metrics(text):
    lang = detect_language(text)
    metrics = {
        "Cohesion Score": calculate_cohesion_score(text),
        "Concreteness Score": calculate_concreteness_score(text, lang),
        "Imageability Score": calculate_imageability_score(text, lang),
        "Age of Acquisition Score": calculate_aoa_score(text, lang),
        "Text Familiarity Index": calculate_text_familiarity_index(text, lang),
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Cohesion Score": 0.2,
        "Concreteness Score": 0.2,
        "Imageability Score": 0.2,
        "Age of Acquisition Score": 0.2,
        "Text Familiarity Index": 0.2,
    }

    aggregated_score = sum(metrics[metric] * weights[metric] for metric in metrics) * 100

    return metrics, aggregated_score

def main(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        text = data.get("content", "")

    if not text:
        print("No content found in the provided JSON file.")
        return

    metrics, aggregated_score = evaluate_cohesion_concreteness_metrics(text)

    print("Text Cohesion and Concreteness Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"Aggregated Cohesion and Concreteness Score: {aggregated_score:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_cohesion_concreteness.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
