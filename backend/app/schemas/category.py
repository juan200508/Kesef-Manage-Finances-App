from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Campos que se comparten entre crear y leer una categoría."""
    name: str


class CategoryCreate(CategoryBase):
    """Lo que llega en el body de POST /categories."""
    pass


class CategoryOut(CategoryBase):
    """Lo que la API devuelve."""
    id: UUID
    user_id: UUID | None
    is_global: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)