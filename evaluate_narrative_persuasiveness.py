import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys

# Ensure nltk resources are downloaded
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("stopwords", quiet=True)

# Define words indicative of narrative and persuasive content in both languages
# Define words indicative of narrative and persuasive content in both languages
narrative_keywords = {
    'en': ["story", "narrative", "tale", "plot", "character", "setting", "theme", "conflict", "resolution", "event", "incident", "account", "chronicle", "saga", "anecdote", "fable", "legend", "myth", "parable", "recital", "yarn", "adventure", "episode", "journey", "quest", "scene", "sequence", "drama", "storyline", "memoir", "novel", "fable", "mythology", "biography", "autobiography", "fairy tale", "narration", "short story", "novella", "folktale"],
    'it': ["storia", "racconto", "trama", "narrazione", "personaggio", "ambientazione", "tema", "conflitto", "risoluzione", "evento", "incidente", "cronaca", "saga", "aneddoto", "favola", "leggenda", "mito", "parabola", "recital", "filone", "avventura", "episodio", "viaggio", "quest", "scena", "sequenza", "dramma", "linea narrativa", "memoria", "romanzo", "favola", "mitologia", "biografia", "autobiografia", "fiaba", "narrazione", "racconto breve", "novella", "racconto popolare"]
}

argument_keywords = {
    'en': ["because", "therefore", "thus", "hence", "since", "consequently", "as a result", "for this reason", "due to", "accordingly", "thereby", "ergo", "for", "because of", "on account of", "owing to", "seeing that", "inasmuch as", "as", "so", "henceforth", "thusly", "thereupon", "wherefore", "considering that", "due to the fact that", "in light of", "as a consequence", "resulting from", "reason being", "for the purpose of", "on these grounds", "by reason of", "in view of"],
    'it': ["perché", "quindi", "così", "pertanto", "poiché", "di conseguenza", "come risultato", "per questa ragione", "a causa di", "di conseguenza", "pertanto", "ergo", "per", "a causa di", "a motivo di", "dato che", "in quanto", "poiché", "visto che", "dunque", "da ciò", "perciò", "da allora", "per conseguenza", "considerando che", "a causa del fatto che", "alla luce di", "come conseguenza", "risultante da", "ragione essendo", "allo scopo di", "su queste basi", "per ragione di", "in vista di"]
}

persuasive_keywords = {
    'en': ["must", "should", "need", "important", "significant", "imperative", "essential", "vital", "crucial", "necessary", "require", "obligatory", "mandatory", "compulsory", "unavoidable", "key", "pivotal", "critical", "urgent", "indispensable", "pressing", "requisite", "paramount", "vital", "decisive", "weighty", "fundamental", "integral", "major", "substantial", "consequential", "compelling", "imperative", "prerequisite", "salient", "urgent", "mandatory"],
    'it': ["deve", "dovrebbe", "bisogno", "importante", "significativo", "imperativo", "essenziale", "vitale", "cruciale", "necessario", "richiedere", "obbligatorio", "mandatorio", "compulsorio", "inevitabile", "chiave", "fondamentale", "critico", "urgente", "indispensabile", "pressante", "requisito", "paramount", "vitale", "decisivo", "pesante", "fondamentale", "integrale", "maggiore", "sostanziale", "conseguente", "convincente", "imperativo", "prerequisito", "saliente", "urgente", "mandatorio"]
}

engaging_keywords = {
    'en': ["exciting", "interesting", "fascinating", "amazing", "incredible", "gripping", "compelling", "captivating", "thrilling", "enthralling", "spellbinding", "riveting", "absorbing", "arresting", "engaging", "mesmerizing", "stirring", "stimulating", "enchanting", "bewitching", "intriguing", "thought-provoking", "immersive", "enticing", "alluring", "dynamic", "electrifying", "invigorating", "exhilarating", "intoxicating", "engrossing", "bewildering", "eye-opening", "excitative", "inviting", "fascinative"],
    'it': ["eccitante", "interessante", "affascinante", "stupefacente", "incredibile", "avvincente", "coinvolgente", "accattivante", "emozionante", "entusiasmante", "incantevole", "travolgente", "assorbente", "sorprendente", "affascinante", "stimolante", "incantatore", "affascinante", "intrigante", "provocante", "immersivo", "allettante", "allettatore", "dinamico", "elettrizzante", "rinvigorente", "esilarante", "incantevole", "avventuroso", "inebriante", "accattivante", "affascinante", "ipnotico", "occhio-aprente", "eccitante", "invitante"]
}

def detect_language(text):
    # Simple heuristic to detect the language based on common stopwords
    words = word_tokenize(text.lower())
    if any(word in words for word in nltk.corpus.stopwords.words('english')):
        return 'en'
    elif any(word in words for word in nltk.corpus.stopwords.words('italian')):
        return 'it'
    else:
        return 'it'  # Default to Italian

def narrative_index(text, lang):
    sentences = sent_tokenize(text)
    keywords = narrative_keywords[lang]
    narrative_score = sum(1 for sentence in sentences if any(word in word_tokenize(sentence.lower()) for word in keywords))
    return narrative_score / len(sentences) if sentences else 0

def argument_strength(text, lang):
    sentences = sent_tokenize(text)
    keywords = argument_keywords[lang]
    argument_score = sum(1 for sentence in sentences if any(word in word_tokenize(sentence.lower()) for word in keywords))
    return argument_score / len(sentences) if sentences else 0

def persuasiveness_score(text, lang):
    words = word_tokenize(text)
    keywords = persuasive_keywords[lang]
    persuasive_score = sum(1 for word in words if word.lower() in keywords)
    return persuasive_score / len(words) if words else 0

def engagement_score(text, lang):
    sentences = sent_tokenize(text)
    keywords = engaging_keywords[lang]
    engagement_score = sum(1 for sentence in sentences if any(word in word_tokenize(sentence.lower()) for word in keywords))
    return engagement_score / len(sentences) if sentences else 0

def normalize_score(score, max_score):
    return score / max_score if max_score != 0 else 0

def evaluate_narrative_persuasiveness_metrics(text):
    lang = detect_language(text)
    metrics = {
        "Narrative Index": normalize_score(narrative_index(text, lang), 1),
        "Argument Strength": normalize_score(argument_strength(text, lang), 1),
        "Persuasiveness Score": normalize_score(persuasiveness_score(text, lang), 0.2),  # Adjusted max value
        "Engagement Score": normalize_score(engagement_score(text, lang), 0.2)  # Adjusted max value
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Narrative Index": 0.25,
        "Argument Strength": 0.25,
        "Persuasiveness Score": 0.25,
        "Engagement Score": 0.25,
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

    metrics, aggregated_score = evaluate_narrative_persuasiveness_metrics(text)

    output = {
        "Narrative Persuasiveness Metrics": metrics,
        "Aggregated Narrative Persuasiveness Score": aggregated_score
    }

    print("Text Narrative and Persuasiveness Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"Aggregated Narrative and Persuasiveness Score: {aggregated_score:.4f}")


    # Export results to JSON
    output_file_path = file_path.replace(".json", "_metrics_narrative_persuasiveness.json")
    with open(output_file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)
    print(f"Metrics exported to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_narrative_persuasiveness.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
