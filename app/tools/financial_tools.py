"""
Ferramentas financeiras para o agente DSPy.

Cada função é uma tool disponível para o dspy.ReAct.
Requisitos DSPy:
  - Tipagem completa nos parâmetros e retorno
  - Docstring clara (usada pelo DSPy para descrever a tool ao modelo)
  - Retorno serializável (dict, str, int, float)
"""

from app.financial.service import FinancialService
from app.financial.repository import FinancialRepository

# Instância compartilhada (singleton simples)
_repo = FinancialRepository("data/transactions.csv", "data/user.json")
_service = FinancialService(_repo)


def get_total_spent(year: int, month: int) -> dict:
    """
    Retorna o total gasto (débitos) em um mês específico.

    Args:
        year: Ano (ex: 2026)
        month: Mês como número (1=Janeiro ... 12=Dezembro)

    Returns:
        dict com year, month e total_spent em reais (float)
    """
    result = _service.get_total_spent(year, month)
    return result.model_dump()


def get_spending_by_category(year: int, month: int) -> dict:
    """
    Retorna os gastos agrupados por categoria em um mês.

    Args:
        year: Ano (ex: 2026)
        month: Mês como número (1=Janeiro ... 12=Dezembro)

    Returns:
        dict com year, month e spending: {categoria: valor_float}
    """
    result = _service.get_spending_by_category(year, month)
    return result.model_dump()


def compare_months(year: int, month: int) -> dict:
    """
    Compara o total gasto no mês informado com o mês anterior.

    Args:
        year: Ano do mês atual (ex: 2026)
        month: Mês atual como número (1=Janeiro ... 12=Dezembro)

    Returns:
        dict com current (mês atual), previous (mês anterior) e difference
    """
    result = _service.compare_months(year, month)
    return result.model_dump()


def get_top_category(year: int, month: int) -> dict:
    """
    Retorna a categoria com o maior volume de gastos em um mês.

    Args:
        year: Ano (ex: 2026)
        month: Mês como número (1=Janeiro ... 12=Dezembro)

    Returns:
        dict com top_category: nome da categoria
    """
    return {"top_category": _service.get_top_category(year, month)}


def get_income_commitment(year: int, month: int) -> dict:
    """
    Calcula o percentual da renda mensal comprometida com gastos.

    Args:
        year: Ano (ex: 2026)
        month: Mês como número (1=Janeiro ... 12=Dezembro)

    Returns:
        dict com ratio (float entre 0 e 1, ex: 0.47 = 47% da renda)
    """
    result = _service.get_income_commitment(year, month)
    return result.model_dump()


def get_total_spent_last_n_months(year: int, month: int, n: int) -> dict:
    """
    Soma o total gasto nos últimos N meses a partir do mês informado (inclusive).

    Args:
        year: Ano do mês de referência (ex: 2026)
        month: Mês de referência como número (1=Janeiro ... 12=Dezembro)
        n: Quantidade de meses para somar (ex: 3 = últimos 3 meses)

    Returns:
        dict com months (int) e total_spent (float)
    """
    return _service.get_total_spent_last_n_months(year, month, n)


# Lista de todas as tools disponíveis para o agente
ALL_TOOLS = [
    get_total_spent,
    get_spending_by_category,
    compare_months,
    get_top_category,
    get_income_commitment,
    get_total_spent_last_n_months,
]
