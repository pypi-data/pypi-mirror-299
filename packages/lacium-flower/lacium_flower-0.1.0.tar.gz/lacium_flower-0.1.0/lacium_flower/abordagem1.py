import re

# Pesos para os 4 níveis de consciência fonológica na Abordagem Fonológica Clássica
PESOS = {
    "rima": 4,
    "silaba": 3,
    "intrassilabica": 2,
    "fonemica": 1
}

############## Abordagem Fonológica Clássica: Similaridade Fonológica ##############

def segmentar_silabas(palavra):
    """
    Função para segmentar uma palavra em sílabas. Utiliza uma abordagem regular para dividir as sílabas.
    
    :param palavra: Palavra a ser segmentada
    :return: Lista de sílabas
    """
    if isinstance(palavra, str):
        return re.findall(r'[bcdfghjklmnpqrstvwxyz]*[aeiouáéíóúãõâêîôûü]+[ns]?|[aeiouáéíóúãõâêîôûü]+[ns]?', palavra.lower())
    return []  # Retorna uma lista vazia se não for uma string válida

def similaridade_rima(palavra1, palavra2):
    """
    Função para calcular a similaridade de rima entre duas palavras.
    
    :param palavra1: Primeira palavra
    :param palavra2: Segunda palavra
    :return: Score de similaridade de rima (0 ou 1)
    """
    if isinstance(palavra1, str) and isinstance(palavra2, str):
        rima1 = palavra1[-2:]
        rima2 = palavra2[-2:]
        return 1 if rima1 == rima2 else 0
    return 0

def similaridade_silaba(palavra1, palavra2):
    """
    Função para calcular a similaridade silábica entre duas palavras.
    
    :param palavra1: Primeira palavra
    :param palavra2: Segunda palavra
    :return: Score de similaridade de sílabas
    """
    silabas1 = segmentar_silabas(palavra1)
    silabas2 = segmentar_silabas(palavra2)
    if silabas1 and silabas2 and isinstance(silabas1, list) and isinstance(silabas2, list):
        score = 1 if len(silabas1) == len(silabas2) else 0
        score += len(set(silabas1) & set(silabas2)) / max(len(silabas1), len(silabas2))
        return score
    return 0

def similaridade_intrassilabica(palavra1, palavra2):
    """
    Função para calcular a similaridade intrassilábica entre duas palavras.
    
    :param palavra1: Primeira palavra
    :param palavra2: Segunda palavra
    :return: Score de similaridade intrassilábica
    """
    def obter_unidades_intrassilabicas(silaba):
        unidades = {"ataque": "", "nucleo": "", "coda": ""}
        ataque_match = re.match(r'^[bcdfghjklmnpqrstvwxyz]*', silaba)
        nucleo_match = re.search(r'[aeiouáéíóúãõâêîôûü]+', silaba)
        coda_match = re.search(r'[bcdfghjklmnpqrstvwxyz]*$', silaba)

        if ataque_match:
            unidades["ataque"] = ataque_match.group()
        if nucleo_match:
            unidades["nucleo"] = nucleo_match.group()
        if coda_match:
            unidades["coda"] = coda_match.group()

        return unidades

    silabas1 = segmentar_silabas(palavra1)
    silabas2 = segmentar_silabas(palavra2)

    if silabas1 and silabas2 and isinstance(silabas1, list) and isinstance(silabas2, list):
        unidades1 = [obter_unidades_intrassilabicas(s) for s in silabas1]
        unidades2 = [obter_unidades_intrassilabicas(s) for s in silabas2]

        score = 0
        for u1, u2 in zip(unidades1, unidades2):
            if u1["ataque"] == u2["ataque"]:
                score += 1
            if u1["nucleo"] == u2["nucleo"]:
                score += 1
            if u1["coda"] == u2["coda"]:
                score += 1
        return score / (3 * max(len(silabas1), len(silabas2)))
    return 0

def similaridade_fonemica(palavra1, palavra2):
    """
    Função para calcular a similaridade fonêmica entre duas palavras.
    
    :param palavra1: Primeira palavra
    :param palavra2: Segunda palavra
    :return: Score de similaridade fonêmica
    """
    if isinstance(palavra1, str) and isinstance(palavra2, str):
        fonemas1 = list(palavra1)
        fonemas2 = list(palavra2)
        count_comum = len(set(fonemas1) & set(fonemas2))
        return count_comum / max(len(fonemas1), len(fonemas2))
    return 0

def calcular_similaridade_abordagem_fonologica(palavra_alvo, palavra):
    """
    Função para calcular a similaridade fonológica total entre duas palavras, utilizando
    os diferentes níveis de consciência fonológica (rima, sílaba, intrassilábica e fonêmica).
    
    :param palavra_alvo: Palavra alvo
    :param palavra: Palavra a ser comparada
    :return: Score total de similaridade
    """
    score_rima = similaridade_rima(palavra_alvo, palavra) * PESOS["rima"]
    score_silaba = similaridade_silaba(palavra_alvo, palavra) * PESOS["silaba"]
    score_intrassilabica = similaridade_intrassilabica(palavra_alvo, palavra) * PESOS["intrassilabica"]
    score_fonemica = similaridade_fonemica(palavra_alvo, palavra) * PESOS["fonemica"]
    score_total = score_rima + score_silaba + score_intrassilabica + score_fonemica
    return score_total

# Função para encontrar a palavra mais similar na abordagem fonológica clássica
def encontrar_palavra_mais_similar_abordagem_fonologica(palavra_alvo, vocabulario):
    """
    Encontra a palavra mais similar no vocabulário utilizando a Abordagem Fonológica Clássica.
    
    :param palavra_alvo: Palavra alvo
    :param vocabulario: Lista de palavras do vocabulário
    :return: Palavra mais similar
    """
    similaridades = [(palavra, calcular_similaridade_abordagem_fonologica(palavra_alvo, palavra)) for palavra in vocabulario]
    similaridades.sort(key=lambda x: x[1], reverse=True)
    return similaridades[0][0]  # Retorna a palavra com maior similaridade
