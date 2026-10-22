import logging
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

from app.db.base import Base
from app.db.session import get_db
from app.api.routers import auth, categories, movements, monthly_incomes, balance
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "auth", "description": "User registration and login."},
    {"name": "categories", "description": "Expense categories, user specific categories or global categories."},
    {"name": "movements", "description": "User expenses and other money movements."},
    {"name": "monthly_incomes", "description": "Monthly incomes by sources."},
    {"name": "balance", "description": "Incomes - monthly expenses, with category breakdown."},
]

app = FastAPI(
    title="Finances API", 
    version="0.1.0",
    description="Personal finances API. For testing:  `POST /login`, copy the `access_token` and  press Authorize.",
    openapi_tags=tags_metadata
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Captura cualquier excepción de negocio (CategoryNotFoundError, etc.)
    que no haya sido interceptada explícitamente en el router correspondiente."""
    logger.warning(f"Business error on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Not control error in {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Server internal error"}
    )


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Endpoint simple para verificar que el servidor y la app responden."""
    result = db.execute(text("SELECT current_database()")).scalar()
    return {"status": "ok", "db": result}


# Ruta para register y login
app.include_router(auth.router)
# Ruta para categories
app.include_router(categories.router)
# Ruta para movements
app.include_router(movements.router)
# Ruta para monthly_incomes
app.include_router(monthly_incomes.router)
# Ruta para balances
app.include_router(balance.router)