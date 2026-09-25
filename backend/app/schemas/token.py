from pydantic import BaseModel

class Token(BaseModel):
    # Lo que devuelve la API /login.
    access_token: str
    token_type: str = "bearer"