from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db

app = FastAPI(title="Finanzas API", version="0.1.0")


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Endpoint simple para verificar que el servidor y la app responden."""
    result = db.execute(text("SELECT current_database()")).scalar()
    return {"status": "ok", "db": result}