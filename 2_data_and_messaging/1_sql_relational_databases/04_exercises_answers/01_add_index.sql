-- Решение 01: добавить индекс под медленный фильтр

EXPLAIN ANALYZE
SELECT * FROM customers WHERE email = 'customer1500@example.com';
-- До индекса: Seq Scan on customers (cost=0.00..44.00 rows=1 ...)
-- 2000 строк читаются целиком ради одного совпадения.

CREATE INDEX idx_customers_email ON customers (email);

-- Обычный B-Tree индекс -- email используется только для точного
-- сравнения (=) в этом запросе, диапазоны/сортировка тут не нужны,
-- поэтому Hash-индекс тоже подошёл бы, но B-Tree -- универсальный выбор
-- по умолчанию и не имеет минусов Hash (нет сортировки/диапазонов --
-- это не нужно сейчас, но не помешает в будущем).

EXPLAIN ANALYZE
SELECT * FROM customers WHERE email = 'customer1500@example.com';
-- После индекса: Index Scan using idx_customers_email on customers
-- (cost=0.29..8.30 rows=1 ...), actual time на порядки меньше.
-- Почему это работает: индекс хранит отсортированные значения email
-- вместе со ссылкой на строку (ctid), поэтому PostgreSQL находит нужную
-- строку за O(log n) сравнений вместо чтения всех 2000 строк подряд.
