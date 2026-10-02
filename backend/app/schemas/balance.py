from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CategoryExpenseBreakdown(BaseModel):
    "Desglose de los gastos totales en un mes por categorías"
    category_id: UUID
    category_name: str
    total: Decimal


class MonthlyBalanceOut(BaseModel):
    "Balance calculado de un mes"
    year: int
    month: int
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    expenses_by_category: list[CategoryExpenseBreakdown]