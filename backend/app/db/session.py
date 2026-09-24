from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# El engine mantiene el pool de conexiones a PostgreSQL
engine = create_engine(settings.database_url)

# SessionLocal es una "fábrica" de sesiones: cada request abre una
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependencia de FastAPI: abre una sesión, la entrega al endpoint,
    y la cierra automáticamente al terminar (haya error o no).
    La vas a usar así en los endpoints: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()