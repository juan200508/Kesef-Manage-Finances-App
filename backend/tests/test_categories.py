# ---------------------------------------------------------------------------
# Creación de categorías
# ---------------------------------------------------------------------------

# Crear una categoría personal de un usuario
def test_create_category(client, registered_user):
    response = client.post(
        "/categories",
        json={"name": "Mascotas"},
        headers=registered_user["headers"],
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mascotas"
    assert data["is_global"] is False


# Crear una categoría duplicada para el mismo usuario
def test_create_duplicate_category_same_user(client, registered_user):
    client.post("/categories", json={"name": "Mascotas"}, headers=registered_user["headers"])

    response = client.post(
        "/categories", json={"name": "Mascotas"}, headers=registered_user["headers"]
    )

    assert response.status_code == 409


# ---------------------------------------------------------------------------
# Listar y filtrar categorías
# ---------------------------------------------------------------------------

# Listar las categorías incluyendo las que se han creado personales
def test_list_categories_includes_own_personal(client, registered_user):
    client.post("/categories", json={"name": "Suscripciones"}, headers=registered_user["headers"])

    response = client.get("/categories", headers=registered_user["headers"])

    names = [c["name"] for c in response.json()]
    assert "Suscripciones" in names


# ---------------------------------------------------------------------------
# Actualización de categorías
# ---------------------------------------------------------------------------

# Intentar actualizar una categoría que no pertenece al usuario
def test_cannot_update_global_category(client, registered_user, otros_category):
    response = client.put(
        f"/categories/{otros_category.id}",
        json={"name": "Ya no es Otros"},
        headers=registered_user["headers"],
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Actualización de categorías
# ---------------------------------------------------------------------------

# Intentar eliminar una categoría que no pertenece al usuario o es global
def test_cannot_delete_global_category(client, registered_user, otros_category):
    response = client.delete(
        f"/categories/{otros_category.id}", headers=registered_user["headers"]
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Actualización de categorías
# ---------------------------------------------------------------------------

# Intentar acceder a una categoría que no pertenece al usuario
def test_cannot_access_another_users_category(client, registered_user, other_user):
    create_response = client.post(
        "/categories", json={"name": "Privada"}, headers=registered_user["headers"]
    )
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}", headers=other_user["headers"])

    assert response.status_code == 404