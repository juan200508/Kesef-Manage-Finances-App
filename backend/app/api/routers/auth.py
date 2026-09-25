from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token

router = APIRouter(prefix="", tags=['auth'])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Crea un nuevo usuario. El email debe ser único
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario registrado con ese email."
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


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Verifica que el email y la contrseña sean correctos, devuelve el access token
    user = db.query(User).filter(User.email == credentials.email).first()

    # Mismo mensaje para si el email no existe como para contraseña incorrecta
    # para no informar cuál falló
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email o contraseña incorrectos"
    )

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise invalid_credentials_exception

    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=access_token, token_type="bearer")
