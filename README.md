# 💰 Financial Chatbot — DSPy

Assistente financeiro pessoal com IA, construído com **DSPy**, **FastAPI** e **Streamlit**. O chatbot responde perguntas em linguagem natural sobre gastos, categorias e saúde financeira — sem prompts manuais, sem parser de regex, sem grafos de orquestração.

> Este projeto é uma reescrita de uma versão anterior baseada em LangGraph + prompt engineering manual. O objetivo é demonstrar como o DSPy simplifica e melhora a qualidade de sistemas baseados em LLM.

---

## ✨ Funcionalidades

- **Linguagem natural** — faça perguntas como *"Quanto gastei esse mês?"* ou *"Qual categoria consomiu mais em fevereiro?"*
- **Raciocínio com ferramentas** — o agente decide automaticamente quais funções chamar (padrão ReAct: Thought → Action → Observation → Answer)
- **Troca de modelo com uma linha** — compatível com Ollama (local), OpenAI, Anthropic e HuggingFace
- **Otimização automática de prompts** — use `BootstrapFewShot` ou `MIPROv2` para melhorar as respostas sem engenharia manual
- **Pipeline de avaliação** — métricas compostas + LLM-as-a-Judge para medir qualidade das respostas

---

## 🏗️ Arquitetura

```
Frontend (Streamlit)
        │
        ▼
API Layer (FastAPI)
        │
        ▼
FinancialChatbot (dspy.Module)
        │
        └── dspy.ReAct ──► Thought → Action → Observation → Answer
                │
                ▼
        Tool Layer  (funções Python tipadas)
                │
                ▼
        FinancialService  (regras de negócio)
                │
                ▼
        Repository  (CSV / JSON)
```

O **DSPy** substitui integralmente a camada de orquestração do LLM. A camada de negócio (`financial/`) não foi alterada.

---

## 📁 Estrutura do projeto

```
financial-chatbot-dspy/
│
├── app/
│   ├── main.py                   # API FastAPI (lifespan, endpoints /chat e /health)
│   ├── config.py                 # Configuração do LM (setup_lm)
│   │
│   ├── chatbot/
│   │   ├── signatures.py         # FinancialQuestion — Signature DSPy (substitui prompt.py)
│   │   └── service.py            # FinancialChatbot + chat() (substitui service.py + graph.py)
│   │
│   ├── financial/
│   │   ├── models.py             # Modelos Pydantic (Transaction, MonthlySummary, etc.)
│   │   ├── repository.py         # Leitura de CSV e JSON
│   │   └── service.py            # Lógica de negócio (totais, comparações, categorias)
│   │
│   ├── tools/
│   │   └── financial_tools.py    # Funções tipadas expostas ao agente dspy.ReAct
│   │
│   ├── dataset/
│   │   └── dataset.py            # TRAINSET e DEVSET para otimização e avaliação
│   │
│   └── evaluate/
│       ├── metricas.py           # Métricas compostas (score_financeiro)
│       ├── avaliacao.py          # Avaliação comparativa (base vs. otimizado)
│       └── llm_as_a_judge.py     # Avaliação com LLM (JuizFinanceiro)
│
├── frontend/
│   └── app.py                    # Interface Streamlit
│
├── data/
│   ├── transactions.csv          # Dados de transações
│   └── user.json                 # Perfil do usuário (renda mensal)
│
├── optimize.py                   # Otimização com BootstrapFewShot / MIPROv2
└── pyproject.toml
```

---

