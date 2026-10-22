import uuid

import pytest
from starlette.requests import Request

from app.core.rate_limit import limiter, user_or_ip_key
from app.core.security import create_access_token


def make_request(headers: dict | None = None) -> Request:
    """Construye un Request mínimo para probar user_or_ip_key sin levantar la app."""
    scope = {
        "type": "http",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
        "client": ("1.2.3.4", 1234),
    }
    return Request(scope)


@pytest.fixture()
def rate_limit_on():
    """Enciende el limiter solo para el test que lo pide (el conftest lo apaga
    en todos los demás). Pídela SIEMPRE después de registered_user / other_user
    en los argumentos del test: así el login de esas fixtures no cuenta."""
    limiter.reset()
    limiter.enabled = True
    yield
    limiter.enabled = False
    limiter.reset()

# ---------------------------------------------------------------------------
# user_or_ip_key (pruebas unitarias; la primera es la regresión del return None)
# ---------------------------------------------------------------------------

def test_key_without_authorization_header_falls_back_to_ip():
    assert user_or_ip_key(make_request()) == "1.2.3.4"


def test_key_with_valid_token_uses_user_id():
    token = create_access_token({"sub": "abc-123"})
    request = make_request({"Authorization": f"Bearer {token}"})

    assert user_or_ip_key(request) == "user:abc-123"


def test_key_with_garbage_token_falls_back_to_ip():
    request = make_request({"Authorization": "Bearer esto.no.es.un.jwt"})

    assert user_or_ip_key(request) == "1.2.3.4"


# ---------------------------------------------------------------------------
# Endpoints públicos: /login y /register (llave = IP)
# ---------------------------------------------------------------------------

def test_login_is_rate_limited(client, registered_user, rate_limit_on):
    payload = {"email": registered_user["email"], "password": "incorrecta"}

    statuses = [client.post("/login", json=payload).status_code for _ in range(6)]

    assert statuses[:5] == [401] * 5     # los 5 permitidos llegan al endpoint
    assert statuses[5] == 429            # el sexto lo corta el limiter


def test_register_is_rate_limited(client, rate_limit_on):
    statuses = []
    for i in range(6):
        response = client.post("/register", json={
            "email": f"user{i}@kesef.com",
            "password": "testpass123",
            "full_name": f"Usuario {i}",
        })
        statuses.append(response.status_code)

    assert statuses[:5] == [201] * 5
    assert statuses[5] == 429


def test_rate_limit_response_body(client, registered_user, rate_limit_on):
    payload = {"email": registered_user["email"], "password": "incorrecta"}
    for _ in range(5):
        client.post("/login", json=payload)

    response = client.post("/login", json=payload)

    assert response.status_code == 429
    assert response.json()["error"].startswith("Rate limit exceeded")


# ---------------------------------------------------------------------------
# Endpoint autenticado: límite por usuario (DELETE /categories/{id} = 10/minute)
# ---------------------------------------------------------------------------

def test_authenticated_endpoint_is_rate_limited(client, registered_user, rate_limit_on):
    url = f"/categories/{uuid.uuid4()}"      # no existe: cada intento da 404 y cuenta igual
    h = registered_user["headers"]

    statuses = [client.delete(url, headers=h).status_code for _ in range(11)]

    assert statuses[:10] == [404] * 10
    assert statuses[10] == 429


def test_rate_limit_is_per_user_not_shared(client, registered_user, other_user, rate_limit_on):
    """Un usuario que agota su límite no bloquea a otro (aunque en los tests
    ambos salgan de la misma IP): la llave es el id del usuario."""
    url = f"/categories/{uuid.uuid4()}"

    for _ in range(11):
        client.delete(url, headers=registered_user["headers"])
    blocked = client.delete(url, headers=registered_user["headers"])
    other = client.delete(url, headers=other_user["headers"])

    assert blocked.status_code == 429
    assert other.status_code == 404           # el otro usuario sigue con su contador en 0