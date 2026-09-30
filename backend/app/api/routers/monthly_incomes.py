from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.monthly_income import MonthlyIncome, MonthlyIncomeSource
from app.schemas.monthly_income import MonthlyIncomeCreate, MonthlyIncomeUpdate, MonthlyIncomeOut


router = APIRouter(prefix="/monthly_incomes", tags=["monthly_incomes"])


@router.post("", response_model=MonthlyIncomeOut, status_code=status.HTTP_201_CREATED)
def created_monthly_income(
    monthly_income_in: MonthlyIncomeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Crea un ingreso mensual de un usuario autenticado

    new_monthly_income = MonthlyIncome(
        user_id = current_user.id,
        year = monthly_income_in.year,
        month = monthly_income_in.month,
        amount = monthly_income_in.amount,
        source = monthly_income_in.source,
        description = monthly_income_in.description
    )

    db.add(new_monthly_income)
    db.commit()
    db.refresh(new_monthly_income)

    return new_monthly_income



@router.get("", response_model=list[MonthlyIncomeOut])
def list_monthly_incomes(
    year: int | None = None,
    month: list[int] | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Lista los ingresos mensuales del usuario autenticado
    # adicionalmente maneja filtros de año y mes si el usuario lo necesita

    query = db.query(MonthlyIncome).filter(
        MonthlyIncome.user_id == current_user.id
    )

    if year:
        query = query.filter(MonthlyIncome.year == year)
    if month:
        query = query.filter(MonthlyIncome.month.in_(month))

    return query.order_by(MonthlyIncome.created_at.desc()).all()


@router.get("/{monthly_income_id}", response_model=MonthlyIncomeOut)
def get_monthly_income(
    monthly_income_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Obtiene un ingreso mensual por su ID
    monthly_income = (
        db.query(MonthlyIncome).filter(
            MonthlyIncome.id == monthly_income_id,
            MonthlyIncome.user_id == current_user.id
        ).first()
    )

    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso mensual no encontrado")

    return monthly_income


@router.put("/{monthly_income_id}", response_model=MonthlyIncomeOut)
def update_monthly_income(
    monthly_income_id: UUID,
    monthly_income_in: MonthlyIncomeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Actualiza un ingreso mensual por su ID
    monthly_income = (
            db.query(MonthlyIncome).filter(
                MonthlyIncome.id == monthly_income_id,
                MonthlyIncome.user_id == current_user.id
            ).first()
        )
    
    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso mensual no encontrado")

    # Convierte los campos del schema en un diccionario, incluyendo los campos que el usuario no envío.
    # el excluse_unset solo actualiza los campos que el usuario especificó con los otros sin tocar los demás 
    update_data = monthly_income_in.model_dump(exclude_unset=True)

    # Actualiza de manera automática los campos que han sido especificados por el cliente 
    for field, value in update_data.items():
        setattr(monthly_income, field, value)

    db.commit()
    db.refresh(monthly_income)

    return monthly_income


@router.delete("/{monthly_income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_monthly_income(
    monthly_income_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Elimina un ingreso mensual
    monthly_income = (
                db.query(MonthlyIncome).filter(
                    MonthlyIncome.id == monthly_income_id,
                    MonthlyIncome.user_id == current_user.id
                ).first()
            )
        
    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingreso mensual no encontrado")

    db.delete(monthly_income)
    db.commit()