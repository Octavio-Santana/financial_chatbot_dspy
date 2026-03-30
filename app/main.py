from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from app.config import setup_lm
from app.chatbot.service import chat, FinancialChatbot


# ---------------------------------------------------------------------------
# Startup: configura o LM uma única vez ao subir o servidor
# ---------------------------------------------------------------------------
chatbot_instance: FinancialChatbot | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chatbot_instance
    # Troque aqui para setup_lm("openai/gpt-4o-mini") se quiser usar API
    setup_lm(
        model_name="ollama_chat/qwen2.5:3b",
        api_base="http://localhost:11434", 
        api_key=""
    )
    chatbot_instance = FinancialChatbot()
    print("✅ Chatbot inicializado")
    yield
    print("🛑 Servidor encerrado")


app = FastAPI(
    title="Financial Chatbot (DSPy)",
    description="Chatbot financeiro reescrito com DSPy",
    version="2.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    user_input: str


class ChatResponse(BaseModel):
    response: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    response = chat(req.user_input, chatbot=chatbot_instance)
    return ChatResponse(response=response)


@app.get("/health")
def health():
    return {"status": "ok"}
