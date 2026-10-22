from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Fields that are share between created and read an user"""
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """What comes in the body of the POST request to /register"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "full_name": "Test", "email": "test@test.com", "password": "test12345"
            }]
        }
    )
    password: str = Field(min_length=8, max_length=72, description="8 to 72 characters")

class UserLogin(BaseModel):
    """What comes in the body of the POST request to /login"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "email": "test@test.com", "password": "test12345"
            }]
        }
    )
    email: EmailStr
    password: str


class UserOut(UserBase):
    """What API returns. Never includes the password"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    # Permite construir este schema directamente desde un objeto
    # SQLAlchemy (model_config en vez de orm_mode, que es la sintaxis vieja de Pydantic v1)
    model_config = ConfigDict(from_attributes=True)