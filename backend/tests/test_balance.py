from datetime import datetime
from decimal import Decimal

import pytest

from app.models.monthly_income import MonthlyIncomeSource
from app.models.movement import MovementType


# ---------------------------------------------------------------------------
# Helpers y fixture de datos
# ---------------------------------------------------------------------------

# Los montos llegan como string ("4500000.00"); se comparan como Decimal.
def D(value) -> Decimal:
    return Decimal(str(value))


# Convierte la lista de balances en {mes: balance} para consultarlos fácil.
def by_month(data: list[dict]) -> dict[int, dict]:
    return {item["month"]: item for item in data}


# Crear movimientos e ingresos para realizar los balances
@pytest.fixture()
def balance_data(registered_user, other_user, personal_category, otros_category,
                 create_income, create_movement):
    u = registered_user

    # --- Septiembre 2026 ---
    create_income(user_data=u, year=2026, month=9, amount=3500000, source=MonthlyIncomeSource.SALARIO)
    create_income(user_data=u, year=2026, month=9, amount=1000000, source=MonthlyIncomeSource.FREELANCE)
    create_movement(user_data=u, category=personal_category, amount=300000,
                    movement_date=datetime(2026, 9, 3), movement_type=MovementType.COMPRA)
    create_movement(user_data=u, category=personal_category, amount=200000,
                    movement_date=datetime(2026, 9, 20), movement_type=MovementType.PAGO)
    create_movement(user_data=u, category=otros_category, amount=150000,
                    movement_date=datetime(2026, 9, 15), movement_type=MovementType.COMPRA)

    # --- Octubre 2026 ---
    create_income(user_data=u, year=2026, month=10, amount=2000000, source=MonthlyIncomeSource.SALARIO)
    create_movement(user_data=u, category=otros_category, amount=400000,
                    movement_date=datetime(2026, 10, 6))

    # --- 2025 (otro año) ---
    create_income(user_data=u, year=2025, month=12, amount=1000000, source=MonthlyIncomeSource.OTROS)
    create_movement(user_data=u, category=otros_category, amount=100000,
                    movement_date=datetime(2025, 8, 10))

    # --- Ruido de otro usuario ---
    create_income(user_data=other_user, year=2026, month=9, amount=999999, source=MonthlyIncomeSource.SALARIO)
    create_movement(user_data=other_user, category=otros_category, amount=888888,
                    movement_date=datetime(2026, 9, 15))


# ---------------------------------------------------------------------------
# Balance de un mes
# ---------------------------------------------------------------------------

def test_monthly_balance_totals(client, registered_user, balance_data):
    response = client.get("/balance?year=2026&month=9", headers=registered_user["headers"])

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    sep = data[0]
    assert sep["year"] == 2026
    assert sep["month"] == 9
    assert D(sep["total_income"]) == D(4500000)
    assert D(sep["total_expenses"]) == D(650000)
    assert D(sep["balance"]) == D(3850000)


def test_monthly_balance_breakdown_by_category(client, registered_user, balance_data, personal_category, otros_category):
    response = client.get("/balance?year=2026&month=9", headers=registered_user["headers"])

    sep = response.json()[0]
    breakdown = sep["expenses_by_category"]

    # Una fila por categoría (los dos movimientos de Vehículo se agrupan en una)
    assert len(breakdown) == 2

    # Ordenado de mayor a menor total
    assert [row["category_name"] for row in breakdown] == ["Vehículo", "Otros"]

    # Totales e ids correctos
    assert D(breakdown[0]["total"]) == D(500000)
    assert breakdown[0]["category_id"] == str(personal_category.id)
    assert D(breakdown[1]["total"]) == D(150000)
    assert breakdown[1]["category_id"] == str(otros_category.id)

    # La suma del desglose coincide con el total de gastos
    assert sum(D(row["total"]) for row in breakdown) == D(sep["total_expenses"])


def test_monthly_balance_only_income(client, registered_user, create_income):
    create_income(user_data=registered_user, year=2026, month=3, amount=2500000, source=MonthlyIncomeSource.SALARIO)

    response = client.get("/balance?year=2026&month=3", headers=registered_user["headers"])

    mar = response.json()[0]
    assert response.status_code == 200
    assert D(mar["total_income"]) == D(2500000)
    assert D(mar["total_expenses"]) == D(0)
    assert D(mar["balance"]) == D(2500000)
    assert mar["expenses_by_category"] == []


def test_monthly_balance_only_expenses(client, registered_user, otros_category, create_movement):
    create_movement(user_data=registered_user, category=otros_category, amount=300000, movement_date=datetime(2026, 3, 10))

    response = client.get("/balance?year=2026&month=3", headers=registered_user["headers"])

    mar = response.json()[0]
    assert response.status_code == 200
    assert D(mar["total_income"]) == D(0)
    assert D(mar["total_expenses"]) == D(300000)
    assert D(mar["balance"]) == D(-300000)
    assert len(mar["expenses_by_category"]) == 1


