from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# El engine mantiene el pool de conexiones a PostgreSQL
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True, # Verifica la conexión con un ping antes de usuarla
    pool_recycle=300   # Recicla conexciones cada 5 minutos, antes que Neon las cierre
)

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
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()