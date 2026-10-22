from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CategoryExpenseBreakdown(BaseModel):
    """ Breakdown of the total expenses in a month by categories """
    category_id: UUID
    category_name: str
    total: Decimal


class MonthlyBalanceOut(BaseModel):
    """Calculated balance of a month"""
    year: int
    month: int
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    expenses_by_category: list[CategoryExpenseBreakdown]