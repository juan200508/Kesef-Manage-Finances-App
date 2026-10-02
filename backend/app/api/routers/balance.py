from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.balance import MonthlyBalanceOut
from app.services.balance_service import get_monthly_balance, get_yearly_balance


router = APIRouter(prefix="/balance", tags=['balance'])


@router.get("", response_model=list[MonthlyBalanceOut])
def get_balance(
    year: int,
    month: int | None = Query(default=None, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if month is not None:
        balance = get_monthly_balance(db=db, user_id=current_user.id, month=month, year=year)
        return [balance]

    return get_yearly_balance(db=db, user_id=current_user.id, year=year)