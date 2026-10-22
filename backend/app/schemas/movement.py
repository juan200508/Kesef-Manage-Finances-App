from datetime import datetime
from uuid import UUID
from typing import Annotated
from decimal import Decimal
from app.models.movement import MovementType
from pydantic import BaseModel, ConfigDict, Field


class MovementBase(BaseModel):
    """Fields that are shared between create and read a movement"""
    movement_type: MovementType 
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    description: str | None = None
    category_id: UUID


class MovementCreate(MovementBase):
    """What comes in the body of the POST request to /movements"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "category_id": "b35650bb-0a02-4f37-ae85-61757dd1c6f1", "movement_type": "RETIRO", "amount": "500000.00",
                "description": "Bank account retirement"
            }]
        }
    )


class MovementUpdate(MovementBase):
    """ All the fields are optional: the client only sends what they want to change."""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "amount": "700000.00"
            }]
        }
    )
    category_id: UUID | None = None
    movement_type: MovementType | None = None
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)] | None = None
    description: str | None = None
    movement_date: datetime | None = None


class MovementOut(MovementBase):
    """What API returns"""
    id: UUID
    user_id: UUID
    movement_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
