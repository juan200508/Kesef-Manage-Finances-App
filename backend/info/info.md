## Modelo de datos
 
| Tabla | Campos principales | Relación |
| --- | --- | --- |
| users | id, email, hashed_password, full_name, created_at | — |
| categories | id, user_id (FK), name, created_atm is_global | pertenece a users |
| movements | id, user_id (FK), category_id (FK), movement_type, amount, description, movement_date, created_at | pertenece a users y categories |
| monthly_incomes | id, user_id (FK), year, month, amount, source, created_at | pertenece a users, admite varias fuentes por mes |
 
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