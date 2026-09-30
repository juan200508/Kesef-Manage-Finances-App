from sqlalchemy import Column, DateTime, ForeignKey, String, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Category(Base):
    """Mapea la tabla `categories` definida en sql/schema.sql."""

    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    name = Column(String(255), nullable=False)
    is_global = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Lado "muchos" de la relación: cada categoría pertenece a un usuario
    owner = relationship("User", back_populates="categories")
    # Lado "uno" de la relación: una categoría tienem muchos movimientos
    movements = relationship("Movement", back_populates="category")