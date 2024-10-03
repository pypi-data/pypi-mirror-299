# Inicializando o pacote Lacium Flower

# Importando as funções principais de cada abordagem

from .abordagem1 import (
    calcular_similaridade_abordagem_fonologica,
    encontrar_palavra_mais_similar_abordagem_fonologica
)

from .abordagem2 import (
    calcular_similaridade_abordagem_embeddings_pyphen_nltk,
    encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk
)

from .abordagem3 import (
    calcular_similaridade_abordagem_embeddings_bert_autoatencao,
    encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao
)

__all__ = [
    "calcular_similaridade_abordagem_fonologica",
    "encontrar_palavra_mais_similar_abordagem_fonologica",
    "calcular_similaridade_abordagem_embeddings_pyphen_nltk",
    "encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk",
    "calcular_similaridade_abordagem_embeddings_bert_autoatencao",
    "encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao"
]
