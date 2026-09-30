from datetime import datetime
from uuid import UUID
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.monthly_income import MonthlyIncomeSource

class MonthlyIncomeBase(BaseModel):
    """Campos que se comparten entre crear y leer un ingreso."""
    year: int = Field(ge=2000, le=2100, description="Año del ingreso, formato de 4 dígitos")
    month: int = Field(ge=1, le=12, description="Mes del ingreso (1=enero, 12=diciembre)")
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    source: MonthlyIncomeSource
    description: str | None = None


class MonthlyIncomeCreate(MonthlyIncomeBase):
    """Lo que llega en el body de POST /montly_income."""


class MonthlyIncomeUpdate(BaseModel):
    """Todos los campos opcionales: el cliente solo manda lo que quiere cambiar."""
    year: int | None = Field(default=None, ge=2000, le=2100)
    month: int | None = Field(default=None, ge=1, le=12)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    source: MonthlyIncomeSource | None = None
    description: str | None = Field(default=None, min_length=1, max_length=255)


class MonthlyIncomeOut(MonthlyIncomeBase):
    """Lo que la API devuelve."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
