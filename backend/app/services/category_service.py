from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import CategoryNotFoundError, DefaultCategoryNotConfiguredError
from app.models.category import Category
from app.models.movement import Movement

def delete_category_and_reassign_movements(
        db: Session,
        category_id: UUID,
        user_id: UUID
):
    """Elimina una categoría personal del usuario, reasignando primero
    todos sus movimientos asociados a la categoría global 'Otros'.

    Args:
        db: sesión activa de SQLAlchemy, provista por el router.
        category_id: id de la categoría personal a eliminar.
        user_id: id del usuario dueño de la categoría (para validar pertenencia).

    Raises:
        CategoryNotFoundError: si la categoría no existe o no pertenece al usuario.
        DefaultCategoryNotConfiguredError: si la categoría global 'Otros' no existe.
    """
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == user_id)
        .first()
    )
    if not category:
        raise CategoryNotFoundError(category_id=str(category_id))

    default_category = (
            db.query(Category).filter(Category.name.ilike("Otros"), Category.is_global == True).first()
        )
    if not default_category:
        raise DefaultCategoryNotConfiguredError()

    db.query(Movement).filter(Movement.category_id == category_id).update(
        {"category_id": default_category.id},
        synchronize_session=False
    )
    db.delete(category)
    db.commit()

    return None
    

    
    