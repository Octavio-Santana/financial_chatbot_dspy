import dspy
from dspy.teleprompt import BootstrapFewShot, MIPROv2

from app.config import setup_lm
from app.chatbot.service import FinancialChatbot
from app.dataset.dataset import TRAINSET


# ---------------------------------------------------------------------------
# Métrica de avaliação
# Aqui usamos uma métrica simples: a resposta contém números relevantes?
# Em produção, use um LLM-judge ou métricas específicas do domínio.
# ---------------------------------------------------------------------------
def financial_metric(gold: dspy.Example, pred: dspy.Prediction, trace=None) -> float:
    """
    Métrica simples: verifica se a resposta gerada menciona pelo menos
    um valor numérico (R$ ou %).
    """
    answer = pred.answer.lower()
    has_value = "r$" in answer or "%" in answer or any(c.isdigit() for c in answer)
    not_empty = len(answer.strip()) > 10
    acc = gold.answer.lower() == answer
    return float(has_value and not_empty and acc)


# ---------------------------------------------------------------------------
# Otimização com BootstrapFewShot (mais rápido, boa para começo)
# ---------------------------------------------------------------------------
def optimize_bootstrap():
    print("🔧 Iniciando otimização com BootstrapFewShot...")

    optimizer = BootstrapFewShot(
        metric=financial_metric,
        max_bootstrapped_demos=3,
        max_labeled_demos=2,
    )

    chatbot = FinancialChatbot()
    compiled = optimizer.compile(chatbot, trainset=TRAINSET)
    compiled.save("chatbot_optimized.json")

    print("✅ Otimização concluída! Salvo em chatbot_optimized.json")
    return compiled


# ---------------------------------------------------------------------------
# Otimização com MIPROv2 (mais poderosa, requer mais exemplos e tempo)
# ---------------------------------------------------------------------------
def optimize_mipro():
    print("🔧 Iniciando otimização com MIPROv2...")

    optimizer = MIPROv2(
        metric=financial_metric,
        auto="light",  # "light" | "medium" | "heavy"
    )

    chatbot = FinancialChatbot()
    compiled = optimizer.compile(
        chatbot,
        trainset=TRAINSET,
        num_trials=10,
    )
    compiled.save("chatbot_optimized_mipro.json")

    print("✅ Otimização MIPROv2 concluída! Salvo em chatbot_optimized_mipro.json")
    return compiled


# ---------------------------------------------------------------------------
# Carregar modelo já otimizado
# ---------------------------------------------------------------------------
def load_optimized(path: str = "chatbot_optimized.json") -> FinancialChatbot:
    chatbot = FinancialChatbot()
    chatbot.load(path)
    print(f"✅ Chatbot otimizado carregado de {path}")
    return chatbot


if __name__ == "__main__":
    setup_lm(
        model_name="ollama_chat/qwen2.5:3b",
        api_base="http://localhost:11434", 
        api_key=""
    )
    optimize_bootstrap()
