import dspy


class FinancialQuestion(dspy.Signature):
    """
    Você é um assistente financeiro pessoal.
    Use as ferramentas disponíveis para responder perguntas sobre gastos,
    categorias, comparações e saúde financeira.

    REGRAS:
    - Nunca invente valores numéricos — sempre consulte uma ferramenta
    - Interprete expressões temporais como "esse mês", "mês passado",
      "este ano" usando a data atual fornecida
    - Responda em português, de forma clara e direta
    - Formate valores monetários como R$ X.XXX,XX
    - Se não houver dados para o período, informe isso ao usuário
    - Use apenas as ferramentas necessárias para responder diretamente à pergunta
    - Evite chamadas desnecessárias de ferramentas
    - Pare assim que tiver informação suficiente para responder
    """

    question: str = dspy.InputField(
        desc="Pergunta do usuário sobre suas finanças pessoais"
    )
    current_date: str = dspy.InputField(
        desc="Data atual no formato DD/MM/YYYY — use para interpretar 'hoje', 'esse mês', etc."
    )
    answer: str = dspy.OutputField(
        desc="Resposta clara, direta e em português ao usuário, com valores formatados"
    )
