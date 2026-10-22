from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.rate_limit import limiter, user_or_ip_key, READ_LIMIT, WRITE_LIMIT
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.category import Category
from app.models.movement import Movement, MovementType
from app.schemas.movement import MovementCreate, MovementOut, MovementUpdate
from app.core.responses import AUTH_RESPONSES


router = APIRouter(prefix="/movements", tags=['movements'], responses=AUTH_RESPONSES)


@router.post(
    "", 
    response_model=MovementOut, 
    status_code=status.HTTP_201_CREATED, 
    summary="Create a movement",
    responses={
        404: {"description": "Category not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def created_movement(
    request: Request,
    movement_in: MovementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Create a movement for an authenticated user. Use an id returned by GET/categories """
    
    category = ( db.query(Category).filter(
            Category.id == movement_in.category_id,
            (Category.user_id == current_user.id) | (Category.is_global == True)
        ).first()
    )

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    new_movement = Movement(
        user_id = current_user.id,
        category_id = movement_in.category_id,
        movement_type = movement_in.movement_type,
        amount = movement_in.amount,
        description = movement_in.description
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


@router.get("", response_model=list[MovementOut], summary="List all the movements",)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def list_movements(
    request: Request,
    movement_type: list[MovementType] | None = Query(default=None, description="The movement type"),
    category_id: list[UUID] | None = Query(default=None, description="Could be a personal category or a global one"),
    start_date: datetime | None = Query(default=None, description="The date of the user start searching"),
    end_date: datetime | None = Query(default=None, description="The final date that the user wants to search"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    """ List the movements that belongs an authenticated user. In addition manage filter for movement type, category and dates """

    query = db.query(Movement).filter(
        Movement.user_id == current_user.id
    )

    if movement_type:
        query = query.filter(Movement.movement_type.in_(movement_type))
    
    if category_id:
        query = query.filter(Movement.category_id.in_(category_id))
    
    if start_date and end_date:
        query = query.filter(Movement.movement_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Movement.movement_date >= start_date)
    elif end_date: 
        query = query.filter(Movement.movement_date <= end_date)

    return query.order_by(Movement.created_at.desc()).all()


@router.get(
    "/{movement_id}", 
    response_model=MovementOut, 
    summary="Get a specific movement",
    responses={
        404: {"description": "Movement not found"}
    }
)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def get_movement(
    request: Request,
    movement_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Get a movement by its ID """
    movement = (
        db.query(Movement)
        .filter(
            Movement.id == movement_id,
            (Movement.user_id == current_user.id) 
        ).first()
    )

    if movement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")

    return movement


@router.put(
    "/{movement_id}", 
    response_model=MovementOut, 
    summary="Update a movement",
    responses={
        404: {"description": "Category or Movement not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def update_movement(
    request: Request,
    movement_id: UUID,
    movement_in: MovementUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Update a movement by its ID """
    movement = (
        db.query(Movement)
        .filter(
            Movement.id == movement_id,
            (Movement.user_id == current_user.id) 
        ).first()
    )
    if movement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")

    # Convierte los campos del schema en un diccionario, incluyendo los campos que el usuario no envío.
    # el excluse_unset solo actualiza los campos que el usuario especificó con los otros sin tocar los demás 
    update_data = movement_in.model_dump(exclude_unset=True)

    # Válida que la nueva categoría enviada corresponde a una global o creada por el usuario
    if movement_in.category_id is not None:
        category = ( db.query(Category).filter(
                Category.id == movement_in.category_id,
                (Category.user_id == current_user.id) | (Category.is_global == True)
            ).first()
        )    
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Actualiza de manera automática los campos que han sido especificados por el cliente 
    for field, value in update_data.items():
        setattr(movement, field, value)

    db.commit()
    db.refresh(movement)

    return movement


@router.delete(
    "/{movement_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Delete a movement",
    responses={
        404: {"description": "Movement not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def delete_movement(
    request: Request,
    movement_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Delete a movement by its ID """
    movement = (
        db.query(Movement)
        .filter(
            Movement.id == movement_id,
            (Movement.user_id == current_user.id) 
        ).first()
    )
    if movement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")

    db.delete(movement)
    db.commit()