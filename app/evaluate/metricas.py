import dspy
import re

def conten_valor_monetario(gold, pred, trace=None) -> bool:
    """
    Métrica booleana: a resposta menciona algum valor em R$?
    Útil para garantir que o modelo não respondeu de foma vaga.
    """

    resposta = pred.answer.lower()
    return "r$" in resposta or any(c.isdigit() for c in resposta)


def resposta_correta(gold, pred, trace=None) -> bool:
    """
    Verifica se o valor esperado na resposta gerada.
    gold.answer contém a resposta de referência do dataset
    """
    esperado = gold.answer.lower()
    gerado = pred.answer.lower()

    # Extrai número da esposta esperada e verifica cada um.
    numeros = re.findall(r"[d.,]+", esperado)
    return all(numero in gerado for numero in numeros)


def score_financeiro(gold, pred, trace=None) -> float:
    """
    Score composto que combina três critérios com pesos diferentes.
    Retorna um float entre 0.0 e 1.0
    """
    resposta = pred.answer.lower()
    pontos = 0.0

    # Critério 1: Contém valor monetário (peso 0.5)
    if "r$" in resposta or any(c.isdigit() for c in resposta):
        pontos += 0.5
    
    # Critério 2: Resposta não é vaga demais (> 20 chars) (peso 0.3)
    if len(resposta.strip()) > 20:
        pontos += 0.3
    
    # Critério 3: Número esperado está presente (peso 0.2)
    numeros_gold = re.findall(r"[d.,]+", gold.answer)
    if numeros_gold and numeros_gold[0] in resposta:
        pontos += 0.2
    
    return pontos



