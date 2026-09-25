import logging
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import get_db
from app.api.routers import auth

logger = logging.getLogger(__name__)

app = FastAPI(title="Finanzas API", version="0.1.0")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no controlado en {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Endpoint simple para verificar que el servidor y la app responden."""
    result = db.execute(text("SELECT current_database()")).scalar()
    return {"status": "ok", "db": result}


# Ruta para register y login
app.include_router(auth.router)