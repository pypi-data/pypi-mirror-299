import spacy
from collections import Counter


nlp = spacy.load("pt_core_news_lg")

def analisar_texto(texto):
    doc = nlp(texto.lower())
    tokens_filtrados = [token.text for token in doc if not token.is_stop and not token.is_punct]
    contagem_palavras = Counter(tokens_filtrados)
    return {
        'total_palavras': len([token for token in doc if not token.is_punct]),
        'palavras_filtradas': len(tokens_filtrados),
        'palavras_mais_comuns': contagem_palavras.most_common(5)
    }
