import dspy


def setup_lm(model_name: str | None = None, **kwargs):
    """
    Configura o LM global do DSPy.

    Exemplos de uso:

    # Modelo local via HuggingFace (mesmo modelo do projeto original)
    setup_lm("Qwen/Qwen2.5-3B-Instruct")

    # OpenAI
    setup_lm("openai/gpt-4o-mini", api_key="sk-...")

    # Anthropic
    setup_lm("anthropic/claude-3-haiku-20240307", api_key="sk-ant-...")

    # Ollama local
    setup_lm("ollama/qwen2.5:3b")
    """
    if model_name is None:
        model_name = "ollama_chat/qwen2.5:3b"

    lm = dspy.LM(model=model_name, max_tokens=512, **kwargs)
    dspy.configure(lm=lm)
    return lm

