-- Habilita la generación de UUIDs (gen_random_uuid) en PostgreSQL
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- Tabla: users
-- ============================================
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================
-- Tabla: categories (categorías de gastos)
-- ============================================
CREATE TABLE categories (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (user_id, name)
);

-- ============================================
-- Tabla: movements (gastos registrados)
-- ============================================
CREATE TABLE movements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id     UUID REFERENCES categories(id) ON DELETE SET NULL,
    movement_type   VARCHAR(20) NOT NULL CHECK (
                        movement_type IN (
                            'COMPRA', 'TRANSFERENCIA',
                            'RETIRO', 'PAGO', 'OTRO'
                        )
                    ),
    amount          NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    description     VARCHAR(255),
    movement_date   DATE NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);

-- ============================================
-- Tabla: monthly_incomes (ingresos declarados por mes, admite varias fuentes)
-- ============================================
CREATE TABLE monthly_incomes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    year        INT NOT NULL CHECK (year >= 2000),
    month       INT NOT NULL CHECK (month BETWEEN 1 AND 12),
    amount      NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    source      VARCHAR(100),
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- Índices para acelerar los queries de las pantallas principales
CREATE INDEX idx_categories_user_id            ON categories(user_id);
CREATE INDEX idx_movements_user_id             ON movements(user_id);
CREATE INDEX idx_movements_category_id         ON movements(category_id);
CREATE INDEX idx_movements_movement_date       ON movements(movement_date);
CREATE INDEX idx_monthly_incomes_user_period   ON monthly_incomes(user_id, year, month);