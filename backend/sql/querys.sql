-- Meses que tienen movimientos
SELECT EXTRACT(MONTH FROM mov.movement_date) AS month 
FROM movements as mov
WHERE mov.user_id = '8bba8798-9425-4d55-98b6-58b6ae3acaaa' 
  AND EXTRACT(YEAR FROM mov.movement_date) = 2026
UNION 
SELECT moi.month
FROM monthly_incomes moi
WHERE moi.user_id = '8bba8798-9425-4d55-98b6-58b6ae3acaaa' 
  AND moi.year = 2026
ORDER BY month DESC;


-- Total de ingresos por mes
SELECT COALESCE(SUM(amount), 0) AS total_incomes
FROM monthly_incomes 
WHERE user_id = '8bba8798-9425-4d55-98b6-58b6ae3acaaa' 
  AND year = 2026
  AND month = 7;


-- Total de gastos por categoría
SELECT 
  c.id AS category_id, 
  c.name AS category_name, 
  SUM(m.amount) AS total
FROM movements AS m
JOIN categories c ON c.id = m.category_id
WHERE m.user_id = '8bba8798-9425-4d55-98b6-58b6ae3acaaa'
  AND EXTRACT(YEAR FROM m.movement_date) = 2026
  AND EXTRACT(MONTH FROM m.movement_date) = 9
GROUP BY c.id, c.name
ORDER BY total DESC;


-- Total de gastos por mes
SELECT 
  EXTRACT(MONTH FROM movement_date) AS month,
  EXTRACT(YEAR  FROM movement_date) AS year,
  SUM(amount)
FROM movements
WHERE user_id = '8bba8798-9425-4d55-98b6-58b6ae3acaaa'
  AND EXTRACT(YEAR  FROM movement_date) = 2026
  AND EXTRACT(MONTH FROM movement_date) = 9
GROUP BY month, year;
  