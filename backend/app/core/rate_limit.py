from fastapi import Request
from jose import JWTError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.security import decode_access_token

# Limiter base: llave es la IP del cliente
limiter = Limiter(key_func=get_remote_address)

READ_LIMIT = "60/minute"
WRITE_LIMIT = "30/minute"

# Para endpoints autenticados: limita por usuario (sub del JWT)
# Si no hay token válido, cae a la IP, así que mandar tokens basura tampoco evade el límite
def user_or_ip_key(request: Request) -> str: 
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        try:
            payload = decode_access_token(auth.removeprefix("Bearer "))
            return f"user:{payload['sub']}"
        except (JWTError, KeyError):
            pass
    return get_remote_address(request)