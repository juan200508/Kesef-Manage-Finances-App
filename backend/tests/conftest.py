import os
from pathlib import Path
from uuid import UUID
from datetime import datetime

import pytest
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env.test", override=True)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.category import Category
from app.models.movement import Movement, MovementType
from app.models.monthly_income import MonthlyIncome, MonthlyIncomeSource
from app.core.rate_limit import limiter

TEST_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True, pool_recycle=300 )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crea todas las tablas de pruebas al inicio de todas la sesiones de test y las elimina al terminar
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


#Una sesión de base de datos para que el TEST pueda consultar/insertar directamente, fuera de las peticiones HTTP (ej. para sembrar datos).
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()


# Cliente HTTP que simula las peticiones a la API 
@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Corre automáticamente después de cada sesión de pruebas eliminando las tablas para que el siguiente  test siempre inicie limpio 
@pytest.fixture(autouse=True)
def clean_database():
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


# Siembra la categoría global 'Otros', necesaria para probar la reasignación al eliminar una categoría personal.
@pytest.fixture()
def otros_category(db_session):
    category = Category(name="Otros", user_id=None, is_global=True)
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


# Crea una categoría personal para la gestión de movimientos.
@pytest.fixture()
def else_category(db_session, other_user):
    category = Category(
        name="Vehículo 2",
        user_id=UUID(other_user["id"]),
        is_global=False
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


# Crea una categoría personal para la gestión de movimientos. 
@pytest.fixture()
def personal_category(db_session, registered_user):
    category = Category(
        name="Vehículo",
        user_id=UUID(registered_user["id"]),
        is_global=False
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


# Crean movimientos de prueba para los test
@pytest.fixture()
def movements(db_session, registered_user, personal_category):
    movements = [
        Movement(
            user_id=UUID(registered_user["id"]),
            category_id=personal_category.id,
            movement_type=MovementType.PAGO,
            amount=amount,
            description=f"Movement {i}",
            movement_date=datetime(2026, 9, day)
        )
        for i, (amount, day) in enumerate([(300000, 3), (220000, 12), (250000, 25)], start=1)
    ]
    db_session.add_all(movements)
    db_session.commit()
    return movements


# Crea ingresos de prueba para los test
@pytest.fixture()
def incomes(db_session, registered_user):
    incomes = [
        MonthlyIncome(
            user_id=UUID(registered_user["id"]),
            year=2026,
            month=9,
            amount=amount,
            source=source,
            description=f"Income {i}"
        )
        for i, (amount, source) in enumerate(
            [
                (3500000, MonthlyIncomeSource.SALARIO), 
                (1000000, MonthlyIncomeSource.FREELANCE), 
                (500000, MonthlyIncomeSource.CONSIGNACIONES)
            ],
            start=1
        )
    ]
    db_session.add_all(incomes)
    db_session.commit()
    return incomes


# Crea un movimiento de manera manual llamado la función create_movement()
@pytest.fixture()
def create_movement(db_session):
    def _create(user_data, category, amount, movement_date, movement_type=MovementType.COMPRA):
        mov = Movement(
            user_id=UUID(user_data["id"]),
            category_id=category.id,
            movement_type=movement_type,
            amount=amount,
            movement_date=movement_date
        )
        db_session.add(mov)
        db_session.commit()
        db_session.refresh(mov)
        return mov
    return _create


# Crea un ingreso de manera manual llamado la función create_income()
@pytest.fixture()
def create_income(db_session):
    def _create(user_data, year, month, amount, source, description=None):
        inc = MonthlyIncome(
            user_id=UUID(user_data["id"]),
            year=year,
            month=month,
            amount=amount,
            source=source,
            description=description
        )
        db_session.add(inc)
        db_session.commit()
        db_session.refresh(inc)
        return inc
    return _create


# Registra un usuario de prueba, hace login, y devuelve sus datos junto con los headers de autenticación ya listos para usar.
@pytest.fixture()
def registered_user(client):
    user_data = {
        "email": "test@kesef.com",
        "password": "testpass12345*",
        "full_name": "Usuario de prueba",
    }
    register_response = client.post("/register", json=user_data)
    user_id = register_response.json()["id"]

    login_response = client.post(
        "/login", json={"email": user_data["email"], "password": user_data["password"]}
    )
    token = login_response.json()["access_token"]

    return {
        "id": user_id,
        "email": user_data["email"], 
        "headers": {"Authorization": f"Bearer {token}"}
    }


# Un segundo usuario, para probar que cada uno solo ve/edita lo suyo.
@pytest.fixture()
def other_user(client):
    user_data = {
        "email": "other@kesef.com",
        "password": "otherpass123456*",
        "full_name": "Otro usuario de prueba",
    }
    register_response = client.post("/register", json=user_data)
    user_id = register_response.json()["id"]

    login_response = client.post(
        "/login", json={"email": user_data["email"], "password": user_data["password"]}
    )
    token = login_response.json()["access_token"]

    return {
        "id": user_id,
        "email": user_data["email"], 
        "headers": {"Authorization": f"Bearer {token}"}}


# Apaga el rate limiting en todos los tests para que registered_user, other_user
# y el resto de la suite no choquen con el 429. Solo test_rate_limit.py lo enciende.
@pytest.fixture(autouse=True)
def disable_rate_limit():
    limiter.enabled = False
    yield
    limiter.reset()