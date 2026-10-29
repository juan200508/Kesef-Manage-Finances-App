from datetime import datetime
from uuid import UUID
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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

    # Validación de que la contraseña contenga al menos un número y un caracter especial
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[^A-Za-z0-9\s]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

class UserLogin(BaseModel):
    """What comes in the body of the POST request to /login"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "email": "test@test.com", "password": "Test12345*"
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