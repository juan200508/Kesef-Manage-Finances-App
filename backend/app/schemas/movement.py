from datetime import datetime
from uuid import UUID
from typing import Annotated
from decimal import Decimal
from app.models.movement import MovementType
from pydantic import BaseModel, ConfigDict, Field


class MovementBase(BaseModel):
    """Campos que se comparten entre crear y leer un movimiento."""
    movement_type: MovementType 
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    description: str | None = None
    category_id: UUID

class MovementCreate(MovementBase):
    """Lo que llega en el body de POST /movements."""


class MovementUpdate(MovementBase):
    """Los campos que el cliente requiera actualizar"""
    category_id: UUID | None = None
    movement_type: MovementType | None = None
    amount: Decimal | None = None
    description: str | None = None
    movement_date: datetime | None = None
    
class MovementOut(MovementBase):
    """Lo que la API devuelve."""
    id: UUID
    user_id: UUID
    movement_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
