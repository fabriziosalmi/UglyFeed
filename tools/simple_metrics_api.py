import gradio as gr
import nltk
import spacy
import textstat
from collections import Counter
from textblob import TextBlob
import string
from langdetect import detect, LangDetectException
import pandas as pd

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('cmudict', quiet=True)

# Load CMU Pronouncing Dictionary
d = nltk.corpus.cmudict.dict()

# Initialize language models dictionary
spacy_models = {
    "en": "en_core_web_sm",
    "es": "es_core_news_sm",
    "fr": "fr_core_news_sm",
    "de": "de_core_news_sm",
    "it": "it_core_news_sm"
}

# Function to get SpaCy model for a given language
def get_spacy_model(language_code):
    if language_code in spacy_models:
        try:
            return spacy.load(spacy_models[language_code])
        except OSError:
            spacy.cli.download(spacy_models[language_code])
            return spacy.load(spacy_models[language_code])
    else:
        # Return English model as a fallback
        return spacy.load("en_core_web_sm")

# Utility functions
def tokenize_text(text):
    return nltk.word_tokenize(text)

def pos_tag_text(text):
    words = tokenize_text(text)
    return nltk.pos_tag(words)

# Function Definitions
def type_token_ratio(words):
    return len(set(words)) / len(words) if words else 0

def hapax_legomena_ratio(words):
    freq_dist = nltk.FreqDist(words)
    hapaxes = freq_dist.hapaxes()
    return len(hapaxes) / len(words) if words else 0

def sentence_complexity(sentences):
    clauses = [len(nltk.sent_tokenize(sentence)) for sentence in sentences]
    return sum(clauses) / len(sentences) if sentences else 0

def average_syllables_per_word(words):
    total_syllables = sum(textstat.syllable_count(word) for word in words)
    return total_syllables / len(words) if words else 0

def lexical_density(pos_tags):
    content_words = [word for word, pos in pos_tags if pos.startswith(('NN', 'VB', 'JJ', 'RB'))]
    return len(content_words) / len(pos_tags) if pos_tags else 0

def polysyllabic_words_count(words):
    return sum(1 for word in words if textstat.syllable_count(word) > 2)

def reading_time_seconds(words, words_per_minute=200):
    return (len(words) / words_per_minute) * 60

def speaking_time_seconds(words, words_per_minute=150):
    return (len(words) / words_per_minute) * 60

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def count_complex_words(words):
    return sum(1 for word in words if textstat.syllable_count(word) >= 3)

def automated_readability_index(text):
    words = textstat.lexicon_count(text, removepunct=True)
    sentences = textstat.sentence_count(text)
    characters = sum(len(word) for word in text if word.isalnum())
    return 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43

