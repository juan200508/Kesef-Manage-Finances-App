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
    month: list[int] | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if month:
        for m in month:
            if not (1 <= m <=12):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"El mes {m} no es válido, debe estar entre 1 y 12."
                )
            
        return [
            get_monthly_balance(db=db, user_id=current_user.id, month=m, year=year)
            for m in month
        ]

    return get_yearly_balance(db=db, user_id=current_user.id, year=year)