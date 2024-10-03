import numpy as np
from sklearn.metrics import accuracy_score
import Levenshtein

# Função para avaliar uma abordagem com base em um conjunto de teste
def avaliar_abordagem(abordagem_func, nome_abordagem, conjunto_de_teste, vocabulario):
    """
    Avalia uma abordagem de similaridade com base em um conjunto de teste.
    
    :param abordagem_func: Função da abordagem que será avaliada
    :param nome_abordagem: Nome da abordagem a ser avaliada
    :param conjunto_de_teste: Lista de dicionários contendo palavras alvo e similares esperadas
    :param vocabulario: Lista de palavras no vocabulário a ser testado
    :return: Acurácia e distância média de Levenshtein
    """
    palavras_preditas = []
    palavras_reais = [teste["similar_esperada"] for teste in conjunto_de_teste]
    distancias_levenshtein = []

    for teste in conjunto_de_teste:
        palavra_alvo = teste["palavra_alvo"]
        similar_esperada = teste["similar_esperada"]

        # Aplicando a abordagem para encontrar a palavra similar
        palavra_predita = abordagem_func(palavra_alvo, vocabulario)
        palavras_preditas.append(palavra_predita)

        # Calculando a distância de Levenshtein entre a palavra predita e a palavra esperada
        distancia = Levenshtein.distance(similar_esperada, palavra_predita)
        distancias_levenshtein.append(distancia)

    # Calculando métricas
    acuracia = accuracy_score(palavras_reais, palavras_preditas)
    media_distancia_levenshtein = np.mean(distancias_levenshtein)

    print(f"Resultados para a abordagem: {nome_abordagem}")
    print(f"Acurácia: {acuracia * 100:.2f}%")
    print(f"Distância média de Levenshtein: {media_distancia_levenshtein:.2f}\n")
    
    return acuracia, media_distancia_levenshtein

# Função principal para avaliar todas as abordagens
def avaliar_todas_abordagens(conjunto_de_teste, vocabulario):
    """
    Avalia as três abordagens de similaridade com o conjunto de teste fornecido.
    
    :param conjunto_de_teste: Lista de dicionários contendo palavras alvo e similares esperadas
    :param vocabulario: Lista de palavras no vocabulário
    """
    from your_library.abordagem1 import encontrar_palavra_mais_similar_abordagem_fonologica
    from your_library.abordagem2 import encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk
    from your_library.abordagem3 import encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao

    # Avaliar Abordagem 1: Fonológica Clássica
    avaliar_abordagem(encontrar_palavra_mais_similar_abordagem_fonologica, "Abordagem Fonológica Clássica", conjunto_de_teste, vocabulario)

    # Avaliar Abordagem 2: Embeddings com Pyphen/NLTK
    avaliar_abordagem(encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk, "Abordagem Embeddings com Pyphen/NLTK", conjunto_de_teste, vocabulario)

    # Avaliar Abordagem 3: Embeddings com BERT/Autoatenção
    avaliar_abordagem(encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao, "Abordagem Embeddings com BERT/Autoatenção", conjunto_de_teste, vocabulario)


############## Exemplo de Conjunto de Teste e Vocabulario ##############

# Exemplo de conjunto de teste
conjunto_de_teste = [
    {"palavra_alvo": "casa", "similar_esperada": "asa"},
    {"palavra_alvo": "fada", "similar_esperada": "hada"},
    {"palavra_alvo": "pato", "similar_esperada": "gato"},
    {"palavra_alvo": "cada", "similar_esperada": "nada"}
]

# Exemplo de vocabulário
vocabulario = ["asa", "fada", "gato", "nada", "mala", "hada", "pata", "casa"]

# Avaliação de todas as abordagens
if __name__ == "__main__":
    avaliar_todas_abordagens(conjunto_de_teste, vocabulario)
