-- Задание 1b: прочитать и объяснить план EXPLAIN ANALYZE
--
-- Столбец orders.order_date не индексирован. Запрос выбирает заказы за
-- последнюю неделю (относительно текущей даты).

EXPLAIN ANALYZE
SELECT * FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';

-- TODO: запишите здесь текстом (в комментариях) ответы на вопросы:
--
-- 1. Какой узел сканирования выбрал планировщик (Seq Scan / Index Scan /
--    Bitmap Heap Scan / другой)? Почему именно этот, а не другой -- с
--    учётом того, сколько строк (примерно) должно попасть в диапазон
--    последних 7 дней из ~700 дней разброса значений order_date?
--
--    Ваш ответ:
--    ...
--
-- 2. Что означают в выводе первое и второе число в cost=X..Y и в
--    actual time=X..Y? Совпадают ли оценка планировщика (rows= в cost-части)
--    и фактическое количество строк (rows= в actual-части)? Если нет --
--    это сигнал к чему?
--
--    Ваш ответ:
--    ...
--
-- 3. TODO: создайте индекс на order_date, выполните ANALYZE orders,
--    и повторите EXPLAIN ANALYZE того же запроса. Изменился ли план?
--    Запишите вывод.
--
--    CREATE INDEX ... ON orders (...);
--    ANALYZE orders;

EXPLAIN ANALYZE
SELECT * FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';

--    Ваш ответ:
--    ...
