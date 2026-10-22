from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter, user_or_ip_key, READ_LIMIT, WRITE_LIMIT
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.monthly_income import MonthlyIncome
from app.schemas.monthly_income import MonthlyIncomeCreate, MonthlyIncomeUpdate, MonthlyIncomeOut
from app.core.responses import AUTH_RESPONSES


router = APIRouter(prefix="/monthly_incomes", tags=["monthly_incomes"], responses=AUTH_RESPONSES)


@router.post("", response_model=MonthlyIncomeOut, status_code=status.HTTP_201_CREATED, summary="Create a monthly income")
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def created_monthly_income(
    request: Request,
    monthly_income_in: MonthlyIncomeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Create a monthly income for an authenticated user """
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


@router.get("", response_model=list[MonthlyIncomeOut], summary="List the monthly incomes that belongs to a user",)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def list_monthly_incomes(
    request: Request,
    year: int | None = Query(default=None, description="Year to consult", examples=[2026]) ,
    month: list[int] | None = Query(default=None, description="Months 1-12. Repeatable: month=1&month=3"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ List all the monthly incomes that belongs to a user. In addition, manage filters for year and month."""
    
    query = db.query(MonthlyIncome).filter(
        MonthlyIncome.user_id == current_user.id
    )

    if year:
        query = query.filter(MonthlyIncome.year == year)
    if month:
        query = query.filter(MonthlyIncome.month.in_(month))

    return query.order_by(MonthlyIncome.created_at.desc()).all()


@router.get(
    "/{monthly_income_id}", 
    response_model=MonthlyIncomeOut, 
    summary="Get a specific monthly income",
    responses={
        404: {"description": "Monthly income not found"}
    }
)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def get_monthly_income(
    request: Request,
    monthly_income_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Get a monthly income by its ID """
    monthly_income = (
        db.query(MonthlyIncome).filter(
            MonthlyIncome.id == monthly_income_id,
            MonthlyIncome.user_id == current_user.id
        ).first()
    )

    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monthly income not found")

    return monthly_income


@router.put(
    "/{monthly_income_id}", 
    response_model=MonthlyIncomeOut, 
    summary="Update a monthly income",
    responses={
        404: {"description": "Monthly income not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def update_monthly_income(
    request: Request,
    monthly_income_id: UUID,
    monthly_income_in: MonthlyIncomeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Update a monthly income by its ID """
    monthly_income = (
            db.query(MonthlyIncome).filter(
                MonthlyIncome.id == monthly_income_id,
                MonthlyIncome.user_id == current_user.id
            ).first()
        )
    
    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monthly income not found")

    # Convierte los campos del schema en un diccionario, incluyendo los campos que el usuario no envío.
    # el excluse_unset solo actualiza los campos que el usuario especificó con los otros sin tocar los demás 
    update_data = monthly_income_in.model_dump(exclude_unset=True)

    # Actualiza de manera automática los campos que han sido especificados por el cliente 
    for field, value in update_data.items():
        setattr(monthly_income, field, value)

    db.commit()
    db.refresh(monthly_income)

    return monthly_income


@router.delete(
    "/{monthly_income_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Delete a monthly income",
    responses={
        404: {"description": "Monthly income not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def delete_monthly_income(
    request: Request,
    monthly_income_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Delete a monthly income by its ID """
    monthly_income = (
                db.query(MonthlyIncome).filter(
                    MonthlyIncome.id == monthly_income_id,
                    MonthlyIncome.user_id == current_user.id
                ).first()
            )
        
    if monthly_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monthly income not found")

    db.delete(monthly_income)
    db.commit()