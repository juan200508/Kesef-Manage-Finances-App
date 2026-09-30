import enum
from sqlalchemy import Column, DateTime, ForeignKey, String, text, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class MovementType(str, enum.Enum):
    COMPRA = "COMPRA"
    TRANSFERENCIA = "TRANSFERENCIA"
    RETIRO = "RETIRO"
    PAGO = "PAGO"
    OTRO = "OTRO" 


class Movement(Base):
    """Mapea la tabla `movements` definida en sql/schema.sql."""

    __tablename__ = "movements"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
        index=True
    )
    movement_type = Column(Enum(MovementType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    movement_date = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Lado "muchos" de la relación: cada movimiento pertenece a un usuario
    owner = relationship("User", back_populates="movements")
    # Lado "muchos" de la relación: cada movimiento pertenece a una categoria
    category = relationship("Category", back_populates="movements")


