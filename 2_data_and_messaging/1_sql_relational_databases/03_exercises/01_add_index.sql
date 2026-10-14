-- Задание 01: добавить индекс под медленный фильтр
--
-- Запрос ниже фильтрует customers по email. Столбец email нигде не
-- индексирован (кроме первичного ключа id на customers.id), поэтому
-- PostgreSQL вынужден читать всю таблицу (Seq Scan), даже если совпадает
-- всего одна строка.

EXPLAIN ANALYZE
SELECT * FROM customers WHERE email = 'customer1500@example.com';

-- TODO: напишите здесь CREATE INDEX, устраняющий полное сканирование
-- по этому запросу.
--
-- CREATE INDEX ... ON customers (...);


-- TODO: выполните EXPLAIN ANALYZE ещё раз (тот же запрос, что выше) и
-- убедитесь, что план сменился на Index Scan / Index Only Scan.

EXPLAIN ANALYZE
SELECT * FROM customers WHERE email = 'customer1500@example.com';
