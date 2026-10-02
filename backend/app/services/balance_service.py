from uuid import UUID

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.monthly_income import MonthlyIncome
from app.models.movement import Movement
from app.schemas.balance import CategoryExpenseBreakdown, MonthlyBalanceOut


def get_monthly_balance(
        db: Session,
        user_id: UUID,
        year: int,
        month: int
):
    """ Calcula el balance del mes específico: Suma de ingresos, suma de gastos (desglose por categorías) y la diferencia entre ambos"""

    # Total de ingresos por mes
    total_income = (
        db.query(func.coalesce(func.sum(MonthlyIncome.amount), 0))
        .filter(
            MonthlyIncome.user_id == user_id,
            MonthlyIncome.year == year,
            MonthlyIncome.month == month
        )
        .scalar()
    )

    # Gastos agrupados por categoría 
    category_rows = (
        db.query(
            Category.id,
            Category.name,
            func.sum(Movement.amount).label("total")
        )
        .join(Category, Category.id == Movement.category_id)
        .filter(
            Movement.user_id == user_id,
            extract("year", Movement.movement_date) == year,
            extract("month", Movement.movement_date) == month
        )
        .group_by(Category.id, Category.name)
        .order_by(func.sum(Movement.amount).desc())
        .all()
    )
    expenses_by_category = [
        CategoryExpenseBreakdown(
            category_id=row.id,
            category_name=row.name,
            total=row.total
        )
        for row in category_rows
    ]

    # Total de gastos
    """
    total_expenses = (
        db.query(
            extract("month", Movement.movement_date).label("month"),
            extract("year", Movement.movement_date).label("year"),
            func.sum(Movement.amount).label("total")
        )
        .filter(
            Movement.user_id == user_id,
            extract("month", Movement.movement_date) == month,
            extract("year", Movement.movement_date) == year
        )
    )
    """
    # o
    total_expenses = sum((item.total for item in expenses_by_category), start=0)

    return MonthlyBalanceOut(
        year=year,
        month=month,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=total_income - total_expenses,
        expenses_by_category=expenses_by_category   
    )


def get_yearly_balance(
        db: Session,
        user_id: UUID,
        year: int
):
    """ Devuelve el balance de un mes del año que tenga movimientos, ya sean ingresos o gastos. """

    movement_months = db.query(
        extract("month", Movement.movement_date).label("month")
    ).filter(
        Movement.user_id == user_id,
        extract("year", Movement.movement_date) == year    
    )
    income_months = db.query(
        MonthlyIncome.month.label("month")
    ).filter(
        MonthlyIncome.user_id == user_id,
        MonthlyIncome.year == year
    )

    months_with_data = movement_months.union(income_months).all()

    # Se ordena descendente, el más reciente primero
    distinct_months = sorted({int(row.month) for row in months_with_data}, reverse=True)

    return [
        get_monthly_balance(db=db, user_id=user_id, month=month, year=year)
        for month in distinct_months
    ]
