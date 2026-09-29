from datetime import datetime
from uuid import UUID
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MonthlyIncomeBase(BaseModel):
    """Campos que se comparten entre crear y leer un ingreso."""
    year: int
    month: int
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    source: str


class MonthlyIncomeCreate(MonthlyIncomeBase):
    """Lo que llega en el body de POST /montly_income."""


class MonthlyIncomeOut(MonthlyIncomeBase):
    """Lo que la API devuelve."""
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
