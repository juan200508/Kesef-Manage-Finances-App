from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class User(Base):
    """Mapea la tabla `users` definida en sql/schema.sql."""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Lado "uno" de la relación: un usuario tiene muchas categorías
    categories = relationship("Category", back_populates="owner")
    # Lado "uno" de la relación: un usuario tiene muchos movimientos
    movements = relationship("Movement", back_populates="owner")
    # Lado "uno" de la relación: un usuario tiene varios ingresos
    monthly_incomes = relationship("MonthlyIncome", back_populates="owner")