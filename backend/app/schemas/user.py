from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Campos que se comparten entre crear y leer un usuario."""
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """Lo que llega en el body de POST /register."""
    password: str


class UserLogin(BaseModel):
    """Lo que llega en el body de POST /login."""
    email: EmailStr
    password: str


class UserOut(UserBase):
    """Lo que la API devuelve. Nunca incluye la contraseña."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    # Permite construir este schema directamente desde un objeto
    # SQLAlchemy (model_config en vez de orm_mode, que es la sintaxis vieja de Pydantic v1)
    model_config = ConfigDict(from_attributes=True)