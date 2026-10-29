# Realizar un registro de un usuario
def test_register_success(client):
    response = client.post(
        "/register",
        json={"email": "nuevo@kesef.com", "password": "claveNueva123457*", "full_name": "Nuevo Usuario"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "nuevo@kesef.com"
    assert data["full_name"] == "Nuevo Usuario"
    assert "id" in data
    assert "hashed_password" not in data


# Intentar realizar un registro con un correo ya existente
def test_register_duplicate_email(client):
    user_data = {"email": "duplicado@kesef.com", "password": "claveNueva123457", "full_name": "Uno"}
    client.post("/register", json=user_data)

    response = client.post("/register", json=user_data)

    assert response.status_code == 400


# Realizar un login de un usuario registrado
def test_login_success(client):
    user_data = {"email": "login@kesef.com", "password": "claveNueva123457", "full_name": "Login"}
    client.post("/register", json=user_data)

    response = client.post(
        "/login", json={"email": user_data["email"], "password": user_data["password"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# Intentar realizar un login con una contraseña incorrecta
def test_login_wrong_password(client):
    user_data = {"email": "wrongpass@kesef.com", "password": "clave12345", "full_name": "Test"}
    client.post("/register", json=user_data)

    response = client.post(
        "/login", json={"email": user_data["email"], "password": "incorrecta"}
    )

    assert response.status_code == 401


# Intentar realizar un login con un correo inexistente
def test_login_nonexistent_email(client):
    response = client.post(
        "/login", json={"email": "noexiste@kesef.com", "password": "cualquiera"}
    )

    assert response.status_code == 401

# Intentar ingresar a un endpoint sin token de acceso

def test_protected_endpoint_requires_token(client):
    response = client.get("/categories")

    assert response.status_code == 401


# Eliminar una categoría para realizar la reasignación a otra
def test_delete_category_reassigns_movements_to_otros(
    client, registered_user, otros_category
):
    cat_response = client.post(
        "/categories", json={"name": "Temporal"}, headers=registered_user["headers"]
    )
    category_id = cat_response.json()["id"]

    movement_response = client.post(
        "/movements",
        json={
            "category_id": category_id,
            "movement_type": "COMPRA",
            "amount": 50000,
            "description": "Prueba de reasignación",
        },
        headers=registered_user["headers"],
    )
    movement_id = movement_response.json()["id"]

    delete_response = client.delete(
        f"/categories/{category_id}", headers=registered_user["headers"]
    )
    assert delete_response.status_code == 204

    get_movement_response = client.get(
        f"/movements/{movement_id}", headers=registered_user["headers"]
    )
    assert get_movement_response.json()["category_id"] == str(otros_category.id)


def test_openapi_schema_is_generated(client):
    assert client.get("/openapi.json").status_code == 200