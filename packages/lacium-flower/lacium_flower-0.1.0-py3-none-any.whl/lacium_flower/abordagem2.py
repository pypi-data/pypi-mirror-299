import pyphen
import nltk
from nltk.corpus import stopwords

# Configurando Pyphen para português brasileiro
dic = pyphen.Pyphen(lang='pt_BR')

# Definição dos pesos para os 4 níveis de consciência fonológica
PESOS = {
    "rima": 4,
    "silaba": 3,
    "intrassilabica": 2,
    "fonemica": 1
}

# Certificando que as stopwords estão baixadas
nltk.download("stopwords")

############## Abordagem Embeddings com Pyphen/NLTK ##############

def get_word_features(word):
    """
    Extrai as características da palavra usando Pyphen para separação em sílabas e NLTK para análise de stopwords.
    
    :param word: Palavra a ser analisada
    :return: Dicionário de características extraídas da palavra
    """
    if isinstance(word, str):
        word = word.lower()
        syllables = dic.inserted(word).split("-")
        num_syllables = len(syllables)
        is_monosyllabic = num_syllables == 1

        if is_monosyllabic:
            tonic = "Monossílaba"
        else:
            if word[-1] in "aeiouáéíóú":
                tonic = "Oxítona"
            elif word[-2] in "aeiouáéíóú":
                tonic = "Paroxítona"
            else:
                tonic = "Proparoxítona"

        rima = word[-2:] if not is_monosyllabic else word
        ataque = syllables[0][0] if not is_monosyllabic else word[0]
        coda = syllables[-1][-1] if not is_monosyllabic else None
        nucleo = ''.join([silaba[1:] for silaba in syllables if len(silaba) > 1])
        ultima_silaba = syllables[-1]

        if isinstance(ultima_silaba, str) and ultima_silaba[-1] in "aeiouáéíóú":
            syllable_ending = "Sílaba Aberta"
        else:
            syllable_ending = "Sílaba Fechada"

        is_stopword = word in stopwords.words("portuguese")

        # Retorna um dicionário de características da palavra
        embedding = {
            "Nível 1 - Rima": rima,
            "Nível 1 - Aliterações": ataque,
            "Nível 2 - Número de Sílabas": num_syllables,
            "Nível 2 - Ordem das Sílabas Invertidas": '-'.join(reversed(syllables)),
            "Nível 2 - Última Sílaba": ultima_silaba,
            "Nível 3 - Ataque": ataque,
            "Nível 3 - Núcleo": nucleo,
            "Nível 3 - Coda": coda,
            "Nível 3 - Tonicidade": tonic,
            "Nível 4 - Sílaba Aberta ou Fechada": syllable_ending,
            "Nível 4 - Stopword": is_stopword
        }

        return embedding
    return {}

def calcular_similaridade_abordagem_embeddings_pyphen_nltk(palavra_alvo, palavra):
    """
    Calcula a similaridade entre duas palavras usando as características extraídas via Pyphen e NLTK.
    
    :param palavra_alvo: Palavra alvo
    :param palavra: Palavra a ser comparada
    :return: Score de similaridade entre as palavras
    """
    features_alvo = get_word_features(palavra_alvo)
    features_palavra = get_word_features(palavra)

    score = 0
    if features_alvo and features_palavra:
        if features_alvo["Nível 1 - Rima"] == features_palavra["Nível 1 - Rima"]:
            score += PESOS["rima"]
        if features_alvo["Nível 1 - Aliterações"] == features_palavra["Nível 1 - Aliterações"]:
            score += PESOS["rima"]

        if features_alvo["Nível 2 - Número de Sílabas"] == features_palavra["Nível 2 - Número de Sílabas"]:
            score += PESOS["silaba"]
        if features_alvo["Nível 3 - Ataque"] == features_palavra["Nível 3 - Ataque"]:
            score += PESOS["intrassilabica"]
    return score

# Função para encontrar a palavra mais similar na Abordagem Embeddings com Pyphen/NLTK
def encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk(palavra_alvo, vocabulario):
    """
    Encontra a palavra mais similar no vocabulário usando a Abordagem Embeddings com Pyphen/NLTK.
    
    :param palavra_alvo: Palavra alvo
    :param vocabulario: Lista de palavras do vocabulário
    :return: Palavra mais similar
    """
    similaridades = [(palavra, calcular_similaridade_abordagem_embeddings_pyphen_nltk(palavra_alvo, palavra)) for palavra in vocabulario]
    similaridades.sort(key=lambda x: x[1], reverse=True)
    return similaridades[0][0]  # Retorna a palavra com maior similaridade
