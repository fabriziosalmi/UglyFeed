from flask import Flask, request, jsonify
import textstat
import nltk
import spacy
from collections import Counter
from textblob import TextBlob
import string

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

import nltk
from nltk.corpus import cmudict
import textstat
from textblob import TextBlob

nltk.download('cmudict')
d = cmudict.dict()

# Function: Type-Token Ratio (TTR)
def type_token_ratio(text):
    words = nltk.word_tokenize(text)
    return len(set(words)) / len(words) if words else 0

# Function: Hapax Legomena Ratio
def hapax_legomena_ratio(text):
    words = nltk.word_tokenize(text)
    freq_dist = nltk.FreqDist(words)
    hapaxes = freq_dist.hapaxes()
    return len(hapaxes) / len(words) if words else 0

# Function: Sentence Complexity
def sentence_complexity(text):
    sentences = nltk.sent_tokenize(text)
    clauses = [len(nltk.sent_tokenize(sentence)) for sentence in sentences]
    return sum(clauses) / len(sentences) if sentences else 0

# Function: Average Syllables per Word
def average_syllables_per_word(text):
    words = nltk.word_tokenize(text)
    total_syllables = sum(textstat.syllable_count(word) for word in words)
    return total_syllables / len(words) if words else 0

# Function: Lexical Density
def lexical_density(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    content_words = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('VB') or pos.startswith('JJ') or pos.startswith('RB')]
    return len(content_words) / len(words) if words else 0

# Function: Polysyllabic Words Count
def polysyllabic_words_count(text):
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if textstat.syllable_count(word) > 2)

# Function: Reading Time (in seconds)
def reading_time_seconds(text):
    words = nltk.word_tokenize(text)
    words_per_minute = 200
    return (len(words) / words_per_minute) * 60

# Function: Speaking Time (in seconds)
def speaking_time_seconds(text):
    words = nltk.word_tokenize(text)
    words_per_minute = 150
    return (len(words) / words_per_minute) * 60

# Function: Sentiment Analysis
def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Function: Count Complex Words
def count_complex_words(text):
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if textstat.syllable_count(word) >= 3)

# Function: Automated Readability Index (ARI)
def automated_readability_index(text):
    words = textstat.lexicon_count(text, removepunct=True)
    sentences = textstat.sentence_count(text)
    characters = sum(len(word) for word in text if word.isalnum())
    return 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43

# Function: Spache Readability Formula
def spache_readability(text):
    return textstat.spache_readability(text)

# Function: Dale-Chall Readability Score
def dale_chall_readability(text):
    return textstat.dale_chall_readability_score(text)

# Function: Count Unique Syllables
def count_unique_syllables(text):
    words = nltk.word_tokenize(text)
    unique_syllables = set()
    for word in words:
        syllables = textstat.syllable_count(word)
        unique_syllables.update(str(syllables).split())
    return len(unique_syllables)

# Function: Count Function Words
def count_function_words(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if word.lower() in stopwords)

# Function: Lexical Variation
def lexical_variation(text):
    words = nltk.word_tokenize(text)
    return len(set(words)) / len(words) if words else 0

# Function: Word Length Variation
def word_length_variation(text):
    words = nltk.word_tokenize(text)
    word_lengths = [len(word) for word in words]
    return max(word_lengths) - min(word_lengths) if word_lengths else 0

# Function: Average Word Frequency Class
def average_word_frequency_class(text):
    words = nltk.word_tokenize(text)
    freq_dist = nltk.FreqDist(words)
    total_freq_class = sum(1 / freq_dist.freq(word) for word in words)
    return total_freq_class / len(words) if words else 0

# Function: Gunning Fog Index
def gunning_fog_index(text):
    return textstat.gunning_fog(text)



def lexical_diversity(text):
    words = nltk.word_tokenize(text)
    return len(set(words)) / len(words) if words else 0

def reading_time(text):
    words = nltk.word_tokenize(text)
    words_per_minute = 200
    return len(words) / words_per_minute

def speaking_time(text):
    words = nltk.word_tokenize(text)
    words_per_minute = 150
    return len(words) / words_per_minute

def count_stopwords(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if word.lower() in stopwords)

def count_punctuation(text):
    return sum(1 for char in text if char in string.punctuation)

def count_conjunctions(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos in ['CC'])

def count_prepositions(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos in ['IN'])

def count_determiners(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos in ['DT'])

def count_pronouns(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos in ['PRP', 'PRP$', 'WP', 'WP$'])

def count_interjections(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos in ['UH'])

def count_uppercase_words(text):
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if word.isupper())

def count_lowercase_words(text):
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if word.islower())

def count_digits(text):
    return sum(1 for char in text if char.isdigit())

def count_alphabetic_characters(text):
    return sum(1 for char in text if char.isalpha())

def count_non_alphabetic_characters(text):
    return sum(1 for char in text if not char.isalpha())

def count_interrogative_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sum(1 for sentence in sentences if sentence.endswith('?'))

def count_exclamatory_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sum(1 for sentence in sentences if sentence.endswith('!'))

def count_imperative_sentences(text):
    sentences = nltk.sent_tokenize(text)
    pos_tags = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]
    return sum(1 for tags in pos_tags if tags and tags[0][1] in ['VB', 'MD'])

def count_declarative_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sum(1 for sentence in sentences if sentence.endswith('.'))

def count_base_forms_of_verbs(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos == 'VB')

def count_past_tense_verbs(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos == 'VBD')

def count_past_participle_verbs(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos == 'VBN')

