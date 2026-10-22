import pytest
import uuid

from app.models.monthly_income import MonthlyIncomeSource


# ---------------------------------------------------------------------------
# Creación de ingresos
# ---------------------------------------------------------------------------

# Crear un ingreso para un usuario
def test_create_personal_income(client, registered_user):
    data_inc = {
        "year": 2026,
        "month": 10,
        "amount": 4500000,
        "source": MonthlyIncomeSource.SALARIO,
    }

    response = client.post(
        "/monthly_incomes",
        json=data_inc,
        headers=registered_user["headers"]
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == registered_user["id"]
    assert data["source"] == MonthlyIncomeSource.SALARIO


# Crear una categoría con una descripción
def test_create_personal_income_with_description(client, registered_user):
    data_inc = {
        "year": 2026,
        "month": 10,
        "amount": 4500000,
        "source": MonthlyIncomeSource.SALARIO,
        "description": "Pago del salario 10 días antes"
    }

    response = client.post(
        "/monthly_incomes",
        json=data_inc,
        headers=registered_user["headers"]
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == registered_user["id"]
    assert data["source"] == MonthlyIncomeSource.SALARIO
    assert data["description"] == data_inc["description"]


# Intentar crear un ingreso sin un source
def test_create_personal_income_without_source(client, registered_user):
    data_inc = {
        "year": 2026,
        "month": 10,
        "amount": 4500000,
        "description": "Pago del salario 10 días antes"
    }

    h = registered_user["headers"]
    assert client.post("/monthly_incomes",json=data_inc,headers=h).status_code == 422


# Intentar crear un ingreso con un source que no existe o es inválido
def test_create_income_with_invalid_source(client, registered_user):
    data_inc = {
            "year": 2026,
            "month": 10,
            "amount": 4500000,
            "source": "VACACIONES",
        }
    
    response = client.post(
        "/monthly_incomes",
        json=data_inc,
        headers=registered_user["headers"]
    )

    assert response.status_code == 422


# Intentar crear un ingreso con un mes y año fuera del rango
@pytest.mark.parametrize("year, month", [
    (2026, 0), (2026, 13),      # mes fuera de rango
    (1999, 10), (2101, 10),     # año fuera de rango
])
def test_create_income_with_invalid_month(client, registered_user, year, month):
    data_inc = {
        "year": year,
        "month": month,
        "amount": 4500000,
        "source": MonthlyIncomeSource.SALARIO,
    }

    response = client.post(
        "/monthly_incomes",
        json=data_inc,
        headers=registered_user["headers"]
    )
    
    assert response.status_code == 422


# Crear dos ingresos con la misma fecha
def test_create_personal_income_with_same_date(client, registered_user):
    data_inc = {
        "year": 2026,
        "month": 10,
        "amount": 4500000,
        "source": MonthlyIncomeSource.SALARIO,
    }

    data_inc2 = {
        "year": 2026,
        "month": 10,
        "amount": 1000000,
        "source": MonthlyIncomeSource.FREELANCE,
    }

    response = client.post(
        "/monthly_incomes",
        json=data_inc,
        headers=registered_user["headers"]
    )

    response2 = client.post(
        "/monthly_incomes",
        json=data_inc2,
        headers=registered_user["headers"]
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == registered_user["id"]
    assert data["source"] == MonthlyIncomeSource.SALARIO

    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["user_id"] == registered_user["id"]
    assert data2["source"] == MonthlyIncomeSource.FREELANCE


# ---------------------------------------------------------------------------
# Filtros y obtención de ingresos
# ---------------------------------------------------------------------------

# Filtrar movimientos por mes y año
def test_income_filters(client, registered_user, other_user, create_income):
    create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)
    create_income(user_data=registered_user, year=2026, month=10, amount=2000000, source=MonthlyIncomeSource.FREELANCE)
    create_income(user_data=registered_user, year=2026, month=9, amount=2000000, source=MonthlyIncomeSource.FREELANCE)
    create_income(user_data=registered_user, year=2026, month=9, amount=5000000, source=MonthlyIncomeSource.CONSIGNACIONES)
    create_income(user_data=registered_user, year=2025, month=9, amount=5000000, source=MonthlyIncomeSource.CONSIGNACIONES)
    create_income(user_data=other_user, year=2026, month=9, amount=5000000, source=MonthlyIncomeSource.CONSIGNACIONES)

    h = registered_user["headers"]
    
    assert len(client.get("/monthly_incomes", headers=h).json()) == 5
    assert len(client.get("/monthly_incomes?year=2026", headers=h).json()) == 4

    data = client.get("/monthly_incomes?year=2026&month=9", headers=h).json()
    assert len(data) == 2 and data[0]["month"] == 9

    data = client.get("/monthly_incomes?year=2026&month=9&month=10", headers=h).json()
    assert len(data) == 4


# Obtener un ingreso por su ID
def test_get_income_by_id(client, registered_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    uuid_test = uuid.uuid4()
    h = registered_user["headers"]

    assert client.get(f"/monthly_incomes/{income.id}",headers=h).status_code == 200
    assert client.get(f"/monthly_incomes/{str(uuid_test)}",headers=h).status_code == 404


# ---------------------------------------------------------------------------
# Actualización de ingresos
# ---------------------------------------------------------------------------

# Actualizar un ingreso con un solo campo
def test_update_income(client, registered_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    h = registered_user["headers"]
    inc_created = client.get(f"/monthly_incomes/{income.id}",headers=h).json()

    response_up = client.put(
        f"/monthly_incomes/{income.id}",
        json={"amount": 5500000},
        headers=h    
    )
    inc_updated = response_up.json()

    assert response_up.status_code == 200
    assert inc_updated["updated_at"] != inc_created["updated_at"]
    assert inc_updated["created_at"] == inc_created["created_at"]
    assert inc_updated["amount"] == "5500000.00"


# Actualizar un ingreso con diferentes campos
def test_update_income_with_some_parameters(client, registered_user, other_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    h = registered_user["headers"]

    response_up = client.put(
        f"/monthly_incomes/{income.id}",
        json={"source": "PRUEBAS"},
        headers=h    
    )

    response_wrong = client.put(
        f"/monthly_incomes/{income.id}",
        json={"source": MonthlyIncomeSource.SALARIO},
        headers=other_user["headers"]   
    )

    assert response_up.status_code == 422
    assert response_wrong.status_code == 404


# ---------------------------------------------------------------------------
# Eliminación de ingresos
# ---------------------------------------------------------------------------

# Eliminar un ingreso de un usuario
def test_delete_income(client, registered_user, other_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    assert client.delete(f"/monthly_incomes/{income.id}",headers=other_user["headers"]).status_code == 404
    assert client.delete(f"/monthly_incomes/{income.id}",headers=registered_user["headers"]).status_code == 204
    assert client.get(f"/monthly_incomes/{income.id}",headers=registered_user["headers"]).status_code == 404


# ---------------------------------------------------------------------------
# Acceso de ingresos
# ---------------------------------------------------------------------------

# Intentar acceder a un endpoint sin token de acceso
def test_income_without_token(client, registered_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    assert client.get(f"/monthly_incomes/{income.id}").status_code == 401


# Intentar acceder a ingresos que no pertenecen al usuarios
def test_one_user_cannot_access_to_other_user_income(client, registered_user, other_user, create_income):
    income = create_income(user_data=registered_user, year=2026, month=10, amount=5000000, source=MonthlyIncomeSource.SALARIO)

    response = client.get(
        f"/monthly_incomes/{income.id}",
        headers=other_user["headers"]
    )

    owner_response = client.get(
        f"/monthly_incomes/{income.id}",
        headers=registered_user["headers"]
    )

    assert response.status_code == 404
    assert owner_response.status_code == 200

