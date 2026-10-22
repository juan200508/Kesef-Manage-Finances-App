from uuid import UUID
from datetime import datetime

from app.models.movement import MovementType


# ---------------------------------------------------------------------------
# Creación de moviemientos
# ---------------------------------------------------------------------------

# Crea un movimiento con una categoría personal
def test_create_movement_with_personal_category(client, registered_user, personal_category):
    data_mov = {
        "category_id": str(personal_category.id),
        "movement_type": MovementType.TRANSFERENCIA,
        "amount": 500000,
        "description": "Prueba de movimiento con categoría personal"
    }
    
    response = client.post(
        "/movements",
        json=data_mov,
        headers=registered_user["headers"]
    )

    assert response.status_code == 201
    data = response.json()
    assert data['category_id'] == str(personal_category.id)
    assert data['user_id'] == registered_user["id"]
    assert data['movement_type'] == MovementType.TRANSFERENCIA


# Crear un movimiento con una categoría global
def test_create_movement_with_global_category(client, registered_user, otros_category):
    data_mov = {
        "category_id": str(otros_category.id),
        "movement_type": MovementType.PAGO,
        "amount": 350000,
        "description": "Prueba de movimiento con categoría global"
    }

    response = client.post(
        "/movements",
        json=data_mov,
        headers=registered_user["headers"]
    )

    assert response.status_code == 201
    data = response.json()
    assert data['category_id'] == str(otros_category.id)
    assert data['user_id'] == registered_user["id"]
    assert data['movement_type'] == MovementType.PAGO


# Intentar crear un movimiento con una categoría que no fue creada por el usuario
def test_create_movement_with_someone_else_category(client, registered_user, else_category):
    data_mov = {
        "category_id": str(else_category.id),
        "movement_type": MovementType.TRANSFERENCIA,
        "amount": 500000,
        "description": "Prueba de movimiento con categoría personal"
    }
    
    response = client.post(
        "/movements",
        json=data_mov,
        headers=registered_user["headers"]
    )

    assert response.status_code == 404


# Crear un movimiento con un tipo que no existe
def test_create_movement_with_wrong_type(client, registered_user, personal_category):
    data_mov = {
        "category_id": str(personal_category.id),
        "movement_type": "Vehículo",
        "amount": 500000,
        "description": "Prueba de movimiento con categoría personal"
    }
    
    response = client.post(
        "/movements",
        json=data_mov,
        headers=registered_user["headers"]
    )

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Filtros de los movimientos
# ---------------------------------------------------------------------------

# Crear movimientos y filtarlos por tipo de movimiento
def test_movement_type_filter(client, registered_user, personal_category, create_movement):

    create_movement(user_data=registered_user, category=personal_category,amount=500000, movement_date=datetime(2026,9,15), movement_type=MovementType.COMPRA)
    create_movement(user_data=registered_user, category=personal_category,amount=500000, movement_date=datetime(2026,9,15), movement_type=MovementType.PAGO)

    response = client.get(
        f"/movements?movement_type=COMPRA",
        headers=registered_user["headers"]
    )

    data = response.json()
    assert response.status_code == 200
    assert data[0]["movement_type"] == "COMPRA"
    assert len(data) == 1


# Crear movimientos y filtarlos por las categorías que el usuario tiene acceso
def test_category_filter(client, registered_user, personal_category, otros_category, create_movement):
    create_movement(user_data=registered_user, category=otros_category,amount=500000, movement_date=datetime(2026,9,15))
    create_movement(user_data=registered_user, category=otros_category,amount=500000, movement_date=datetime(2026,9,15))

    response = client.get(
        f"/movements?category_id={personal_category.id}&category_id={otros_category.id}",
        headers=registered_user["headers"]
    )

    assert response.status_code == 200


# Crear movimientos y filtrarlos por fecha
def test_movement_date_filter_with_startdate_enddate(client, registered_user, otros_category, create_movement):
    create_movement(user_data=registered_user, category=otros_category,amount=500000, movement_date=datetime(2026,9,15))
    create_movement(user_data=registered_user, category=otros_category,amount=500000, movement_date=datetime(2026,9,30))
    create_movement(user_data=registered_user, category=otros_category,amount=500000, movement_date=datetime(2026,10,6))

    
    response = client.get(
        f"/movements?start_date=2026-09-14&end_date=2026-09-30",
        headers=registered_user["headers"]
    )

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


