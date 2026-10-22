from datetime import datetime
from uuid import UUID
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.monthly_income import MonthlyIncomeSource


class MonthlyIncomeBase(BaseModel):
    """ Fields that are shared between create and read an income """
    year: int = Field(ge=2000, le=2100, description="Year of the income, 4 digits format")
    month: int = Field(ge=1, le=12, description="Month of the income (1=January, 12=December)")
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    source: MonthlyIncomeSource
    description: str | None = None


class MonthlyIncomeCreate(MonthlyIncomeBase):
    """ What comes in the body of the POST request to /monthly_income """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "year": 2026, "month": 12, "amount": "4500000.00", "source": "SALARIO", "description": "December payment"
            }]
        }
    )


class MonthlyIncomeUpdate(BaseModel):
    """ All the fields are optional: the client only sends what they want to change."""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "month": 11, "source": "SALARIO", "description": "November payment"
            }]
        }
    )
    year: int | None = Field(default=None, ge=2000, le=2100)
    month: int | None = Field(default=None, ge=1, le=12)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    source: MonthlyIncomeSource | None = None
    description: str | None = Field(default=None, min_length=1, max_length=255)


class MonthlyIncomeOut(MonthlyIncomeBase):
    """What API returns"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
