from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter, user_or_ip_key, READ_LIMIT
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.balance import MonthlyBalanceOut
from app.services.balance_service import get_monthly_balance, get_yearly_balance
from app.core.responses import AUTH_RESPONSES


router = APIRouter(prefix="/balance", tags=['balance'], responses=AUTH_RESPONSES)


@router.get(
    "", 
    response_model=list[MonthlyBalanceOut], 
    summary="Monthly or yearly balance",
    responses={
        422: {"description": "Month out of range"}
    }
)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def get_balance(
    request: Request,
    year: int = Query(description="Year to consult", examples=[2026]),
    month: list[int] | None = Query(default=None, description="Months 1-12. Repite: month=1&month=3. Without it, returns only the months of the year with data."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Get the movements and incomes and build a monthly or yearly balance. """
    if month:
        for m in month:
            if not (1 <= m <=12):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Month {m} is not valid, has to be between 1 and 12."
                )
            
        return [
            get_monthly_balance(db=db, user_id=current_user.id, month=m, year=year)
            for m in month
        ]

    return get_yearly_balance(db=db, user_id=current_user.id, year=year)