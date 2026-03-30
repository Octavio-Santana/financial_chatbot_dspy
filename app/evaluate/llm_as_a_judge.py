import dspy

class JuizFinanceiro(dspy.Signature):
    """
    Você é um especializado em respostas de assistentes financeiros.
    Avalie a resposta gerada com base nos critérios fornecidos.
    Seja criterioso e justo. Justifique sua nota antes de dá-la.
    """

    pergunta: str = dspy.InputField(desc="Pergunta original do usuário")
    resposta_gerada: str = dspy.InputField(desc="Resposta produzida pelo chatbot")
    resposta_esperada: str = dspy.InputField(desc="Resposta de referência (ground truth)")
    
    justificativa: str = dspy.OutputField(desc="Análise detalhada dos pontos fortes e fracos da resposta gerada")
    nota: float = dspy.OutputField(desc="Nota de 0.0 a 1.0. 1.0 = perfeito e 0.0 = completamente errado")


juiz = dspy.ChainOfThought(JuizFinanceiro)


def llm_judge(gold, pred, trace=None) -> float:
    """
    Usa um LLM para avaliar a qualidade da resposta.
    Combina o julgamento do LLM com uma verificação básica de formato.
    """

    try:
        avaliacao = juiz(
            pergunta = gold.question,
            resposta_gerada = pred.answer,
            resposta_esperada = gold.answer,
        )

        nota_llm = float(avaliacao.nota)

        # Guardrail: penalizar respostas sem valores númericos
        resposta = pred.answer.lower()
        tem_numero = "r$" in resposta or any(c.isdigit() for c in resposta)
        penalidade = 0.0 if tem_numero else 0.2

        return max(0.0, nota_llm - penalidade)
    
    except Exception as e:
        print(f"Erro no juiz LLM: {e}")
        return 0.0
