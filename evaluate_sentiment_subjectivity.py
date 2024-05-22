import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords
from langdetect import detect

# Ensure nltk resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Define sentiment analysis functions
def calculate_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def calculate_sentiment_consistency(sentiments):
    positive = sum(1 for sentiment in sentiments if sentiment > 0)
    negative = sum(1 for sentiment in sentiments if sentiment < 0)
    neutral = sum(1 for sentiment in sentiments if sentiment == 0)
    total = len(sentiments)
    return max(positive, negative, neutral) / total if total > 0 else 0

def calculate_polarity_score(sentiments):
    return sum(sentiments) / len(sentiments) if sentiments else 0

def calculate_subjectivity_intensity(subjectivities):
    return sum(subjectivities) / len(subjectivities) if subjectivities else 0

def calculate_sentiment_variability(sentiments):
    return max(sentiments) - min(sentiments) if sentiments else 0

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'it'  # Default to Italian

def translate_to_english(text, lang):
    if lang != 'en':
        blob = TextBlob(text)
        text = str(blob.translate(to='en'))
    return text

def evaluate_sentiment_subjectivity_metrics(text, lang):
    text = translate_to_english(text, lang)
    sentences = sent_tokenize(text)
    sentiments = []
    subjectivities = []

    for sentence in sentences:
        polarity, subjectivity = calculate_sentiment(sentence)
        sentiments.append(polarity)
        subjectivities.append(subjectivity)

    metrics = {
        "Sentiment Consistency": calculate_sentiment_consistency(sentiments),
        "Polarity Score": calculate_polarity_score(sentiments),
        "Subjectivity Intensity": calculate_subjectivity_intensity(subjectivities),
        "Sentiment Variability": calculate_sentiment_variability(sentiments)
    }

    # Calculate aggregated score (weights sum up to 1, scaled to 100)
    weights = {
        "Sentiment Consistency": 0.25,
        "Polarity Score": 0.25,
        "Subjectivity Intensity": 0.25,
        "Sentiment Variability": 0.25
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

    lang = detect_language(text)
    metrics, aggregated_score = evaluate_sentiment_subjectivity_metrics(text, lang)

    print("Text Sentiment and Subjectivity Metrics:")
    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")
    print(f"Aggregated Sentiment and Subjectivity Score: {aggregated_score:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_sentiment_subjectivity.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
