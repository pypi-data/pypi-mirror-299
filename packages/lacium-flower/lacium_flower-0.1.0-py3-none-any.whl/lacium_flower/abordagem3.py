import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel

# Carregar o modelo e tokenizer do BERT para a Abordagem Embeddings com BERT/Autoatenção
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
bert_model = BertModel.from_pretrained('neuralmind/bert-base-portuguese-cased')

############## Abordagem Embeddings com BERT/Autoatenção ##############

class AutoAttentionModel(nn.Module):
    """
    Implementação de um modelo de autoatenção simples usando BERT embeddings.
    """
    def __init__(self, embed_dim, num_heads):
        super(AutoAttentionModel, self).__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.linear = nn.Linear(embed_dim, 1)

    def forward(self, query, key, value):
        """
        Método forward do modelo de autoatenção.
        :param query: Query tensor
        :param key: Key tensor
        :param value: Value tensor
        :return: Resultado da atenção e pesos de atenção
        """
        attn_output, attn_weights = self.attention(query, key, value)
        output = self.linear(attn_output)
        return output, attn_weights


def obter_embedding(palavra):
    """
    Obtém o embedding BERT para uma palavra.
    
    :param palavra: Palavra a ser embebida
    :return: Embedding BERT da palavra
    """
    if isinstance(palavra, str):
        inputs = tokenizer(palavra, return_tensors='pt')
        outputs = bert_model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.squeeze(0)
    return torch.zeros(768)  # Retorna um tensor vazio se a palavra não for válida


def calcular_similaridade_abordagem_embeddings_bert_autoatencao(palavra_alvo, palavra):
    """
    Calcula a similaridade entre duas palavras usando embeddings BERT e autoatenção.
    
    :param palavra_alvo: Palavra alvo
    :param palavra: Palavra a ser comparada
    :return: Score de similaridade
    """
    # Preparando os embeddings para a palavra alvo e a palavra de vocabulário
    embeddings_alvo = obter_embedding(palavra_alvo).unsqueeze(0)  # Transformar para dimensão (1, embed_dim)
    embeddings_vocabulario = obter_embedding(palavra).unsqueeze(0)  # Transformar para dimensão (1, embed_dim)

    # Redimensionando para (batch_size, seq_length, embed_dim) necessário para a atenção
    embeddings_alvo = embeddings_alvo.unsqueeze(0)  # Resulta em (1, 1, embed_dim)
    embeddings_vocabulario = embeddings_vocabulario.unsqueeze(0)  # Resulta em (1, 1, embed_dim)

    embed_dim = embeddings_alvo.shape[-1]
    num_heads = 4

    # Criando o modelo de autoatenção
    model = AutoAttentionModel(embed_dim, num_heads)

    # Calculando a atenção entre a palavra alvo e a palavra do vocabulário
    output, attn_weights = model(embeddings_alvo, embeddings_vocabulario, embeddings_vocabulario)

    # Retornando o score de similaridade
    similaridade_score = torch.sum(output).item()
    return similaridade_score


# Função para encontrar a palavra mais similar na Abordagem Embeddings com BERT/Autoatenção
def encontrar_palavra_mais_similar_abordagem_embeddings_bert_autoatencao(palavra_alvo, vocabulario):
    """
    Encontra a palavra mais similar no vocabulário usando a Abordagem Embeddings com BERT/Autoatenção.
    
    :param palavra_alvo: Palavra alvo
    :param vocabulario: Lista de palavras do vocabulário
    :return: Palavra mais similar
    """
    similaridades = [(palavra, calcular_similaridade_abordagem_embeddings_bert_autoatencao(palavra_alvo, palavra)) for palavra in vocabulario]
    similaridades.sort(key=lambda x: x[1], reverse=True)
    return similaridades[0][0]  # Retorna a palavra com maior similaridade
