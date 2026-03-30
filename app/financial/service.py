from app.financial.models import (
    MonthlySummary,
    CategorySpending,
    ComparisonResult,
    IncomeCommitment
)
from app.financial.repository import FinancialRepository

class FinancialService:

    def __init__(self, repository: FinancialRepository):
        self.repository = repository

    def get_total_spent(self, year: int, month: int) -> MonthlySummary:
        """Total Gasto"""
        df = self.repository.get_transactions_by_month(year, month)

        expenses = df[df["type"] == "debit"]
        total = float(expenses["amount"].sum())

        return MonthlySummary(
            year=year,
            month=month,
            total_spent=total
        )
    
    def get_spending_by_category(self, year: int, month: int) -> CategorySpending:
        """Gasto por Categoria"""
        df = self.repository.get_transactions_by_month(year, month)

        expenses = df[df["type"] == "debit"]

        grouped = (
            expenses.groupby("category")["amount"]
            .sum()
            .to_dict()
        )

        return CategorySpending(
            year=year,
            month=month,
            spending={k: float(v) for k, v in grouped.items()}
        )
    
    def get_top_category(self, year: int, month: int) -> str:
        """Maior Categoria"""
        spending = self.get_spending_by_category(year, month).spending

        if not spending:
            return "Sem dados"
        
        return max(spending, key=spending.get)
    
    def compare_months(self, year:int, month: int) -> ComparisonResult:
        """Comparação entre meses"""
        current = self.get_total_spent(year, month).total_spent

        prev_month = month - 1
        prev_year = year

        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        
        previous = self.get_total_spent(prev_year, prev_month).total_spent

        return ComparisonResult(
            current=current,
            previous=previous,
            difference=current - previous
        )
    
    def get_income_commitment(self, year:int, month: int) -> IncomeCommitment:
        """% da Renda"""
        income = self.repository.get_user_income()
        total = self.get_total_spent(year, month).total_spent

        ratio = total / income if income else 0

        return IncomeCommitment(ratio=ratio)
    
    def get_financial_health(self, year: int, month: int) -> dict:
        """Exemplo de lógica mais 'inteligente'"""
        commitment = self.get_income_commitment(year, month).ratio

        if commitment < 0.5:
            status = "saudável"
        elif commitment < 0.8:
            status = "atenção"
        else:
            status = "crítico"
        
        return {
            "commitment": commitment,
            "status": status
        }
    
    def get_total_spent_last_n_months(self, year: int, month: int, n: int):
        total = 0.0

        current_year = year
        current_month = month

        for _ in range(n):
            summary = self.get_total_spent(current_year, current_month)
            total += summary.total_spent

            # volta um mês
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1

        return {
            "months": n,
            "total_spent": total
        }