def test_all_movement_types_count_as_expenses(client, registered_user, otros_category, create_movement):
    create_movement(user_data=registered_user, category=otros_category, amount=100000,
                    movement_date=datetime(2026, 3, 10), movement_type=MovementType.COMPRA)
    create_movement(user_data=registered_user, category=otros_category, amount=50000,
                    movement_date=datetime(2026, 3, 11), movement_type=MovementType.PAGO)

    response = client.get("/balance?year=2026&month=3", headers=registered_user["headers"])

    assert D(response.json()[0]["total_expenses"]) == D(150000)


def test_month_boundaries(client, registered_user, otros_category, create_movement):
    """Un movimiento del 30/sep a las 23:59 es de septiembre; el del 1/oct 00:00 es de octubre."""
    create_movement(user_data=registered_user, category=otros_category, amount=100000,
                    movement_date=datetime(2026, 9, 30, 23, 59))
    create_movement(user_data=registered_user, category=otros_category, amount=200000,
                    movement_date=datetime(2026, 10, 1, 0, 0))

    response = client.get("/balance?year=2026&month=9&month=10", headers=registered_user["headers"])

    months = by_month(response.json())
    assert D(months[9]["total_expenses"]) == D(100000)
    assert D(months[10]["total_expenses"]) == D(200000)


# ---------------------------------------------------------------------------
# Aislamiento entre usuarios
# ---------------------------------------------------------------------------

def test_balance_does_not_mix_users(client, registered_user, other_user, balance_data):
    mine = client.get("/balance?year=2026&month=9", headers=registered_user["headers"]).json()[0]
    theirs = client.get("/balance?year=2026&month=9", headers=other_user["headers"]).json()[0]

    # Los totales de registered_user no incluyen los 999.999 / 888.888 de other_user
    assert D(mine["total_income"]) == D(4500000)
    assert D(mine["total_expenses"]) == D(650000)

    # Y other_user solo ve lo suyo
    assert D(theirs["total_income"]) == D(999999)
    assert D(theirs["total_expenses"]) == D(888888)
    assert D(theirs["balance"]) == D(999999 - 888888)


# ---------------------------------------------------------------------------
# Vista anual (sin parámetro month)
# ---------------------------------------------------------------------------

def test_yearly_balance_returns_only_months_with_data(client, registered_user, balance_data):
    response = client.get("/balance?year=2026", headers=registered_user["headers"])

    assert response.status_code == 200
    data = response.json()

    # Solo septiembre y octubre (no 12 meses), el más reciente primero
    assert [item["month"] for item in data] == [10, 9]

    months = by_month(data)
    assert D(months[10]["total_income"]) == D(2000000)
    assert D(months[10]["total_expenses"]) == D(400000)
    assert D(months[10]["balance"]) == D(1600000)
    assert D(months[9]["balance"]) == D(3850000)


def test_yearly_balance_includes_months_with_only_income_or_only_expenses(
        client, registered_user, balance_data):
    data = client.get("/balance?year=2025", headers=registered_user["headers"]).json()

    # Dic 2025: solo ingreso. Ago 2025: solo gasto. Orden descendente.
    assert [item["month"] for item in data] == [12, 8]

    months = by_month(data)
    assert D(months[12]["total_income"]) == D(1000000)
    assert D(months[12]["total_expenses"]) == D(0)
    assert D(months[8]["total_income"]) == D(0)
    assert D(months[8]["total_expenses"]) == D(100000)
    assert D(months[8]["balance"]) == D(-100000)


def test_yearly_balance_without_data_returns_empty_list(client, registered_user, balance_data):
    response = client.get("/balance?year=2024", headers=registered_user["headers"])

    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# Filtro por meses
# ---------------------------------------------------------------------------

def test_filter_single_month_returns_list_of_one(client, registered_user, balance_data):
    response = client.get("/balance?year=2026&month=10", headers=registered_user["headers"])

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["month"] == 10
    assert D(data[0]["balance"]) == D(1600000)


def test_filter_multiple_months(client, registered_user, balance_data):
    response = client.get("/balance?year=2026&month=9&month=10", headers=registered_user["headers"])

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

    months = by_month(data)
    assert D(months[9]["balance"]) == D(3850000)
    assert D(months[10]["balance"]) == D(1600000)


def test_filter_month_without_data_returns_zeros(client, registered_user, balance_data):
    """Si el mes se pide explícitamente y no tiene datos, se devuelve en ceros
    (distinto de la vista anual, que lo omite)."""
    response = client.get("/balance?year=2026&month=5", headers=registered_user["headers"])

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["month"] == 5
    assert D(data[0]["total_income"]) == D(0)
    assert D(data[0]["total_expenses"]) == D(0)
    assert D(data[0]["balance"]) == D(0)
    assert data[0]["expenses_by_category"] == []


# ---------------------------------------------------------------------------
# Validaciones y seguridad
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query", [
    "year=2026&month=0",
    "year=2026&month=13",
    "year=2026&month=9&month=13",   # uno válido y uno inválido: se rechaza todo
    "year=2026&month=abc",
    "year=abc",
    "month=9",                      # falta year
])
def test_balance_invalid_params(client, registered_user, query):
    response = client.get(f"/balance?{query}", headers=registered_user["headers"])

    assert response.status_code == 422


def test_balance_requires_token(client):
    assert client.get("/balance?year=2026").status_code == 401