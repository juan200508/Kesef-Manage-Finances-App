from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """ Fields that are shared between create and read a category """
    name: str


class CategoryCreate(CategoryBase):
    """ All that is include in the body of the POST request to /categories """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "name": "Vehículo"
            }]
        }
    )


class CategoryOut(CategoryBase):
    """ What API returns """
    id: UUID
    user_id: UUID | None
    is_global: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)