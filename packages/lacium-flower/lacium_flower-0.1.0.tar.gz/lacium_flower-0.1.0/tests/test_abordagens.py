import unittest
from lacium_flower.abordagem1 import calcular_similaridade_abordagem_fonologica, encontrar_palavra_mais_similar_abordagem_fonologica
from lacium_flower.abordagem2 import calcular_similaridade_abordagem_embeddings_pyphen_nltk, encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk
from lacium_flower.abordagem3 import calcular_similaridade_abordagem_embeddings_bert_autoatencao, encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao

class TestLaciumFlower(unittest.TestCase):

    def setUp(self):
        # Configura um vocabulário de teste e conjunto de palavras para testar
        self.vocabulario = ["asa", "fada", "gato", "nada", "mala", "hada", "pata", "casa"]
        self.palavra_alvo = "casa"

    # Testes para a Abordagem 1: Fonológica Clássica
    def test_calcular_similaridade_abordagem_fonologica(self):
        similaridade = calcular_similaridade_abordagem_fonologica("casa", "asa")
        self.assertGreater(similaridade, 0, "A similaridade fonológica deveria ser maior que 0")

    def test_encontrar_palavra_mais_similar_abordagem_fonologica(self):
        palavra_similar = encontrar_palavra_mais_similar_abordagem_fonologica(self.palavra_alvo, self.vocabulario)
        self.assertEqual(palavra_similar, "asa", "A palavra mais similar deveria ser 'asa' na abordagem fonológica")

    # Testes para a Abordagem 2: Embeddings com Pyphen/NLTK
    def test_calcular_similaridade_abordagem_embeddings_pyphen_nltk(self):
        similaridade = calcular_similaridade_abordagem_embeddings_pyphen_nltk("casa", "asa")
        self.assertGreater(similaridade, 0, "A similaridade de embeddings com Pyphen/NLTK deveria ser maior que 0")

    def test_encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk(self):
        palavra_similar = encontrar_palavra_mais_similar_abordagem_embeddings_pyphen_nltk(self.palavra_alvo, self.vocabulario)
        self.assertEqual(palavra_similar, "asa", "A palavra mais similar deveria ser 'asa' na abordagem Embeddings com Pyphen/NLTK")

    # Testes para a Abordagem 3: Embeddings com BERT/Autoatenção
    def test_calcular_similaridade_abordagem_embeddings_bert_autoatencao(self):
        similaridade = calcular_similaridade_abordagem_embeddings_bert_autoatencao("casa", "asa")
        self.assertGreater(similaridade, 0, "A similaridade de embeddings com BERT/Autoatenção deveria ser maior que 0")

    def test_encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao(self):
        palavra_similar = encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao(self.palavra_alvo, self.vocabulario)
        self.assertIn(palavra_similar, self.vocabulario, "A palavra mais similar deve estar presente no vocabulário")
        
if __name__ == '__main__':
    unittest.main()
