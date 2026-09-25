from app.db.session import SessionLocal
from app.models.category import Category
from app.db.base import Base  # noqa: F401 - fuerza a registrar todos los modelos antes de usarlos

GLOBAL_CATEGORIES = [
    "Alimentación",
    "Transporte",
    "Vivienda",
    "Entretenimiento",
    "Salud",
    "Educación",
    "Otros"
]

def seed_categories():
    db = SessionLocal()
    try:
        for name in GLOBAL_CATEGORIES:
            exists = db.query(Category).filter(Category.name == name, Category.is_global == True).first()
            if not exists:
                db.add(Category(name=name, user_id=None, is_global=True))
            db.commit()
        print(f"Categorías globales sembradas {len(GLOBAL_CATEGORIES)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_categories()