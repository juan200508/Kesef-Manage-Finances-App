## Modelo de datos
 
| Tabla | Campos principales | Relación |
| --- | --- | --- |
| users | id, email, hashed_password, full_name, created_at, update_at | — |
| categories | id, user_id (FK), name, created_at, update_at, is_global | pertenece a users |
| movements | id, user_id (FK), category_id (FK), movement_type, amount, description, movement_date, created_at, update_at | pertenece a users y categories |
| monthly_incomes | id, user_id (FK), year, month, amount, source, description, created_at, update_at | pertenece a users, admite varias fuentes por mes |
 
`movement_type` está restringido a: COMPRA, CONSIGNACION, TRANSFERENCIA, RETIRO, PAGO, OTRO. Todos los IDs son UUID generados por PostgreSQL (`gen_random_uuid()`).

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py          (auth: hash + JWT)
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── movement.py
│   │   └── monthly_income.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── movement.py
│   │   └── monthly_income.py
│   └── api/
│       ├── deps.py              (get_current_user)
│       └── routers/
│           ├── auth.py
│           ├── categories.py
│           ├── movements.py
│           └── incomes.py
├── sql/
│   └── schema.sql
├── .env
├── .env.example
└── requirements.txt
```

# ROAD MAP PARA TERMINAL EL BACKEND
1. Pruebas automatizadas con pytest, incluye todas las pruebas funcionales.
2. Documentación con swagger y con un read.me en la raíz del proyecto
3. Rate limiting para controlar desde el código el número de peticiones que un usuario puede enviar en un determinado tiempo

# test_movements.py
Crear movimiento exitoso (con una categoría propia, y también con una global, para confirmar que ambas son válidas).
Crear movimiento con category_id inexistente o ajeno → 404.
Crear movimiento con movement_type inválido (algo fuera del Enum) → 422.
Listar — confirmar aislamiento (un usuario no ve movimientos de otro).
Filtros: por movement_type, por category_id (lista), por rango de fechas — al menos un test por cada uno.
Actualización parcial (PUT con un solo campo) — confirmar que los demás campos no cambiaron.
Confirmar que created_at y movement_date no cambian en un PUT, pero updated_at sí (el bug que corregiste hace un tiempo — este test te protege de que vuelva a pasar).

# test_monthly_incomes.py
Crear ingreso exitoso.
Crear con source inválido (fuera del Enum) → 422.
Crear con month fuera de rango (13, 0) → 422.
Confirmar que sí se pueden crear dos ingresos con el mismo year+month+source (tu decisión deliberada de no aplicar unicidad) — este test documenta esa decisión de diseño.
Filtros por year y month.
Aislamiento entre usuarios.

# test_balance.py (el más interesante, porque depende de datos previos)
Balance de un mes sin ningún dato → todo en cero, sin error.
Balance con ingresos y movimientos de prueba → confirmar que balance = total_income - total_expenses matemáticamente.
Confirmar que expenses_by_category suma exactamente igual a total_expenses.
GET /balance?year=X (sin mes) → confirmar que devuelve una lista con los meses que tienen datos, y que un mes sin datos no aparece.
GET /balance?year=X&month=Y → confirma que devuelve una lista de un solo elemento.

# Prueba
def test_balance_two_months(client, registered_user, personal_category, create_movement):
    create_movement(personal_category, 10000, datetime(2026, 8, 10))
    create_movement(personal_category, 25000, datetime(2026, 9, 10))
    create_movement(personal_category, 5000, datetime(2026, 9, 20))

    response = client.get("/balance?year=2026", headers=registered_user["headers"])

    assert len(response.json()) == 2   # agosto y septiembre