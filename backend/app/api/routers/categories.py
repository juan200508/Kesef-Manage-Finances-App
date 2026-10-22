from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter, user_or_ip_key, READ_LIMIT, WRITE_LIMIT
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut
from app.core.exceptions import CategoryNotFoundError, DefaultCategoryNotConfiguredError
from app.services.category_service import delete_category_and_reassign_movements
from app.core.responses import AUTH_RESPONSES

router = APIRouter(prefix="/categories", tags=['categories'], responses=AUTH_RESPONSES)

@router.post(
    "", 
    response_model=CategoryOut, 
    status_code=status.HTTP_201_CREATED, 
    summary="Create a personal category",
    responses={
        409: {"description": "Category name duplicated"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def create_category(
    request: Request,
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Create a personal category for an authenticated user """

    category = (
        db.query(Category).filter(
            Category.name == category_in.name, 
            Category.is_global == False,
            Category.user_id == current_user.id
        ).first()
    )
    if category: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category alredy created with this name")

    new_category = Category(
        name = category_in.name,
        user_id = current_user.id,
        is_global = False
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("", response_model=list[CategoryOut], summary="List global and personal categories",)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def list_categories(
    request: Request,
    name: str | None = Query(default=None, description="Category name", examples=["Otros"]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ List categories that the user have created with the global ones. If the name parameter comes in the request, will search for matches (case-insensitive) """

    query = db.query(Category).filter(
        (Category.user_id == current_user.id) | (Category.is_global == True) # noqa: E712
    )

    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))

    return query.order_by(Category.is_global.desc(), Category.created_at.desc()).all()


@router.get(
    "/{category_id}", 
    response_model=CategoryOut, 
    summary="Get a specific category",
    responses={
        404: {"description": "Category not found"}
    }
)
@limiter.limit(READ_LIMIT, key_func=user_or_ip_key)
def get_category(
    request: Request,
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Get a category, whether it is global or belongs to an authenticated user """
    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            (Category.user_id == current_user.id) | (Category.is_global == True),
        ).first()
    )

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    return category


@router.put(
    "/{category_id}", 
    response_model=CategoryOut, 
    summary="Update a personal category",
    responses={
        404: {"description": "Category not found"}
    }
)
@limiter.limit(WRITE_LIMIT, key_func=user_or_ip_key)
def update_category(
    request: Request,
    category_id: UUID,
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Update a personal category. The global ones can't be updated by the users. """
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    category.name = category_in.name
    db.commit()
    db.refresh(category)

    return category


@router.delete(
    "/{category_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Delete a personal category",
    responses={
        404: {"description": "Category not found"},
        500: {"description": "Category Other not exists"}
    }
)
@limiter.limit("10/minute", key_func=user_or_ip_key)
def delete_category(
    request: Request,
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ Delete a personal category and if it has some movements, this will be assign to a default category. The global ones can't be deleted """
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
