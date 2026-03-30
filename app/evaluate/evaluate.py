from dspy.evaluate import Evaluate

from app.config import setup_lm
from app.chatbot.service import FinancialChatbot
from app.evaluate.metricas import score_financeiro
from app.evaluate.llm_as_a_judge import llm_judge
from app.dataset.dataset import DEVSET
from optimize import load_optimized

# Configurar LM
setup_lm(
    model_name="ollama_chat/qwen2.5:3b",
    api_base="http://localhost:11434", 
    api_key=""
)

# Criar o avaliador
avaliar = Evaluate(
    devset=DEVSET,
    metric=score_financeiro,
    num_threads=4,      # paralelismo
    display_progress=True,
    display_table=5     # exibir as 5 primeiras linhas da tabela
)

# ChatBot
chatbot_base = FinancialChatbot()
chatbot_otimizado = load_optimized("chatbot_optimized.json")

# Executar
score_base = avaliar(chatbot_base).score
score_otimizado = avaliar(chatbot_otimizado).score

print("#"*25)
print(f"Score Base: {score_base}")
print(f"Score Otimizado: {score_otimizado}")
print(f"Ganho: {score_otimizado - score_base}")
print("#"*25)

avaliar_com_juiz = Evaluate(
    devset=DEVSET,
    metric=llm_judge,
    num_threads=2,
    display_progress=True
)

score_com_juiz = avaliar_com_juiz(chatbot_otimizado)
print(f"Score LLM-Judge: {score_com_juiz.score}")
print(score_com_juiz)