## ⚙️ Pré-requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) **ou** pip
- Para modelos locais: [Ollama](https://ollama.com) instalado e rodando

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/financial-chatbot-dspy.git
cd financial-chatbot-dspy
```

### 2. Instale as dependências

Com `uv` (recomendado):
```bash
uv sync
```

Com `pip`:
```bash
pip install -e .
```

### 3. Configure o modelo

O projeto vem pré-configurado para usar o **Ollama** com o modelo `qwen2.5:3b`. Para baixar o modelo:

```bash
ollama pull qwen2.5:3b
```

Para usar outro provedor, veja a seção [Troca de modelo](#-troca-de-modelo).

---

## ▶️ Executando

### API (FastAPI)

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em `http://localhost:8000/docs`.

Exemplo de requisição:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Quanto gastei esse mês?"}'
```

Resposta esperada:

```json
{
  "response": "Em março de 2026 você gastou R$ 3.640,00."
}
```

### Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Acesse `http://localhost:8501` no navegador.

---

## 🔄 Troca de modelo

Edite a chamada `setup_lm(...)` em `app/main.py` (para a API) ou em `frontend/app.py` (para o frontend):

```python
from app.config import setup_lm

# Ollama local (padrão)
setup_lm("ollama_chat/qwen2.5:3b", api_base="http://localhost:11434", api_key="")

# OpenAI
setup_lm("openai/gpt-4o-mini", api_key="sk-...")

# Anthropic
setup_lm("anthropic/claude-3-haiku-20240307", api_key="sk-ant-...")
```

A troca do modelo **não requer nenhuma outra alteração** no código.

---

## 🧪 Otimização de prompts

O DSPy permite compilar o chatbot com exemplos de treinamento, gerando few-shots automaticamente que melhoram a qualidade das respostas.

### BootstrapFewShot (rápido, indicado para começar)

```bash
python optimize.py
```

O modelo otimizado é salvo em `chatbot_optimized.json`. Para carregá-lo na API:

```python
from optimize import load_optimized
chatbot = load_optimized("chatbot_optimized.json")
```

### MIPROv2 (mais poderoso, requer mais tempo e exemplos)

Descomente a chamada `optimize_mipro()` em `optimize.py` e execute novamente.

---

## 📊 Avaliação

Compare a qualidade do chatbot base com o otimizado:

```bash
python app/evaluate/evaluate.py
```

A saída mostra três métricas:
- **score_financeiro** — métrica composta (valores monetários + completude + exatidão numérica)
- **Score Base** — desempenho sem otimização
- **Score Otimizado** — desempenho após `BootstrapFewShot`
- **Score LLM-Judge** — avaliação qualitativa feita por um segundo LLM (`JuizFinanceiro`)

---

## 🔧 Ferramentas disponíveis para o agente

| Função | Descrição |
|---|---|
| `get_total_spent(year, month)` | Total gasto (débitos) em um mês |
| `get_spending_by_category(year, month)` | Gastos agrupados por categoria |
| `compare_months(year, month)` | Comparação com o mês anterior |
| `get_top_category(year, month)` | Categoria com maior volume de gastos |
| `get_income_commitment(year, month)` | Percentual da renda comprometida |
| `get_total_spent_last_n_months(year, month, n)` | Total dos últimos N meses |

---

## 🤔 Por que DSPy?

| Problema (antes) | Solução (DSPy) |
|---|---|
| Parser regex frágil para extrair chamadas de ferramentas | `dspy.ReAct` gerencia tool use nativamente |
| Loop detection manual no grafo LangGraph | Controlado por `max_iters` no `ReAct` |
| Prompt como f-string de 60 linhas | `Signature` declarativa de ~15 linhas |
| Troca de modelo exigia refatoração | Uma linha: `setup_lm("provider/model")` |
| Sem otimização sistemática de prompts | `BootstrapFewShot` e `MIPROv2` nativos |

**Resultado:** ~200 linhas de orquestração removidas, comportamento equivalente ou superior.

---

## 📦 Dependências principais

| Pacote | Versão mínima | Uso |
|---|---|---|
| `dspy` | 2.6.0 | Orquestração do LLM, agente ReAct, otimização |
| `fastapi` | 0.115.0 | API REST |
| `uvicorn` | 0.30.0 | Servidor ASGI |
| `streamlit` | 1.35.0 | Interface web |
| `pandas` | 2.2.0 | Leitura e processamento de CSV |
| `pydantic` | 2.7.0 | Modelos de dados e validação |

---

## 📄 Licença

MIT