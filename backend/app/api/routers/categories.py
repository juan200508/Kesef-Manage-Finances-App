from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut
from app.core.exceptions import CategoryNotFoundError, DefaultCategoryNotConfiguredError
from app.services.category_service import delete_category_and_reassign_movements

router = APIRouter(prefix="/categories", tags=['categories'])

@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Crea una categoria personal para un usuario autenticado

    category = (
        db.query(Category).filter(
            Category.name == category_in.name, 
            Category.is_global == False,
            Category.user_id == current_user.id
        ).first()
    )
    if category: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Categoría ya creada con este nombre.")

    new_category = Category(
        name = category_in.name,
        user_id = current_user.id,
        is_global = False
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("", response_model=list[CategoryOut])
def list_categories(
    name: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Lista las categorías que el usuario ha creado junto con las globales
    # si se pasa el parámetro name, buscará por coincidencias (case-insensitive)

    query = db.query(Category).filter(
        (Category.user_id == current_user.id) | (Category.is_global == True) # noqa: E712
    )

    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))

    return query.order_by(Category.is_global.desc(), Category.created_at.desc()).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Obtiene una categoría, si es global o si pertenece al usuario autenticado
    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            (Category.user_id == current_user.id) | (Category.is_global == True),
        ).first()
    )

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: UUID,
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Actualiza una categoría personal. Las categorías globales no pueden ser editadas por los usuarios
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )

    category.name = category_in.name
    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Elimina una categoría personal y si tiene algún movimiento asígnado lo asigna a un movimiento default, las categorias globales no se pueden editar
    try:
        delete_category_and_reassign_movements(
            db=db,
            category_id=category_id,
            user_id=current_user.id
        )
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from None
    except DefaultCategoryNotConfiguredError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message) from None

    return None
