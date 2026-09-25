from datetime import datetime, timedelta, timezone

from jose import JWSError, jwt

import bcrypt

from app.core.config import settings


def hash_password(password: str) -> str:
    # Genera el hash de una contraseña en texto plano.
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password:str) -> bool:
    # Compara una contaseña en texto plano en contra de su hash
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Genera un JWT firmado a partir de un payload 
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    # Decodifica y valida un JWT. Lanza JWTError si es inválido o expiró
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
