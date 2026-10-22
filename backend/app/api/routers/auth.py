from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.core.rate_limit import limiter 
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token

router = APIRouter(prefix="", tags=['auth'])

@router.post(
    "/register", 
    response_model=UserOut, 
    status_code=status.HTTP_201_CREATED, 
    summary="Register a user",
    responses={
        400: {"description": "Email alredy registered"},
        429: {"description": "5 request per hour"}
    }
)
@limiter.limit("5/hour")
def register(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a user. The user has to be unique."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User alredy created with this email"
        )

    new_user = User(
        email = user_in.email,
        hashed_password = hash_password(user_in.password),
        full_name = user_in.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login", 
    response_model=Token,
    summary="Login",
    responses={
        401: {"description": "Incorrect password or email."},
        429: {"description": "Too many requests (5 per minute)"}
    }
)
@limiter.limit("5/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """ Verify that email and password are correct, return the access token """
    user = db.query(User).filter(User.email == credentials.email).first()

    # Mismo mensaje para si el email no existe como para contraseña incorrecta
    # para no informar cuál falló
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise invalid_credentials_exception

    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=access_token, token_type="bearer")
