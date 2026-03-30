from datetime import datetime
import dspy

from app.chatbot.signatures import FinancialQuestion
from app.tools.financial_tools import ALL_TOOLS


class FinancialChatbot(dspy.Module):
    """
    Agente financeiro baseado em dspy.ReAct.

    dspy.ReAct implementa o padrão Reasoning + Acting:
      Thought → Action (tool call) → Observation → ... → Answer

    max_iters=4 permite até 4 ciclos de tool use por pergunta,
    suficiente para perguntas que precisam de mais de uma ferramenta.
    """

    def __init__(self, max_iters: int = 4):
        super().__init__()
        self.agent = dspy.ReAct(
            signature=FinancialQuestion,
            tools=ALL_TOOLS,
            max_iters=max_iters,
        )

    def forward(self, question: str, current_date: str = None) -> dspy.Prediction:
        current_date = datetime.now().strftime("%d/%m/%Y")
        return self.agent(question=question, current_date=current_date)


def chat(user_input: str, chatbot: FinancialChatbot | None = None) -> str:
    """
    Função de conveniência para uso na API e no frontend.

    Args:
        user_input: Pergunta do usuário
        chatbot: Instância do chatbot (usa singleton global se None)

    Returns:
        Resposta em texto
    """
    if chatbot is None:
        chatbot = _get_default_chatbot()

    result = chatbot(question=user_input)
    print(result)
    return result.answer


# ---------------------------------------------------------------------------
# Singleton global — evita recarregar o modelo a cada request
# ---------------------------------------------------------------------------
_default_chatbot: FinancialChatbot | None = None


def _get_default_chatbot() -> FinancialChatbot:
    global _default_chatbot
    if _default_chatbot is None:
        _default_chatbot = FinancialChatbot()
    return _default_chatbot
