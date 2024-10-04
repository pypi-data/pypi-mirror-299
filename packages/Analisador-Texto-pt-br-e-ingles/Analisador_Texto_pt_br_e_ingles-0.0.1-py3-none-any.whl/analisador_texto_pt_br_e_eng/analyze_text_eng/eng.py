import spacy
from collections import Counter

nlp = spacy.load("en_core_web_lg")

def analyze_text(text):
    doc = nlp(text.lower())
    filtered_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_count = Counter(filtered_tokens)
    return {
        'total_words': len([token for token in doc if not token.is_punct]),
        'filtered_words': len(filtered_tokens),
        'most_common_words': word_count.most_common(5)
    }
