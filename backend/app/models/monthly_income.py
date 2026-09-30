import enum
from sqlalchemy import Column, DateTime, ForeignKey, String, text, Integer, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class MonthlyIncomeSource(str, enum.Enum):
    SALARIO = "SALARIO"
    FREELANCE = "FREELANCE"
    CONSIGNACIONES = "CONSIGNACIONES"
    OTROS = "OTROS"

class MonthlyIncome(Base):
    """Mapea la tabla `monthly_incomes` definida en sql/schema.sql."""
    
    __tablename__ = "monthly_incomes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    source = Column(Enum(MonthlyIncomeSource), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Lado "muchos" de la relación: cada ingreso pertenece a un usuario
    owner = relationship("User", back_populates="monthly_incomes")