def custom_metrics(text, lang_model):
    words = tokenize_text(text)
    sentences = nltk.sent_tokenize(text)
    pos_tags = pos_tag_text(text)
    doc = lang_model(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    entity_counts = Counter(ent.label_ for ent in doc.ents)
    sentiment_polarity, subjectivity = sentiment_analysis(text)

    metrics = {
        'Noun Count': sum(1 for word, pos in pos_tags if pos.startswith('NN')),
        'Verb Count': sum(1 for word, pos in pos_tags if pos.startswith('VB')),
        'Adjective Count': sum(1 for word, pos in pos_tags if pos.startswith('JJ')),
        'Adverb Count': sum(1 for word, pos in pos_tags if pos.startswith('RB')),
        'Unique Words': len(set(words)),
        'Unique Characters': len(set(text)),
        'Stopword Count': sum(1 for word in words if word.lower() in set(nltk.corpus.stopwords.words('english'))),
        'Punctuation Count': sum(1 for char in text if char in string.punctuation),
        'Conjunction Count': sum(1 for word, pos in pos_tags if pos == 'CC'),
        'Preposition Count': sum(1 for word, pos in pos_tags if pos == 'IN'),
        'Determiner Count': sum(1 for word, pos in pos_tags if pos == 'DT'),
        'Pronoun Count': sum(1 for word, pos in pos_tags if pos in ['PRP', 'PRP$', 'WP', 'WP$']),
        'Interjection Count': sum(1 for word, pos in pos_tags if pos == 'UH'),
        'Uppercase Word Count': sum(1 for word in words if word.isupper()),
        'Lowercase Word Count': sum(1 for word in words if word.islower()),
        'Digit Count': sum(1 for char in text if char.isdigit()),
        'Alphabetic Character Count': sum(1 for char in text if char.isalpha()),
        'Non-Alphabetic Character Count': sum(1 for char in text if not char.isalpha()),
        'Monosyllabic Word Count': sum(1 for word in words if textstat.syllable_count(word) == 1),
        'Entity Count': len(entities),
        'Entity Labels': dict(entity_counts),
        'Average Sentence Length': sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0,
        'Average Word Length': sum(len(word) for word in words) / len(words) if words else 0,
        'Lexical Diversity': len(set(words)) / len(words) if words else 0,
        'Estimated Reading Time (minutes)': reading_time_seconds(words) / 60,
        'Estimated Speaking Time (minutes)': speaking_time_seconds(words) / 60,
        'Sentiment Polarity': sentiment_polarity,
        'Sentiment Subjectivity': subjectivity,
        'LIX Readability': textstat.lix(text),
        'RIX Readability': textstat.rix(text),
        'Interrogative Sentence Count': sum(1 for sentence in sentences if sentence.endswith('?')),
        'Exclamatory Sentence Count': sum(1 for sentence in sentences if sentence.endswith('!')),
        'Imperative Sentence Count': sum(1 for tags in [pos_tag_text(sentence) for sentence in sentences] if tags and tags[0][1] in ['VB', 'MD']),
        'Declarative Sentence Count': sum(1 for sentence in sentences if sentence.endswith('.')),
        'Base Form Verb Count': sum(1 for word, pos in pos_tags if pos == 'VB'),
        'Past Tense Verb Count': sum(1 for word, pos in pos_tags if pos == 'VBD'),
        'Past Participle Verb Count': sum(1 for word, pos in pos_tags if pos == 'VBN'),
        'Gerund/Present Participle Verb Count': sum(1 for word, pos in pos_tags if pos == 'VBG'),
        'Type-Token Ratio': type_token_ratio(words),
        'Hapax Legomena Ratio': hapax_legomena_ratio(words),
        'Sentence Complexity': sentence_complexity(sentences),
        'Average Syllables per Word': average_syllables_per_word(words),
        'Lexical Density': lexical_density(pos_tags),
        'Polysyllabic Words Count': polysyllabic_words_count(words),
        'Reading Time (seconds)': reading_time_seconds(words),
        'Speaking Time (seconds)': speaking_time_seconds(words),
        'Complex Words Count': count_complex_words(words),
        'Automated Readability Index': automated_readability_index(text),
        'Spache Readability': textstat.spache_readability(text),
        'Dale-Chall Readability': textstat.dale_chall_readability_score(text),
        'Unique Syllables Count': len(set(textstat.syllable_count(word) for word in words)),
        'Function Words Count': sum(1 for word in words if word.lower() in set(nltk.corpus.stopwords.words('english'))),
        'Lexical Variation': len(set(words)) / len(words) if words else 0,
        'Word Length Variation': max(len(word) for word in words) - min(len(word) for word in words) if words else 0,
        'Average Word Frequency Class': sum(1 / nltk.FreqDist(words).freq(word) for word in words) / len(words) if words else 0,
        'Gunning Fog Index': textstat.gunning_fog(text),
    }

    for tag, count in Counter(tag for word, tag in pos_tags).items():
        metrics[f'POS Count {tag}'] = count

    return metrics

def compute_text_metrics(text):
    # Detect language
    try:
        language_code = detect(text)
    except LangDetectException:
        return pd.DataFrame([{'Metric': 'Error', 'Value': 'Unable to detect language'}])

    # Load appropriate SpaCy model
    lang_model = get_spacy_model(language_code)

    words = tokenize_text(text)
    sentences = nltk.sent_tokenize(text)

    metrics = {
        'Word Count': len(words),
        'Character Count': len(text),
        'Sentence Count': len(sentences),
        'Syllable Count': textstat.syllable_count(text),
        'Flesch Reading Ease': textstat.flesch_reading_ease(text),
        'SMOG Index': textstat.smog_index(text),
        'Flesch-Kincaid Grade': textstat.flesch_kincaid_grade(text),
        'Coleman-Liau Index': textstat.coleman_liau_index(text),
        'Automated Readability Index': textstat.automated_readability_index(text),
        'Dale-Chall Readability Score': textstat.dale_chall_readability_score(text),
        'Difficult Words': textstat.difficult_words(text),
        'Linsear Write Formula': textstat.linsear_write_formula(text),
        'Gunning Fog': textstat.gunning_fog(text),
        'Text Standard': textstat.text_standard(text),
        'Average Word Length': sum(len(word) for word in words) / len(words) if words else 0,
        'Reading Time (seconds)': textstat.reading_time(text, 200),
    }

    custom = custom_metrics(text, lang_model)
    metrics.update(custom)

    df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    return df

def gradio_interface(text):
    metrics = compute_text_metrics(text)
    return metrics

# Create a Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=10, placeholder="Enter text here..."),
    outputs=gr.Dataframe(),
    title="Text Metrics Calculator",
    description="Paste the text and get various readability and text metrics calculated.",
)

if __name__ == "__main__":
    iface.launch(share=True)