def count_gerund_or_present_participle_verbs(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return sum(1 for word, pos in pos_tags if pos == 'VBG')

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def count_unique_characters(text):
    return len(set(text))

def count_monosyllabic_words(text):
    words = nltk.word_tokenize(text)
    return sum(1 for word in words if textstat.syllable_count(word) == 1)

def lix_readability(text):
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    long_words = sum(1 for word in words if len(word) > 6)
    return len(words) / len(sentences) + 100 * (long_words / len(words)) if words else 0

def rix_readability(text):
    words = nltk.word_tokenize(text)
    long_words = sum(1 for word in words if len(word) > 6)
    return long_words / len(nltk.sent_tokenize(text)) if words else 0

def custom_metrics(text):
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)

    pos_tags = nltk.pos_tag(words)
    pos_counts = Counter(tag for word, tag in pos_tags)

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    entity_counts = Counter(ent.label_ for ent in doc.ents)

    sentiment_polarity, subjectivity = sentiment_analysis(text)

def custom_metrics(text):
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)

    pos_tags = nltk.pos_tag(words)
    pos_counts = Counter(tag for word, tag in pos_tags)

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    entity_counts = Counter(ent.label_ for ent in doc.ents)

    sentiment_polarity, subjectivity = sentiment_analysis(text)

    metrics = {
        'noun_count': sum(1 for word, pos in pos_tags if pos.startswith('NN')),
        'verb_count': sum(1 for word, pos in pos_tags if pos.startswith('VB')),
        'adjective_count': sum(1 for word, pos in pos_tags if pos.startswith('JJ')),
        'adverb_count': sum(1 for word, pos in pos_tags if pos.startswith('RB')),
        'unique_words': len(set(words)),
        'unique_characters': count_unique_characters(text),
        'stopword_count': count_stopwords(text),
        'punctuation_count': count_punctuation(text),
        'conjunction_count': count_conjunctions(text),
        'preposition_count': count_prepositions(text),
        'determiner_count': count_determiners(text),
        'pronoun_count': count_pronouns(text),
        'interjection_count': count_interjections(text),
        'uppercase_word_count': count_uppercase_words(text),
        'lowercase_word_count': count_lowercase_words(text),
        'digit_count': count_digits(text),
        'alphabetic_character_count': count_alphabetic_characters(text),
        'non_alphabetic_character_count': count_non_alphabetic_characters(text),
        'monosyllabic_word_count': count_monosyllabic_words(text),
        'entity_count': len(entities),
        'entity_labels': dict(entity_counts),
        'average_sentence_length': sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0,
        'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
        'lexical_diversity': lexical_diversity(text),
        'estimated_reading_time_minutes': reading_time(text),
        'estimated_speaking_time_minutes': speaking_time(text),
        'sentiment_polarity': sentiment_polarity,
        'subjectivity': subjectivity,
        'lix_readability': lix_readability(text),
        'rix_readability': rix_readability(text),
        'interrogative_sentence_count': count_interrogative_sentences(text),
        'exclamatory_sentence_count': count_exclamatory_sentences(text),
        'imperative_sentence_count': count_imperative_sentences(text),
        'declarative_sentence_count': count_declarative_sentences(text),
        'base_form_verb_count': count_base_forms_of_verbs(text),
        'past_tense_verb_count': count_past_tense_verbs(text),
        'past_participle_verb_count': count_past_participle_verbs(text),
        'gerund_present_participle_verb_count': count_gerund_or_present_participle_verbs(text),
        'type_token_ratio': type_token_ratio(text),
        'hapax_legomena_ratio': hapax_legomena_ratio(text),
        'sentence_complexity': sentence_complexity(text),
        'average_syllables_per_word': average_syllables_per_word(text),
        'lexical_density': lexical_density(text),
        'polysyllabic_words_count': polysyllabic_words_count(text),
        'reading_time_seconds': reading_time_seconds(text),
        'speaking_time_seconds': speaking_time_seconds(text),
        'complex_words_count': count_complex_words(text),
        'automated_readability_index': automated_readability_index(text),
        'spache_readability': spache_readability(text),
        'dale_chall_readability': dale_chall_readability(text),
        'unique_syllables_count': count_unique_syllables(text),
        'function_words_count': count_function_words(text),
        'lexical_variation': lexical_variation(text),
        'word_length_variation': word_length_variation(text),
        'average_word_frequency_class': average_word_frequency_class(text),
        'gunning_fog_index': gunning_fog_index(text),
    }

    for tag, count in pos_counts.items():
        metrics[f'pos_count_{tag}'] = count

    return metrics

def compute_text_metrics(text):
    metrics = {
        'word_count': len(text.split()),
        'character_count': len(text),
        'sentence_count': textstat.sentence_count(text),
        'syllable_count': textstat.syllable_count(text),
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'smog_index': textstat.smog_index(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'coleman_liau_index': textstat.coleman_liau_index(text),
        'automated_readability_index': textstat.automated_readability_index(text),
        'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
        'difficult_words': textstat.difficult_words(text),
        'linsear_write_formula': textstat.linsear_write_formula(text),
        'gunning_fog': textstat.gunning_fog(text),
        'text_standard': textstat.text_standard(text),
        'average_word_length': sum(len(word) for word in text.split()) / len(text.split()) if text.split() else 0,
        'reading_time_seconds': textstat.reading_time(text, 200)
    }

    custom = custom_metrics(text)
    metrics.update(custom)

    return metrics

@app.route('/metrics', methods=['POST'])
def get_metrics():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    metrics = compute_text_metrics(text)
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
