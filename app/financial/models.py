from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class Transaction(BaseModel):
    id: int
    date: datetime
    amount: float
    category: str
    description: str
    type: str # credit /debit


class MonthlySummary(BaseModel):
    year: int
    month: int
    total_spent: float


class CategorySpending(BaseModel):
    year: int
    month: int
    spending: Dict[str, float]


class ComparisonResult(BaseModel):
    current: float
    previous: float
    difference: float


class IncomeCommitment(BaseModel):
    ratio: float