# ---------------------------------------------------------------------------
# Actualización de movimientos
# ---------------------------------------------------------------------------

# Actualizar un movimiento enviando solamente un campo 
def test_update_movement_one_field(client, registered_user, personal_category, create_movement):

    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    response_mov = client.get(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    data_update = {"amount": 500000}
    response_update = client.put(
        f"/movements/{mov.id}",
        json=data_update,
        headers=registered_user["headers"]
    )

    mov_created = response_mov.json()
    mov_updated = response_update.json()

    assert response_update.status_code == 200
    assert mov_updated["updated_at"] != mov_created["updated_at"]
    assert mov_updated["created_at"] == mov_created["created_at"]
    assert mov_updated["movement_date"] == mov_created["movement_date"]
    assert mov_updated["amount"] == "500000.00"


# Intentar actualizar un movimiento con una categoría que no pertenece al usuario o que no es global 
def test_update_movement_with_else_category(client, registered_user, personal_category, else_category, create_movement):
    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    data_update = {"category_id": str(else_category.id)}
    response_update = client.put(
        f"/movements/{mov.id}",
        json=data_update,
        headers=registered_user["headers"]
    )

    assert response_update.status_code == 404


# Intentar actualizar un movimiento que no pertenece al usuario
def test_update_other_user_movement(client, registered_user, other_user, else_category, create_movement):
    mov = create_movement(user_data=other_user, category=else_category, amount=450000, movement_date=datetime(2026, 10, 5))

    response = client.put(
        f"/movements/{mov.id}",
        json={"amount": 650000},
        headers=registered_user["headers"]
    )

    assert response.status_code == 404


# Intentar actualizar un movimiento que se ha eliminado
def test_update_movement_deleted(client, registered_user, personal_category, create_movement):

    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    client.delete(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    data_update = {"amount": 500000}
    response_update = client.put(
        f"/movements/{mov.id}",
        json=data_update,
        headers=registered_user["headers"]
    )

    assert response_update.status_code == 404


# ---------------------------------------------------------------------------
# Eliminación de movimientos
# ---------------------------------------------------------------------------

# Intentar eliminar un movimiento que no pertenece al usuario
def test_delete_other_user_movement(client, registered_user, other_user, else_category, create_movement):
    mov = create_movement(user_data=other_user, category=else_category, amount=450000, movement_date=datetime(2026, 10, 5))

    response = client.delete(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    assert response.status_code == 404


# Intentar buscar u obtener un movimiento que se ha eliminado
def test_delete_movement_then_get(client, registered_user, personal_category, create_movement):
    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    client.delete(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    response = client.get(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    assert response.status_code == 404


# Eliminar un movimiento
def test_delete_movement(client, registered_user, personal_category, create_movement):
    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    response = client.delete(
        f"/movements/{mov.id}",
        headers=registered_user["headers"]
    )

    assert response.status_code == 204


# ---------------------------------------------------------------------------
# Validaciones de seguridad
# ---------------------------------------------------------------------------

# Realizar alguna petición sin el token de registro del usuario
def test_get_movement_without_token(client, registered_user, personal_category, create_movement):
    mov = create_movement(user_data=registered_user, category=personal_category, amount=450000, movement_date=datetime(2026, 10, 5))

    response = client.get(
        f"/movements/{mov.id}"
    )

    assert response.status_code == 401


# Intentar ver los movimientos de otro usuario
def test_user_cannot_see_movements_from_another_user_v2(client, registered_user, other_user, else_category, create_movement):
    other_user_mov = create_movement(user_data=other_user, category=else_category,amount=500000, movement_date=datetime(2026,9,15))

    response = client.get(
        f"/movements/{other_user_mov.id}",
        headers=registered_user["headers"]
    )

    owner_response = client.get(
        f"/movements/{other_user_mov.id}",
        headers=other_user["headers"]
    )   

    assert response.status_code == 404
    assert owner_response.status_code == 200