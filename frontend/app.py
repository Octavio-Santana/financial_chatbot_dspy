"""
Frontend Streamlit — atualizado para DSPy.

Uso:
    streamlit run frontend/app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import setup_lm
from app.chatbot.service import FinancialChatbot

# ---------------------------------------------------------------------------
# Inicialização (roda uma vez por sessão Streamlit)
# ---------------------------------------------------------------------------
if "chatbot" not in st.session_state:
    with st.spinner("Carregando modelo..."):
        setup_lm(
            model_name="ollama_chat/qwen2.5:3b",
            api_base="http://localhost:11434", 
            api_key=""
        )
        st.session_state.chatbot = FinancialChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
st.title("💰 Assistente Financeiro")
st.caption("Powered by DSPy + Qwen2.5")

# Exemplos rápidos
with st.expander("💡 Exemplos de perguntas"):
    examples = [
        "Quanto gastei esse mês?",
        "Qual categoria eu mais gastei em fevereiro?",
        "Estou gastando mais do que mês passado?",
        "Qual percentual da minha renda estou comprometendo?",
        "Quanto gastei nos últimos 3 meses?",
    ]
    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state.pending_input = ex

# Histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input do usuário
user_input = st.chat_input("Pergunte sobre suas finanças...")

# Suporte a clique nos exemplos
if "pending_input" in st.session_state:
    user_input = st.session_state.pop("pending_input")

if user_input:
    # Exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Gera resposta
    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            result = st.session_state.chatbot(question=user_input)
            print(result)
            response = result.answer

        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
