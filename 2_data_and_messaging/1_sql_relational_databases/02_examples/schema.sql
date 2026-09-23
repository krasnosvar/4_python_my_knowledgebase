-- Схема для примеров из 02_examples.
-- Домен намеренно смешанный: разные таблицы иллюстрируют разные темы теории.

-- 1. Счета -- пример ACID / транзакций (банковский перевод)
CREATE TABLE IF NOT EXISTS accounts (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL UNIQUE,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts (name, balance) VALUES
    ('Alice', 1000.00),
    ('Bob',    500.00),
    ('Carol',  250.00)
ON CONFLICT (name) DO NOTHING;

-- 2. Авторы и книги -- пример SQLAlchemy ORM и проблемы N+1
CREATE TABLE IF NOT EXISTS authors (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id             SERIAL PRIMARY KEY,
    author_id      INT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    title          VARCHAR(255) NOT NULL,
    published_year INT
);

INSERT INTO authors (id, name) VALUES
    (1, 'Лев Толстой'),
    (2, 'Фёдор Достоевский'),
    (3, 'Антон Чехов'),
    (4, 'Александр Пушкин'),
    (5, 'Николай Гоголь')
ON CONFLICT (id) DO NOTHING;

INSERT INTO books (author_id, title, published_year) VALUES
    (1, 'Война и мир', 1869),
    (1, 'Анна Каренина', 1877),
    (2, 'Преступление и наказание', 1866),
    (2, 'Идиот', 1869),
    (2, 'Братья Карамазовы', 1880),
    (3, 'Вишнёвый сад', 1904),
    (3, 'Чайка', 1896),
    (4, 'Евгений Онегин', 1833),
    (5, 'Мёртвые души', 1842)
ON CONFLICT DO NOTHING;

SELECT setval('authors_id_seq', (SELECT max(id) FROM authors));
SELECT setval('books_id_seq', (SELECT max(id) FROM books));

-- 3. Клиенты и заказы -- пример индексов и EXPLAIN ANALYZE (нужен объём данных)
CREATE TABLE IF NOT EXISTS customers (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    city  VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id          SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    status      VARCHAR(20) NOT NULL,
    order_date  DATE NOT NULL,
    total       NUMERIC(10, 2) NOT NULL
);

-- Наполняем 2 000 клиентов и 200 000 заказов через generate_series,
-- чтобы EXPLAIN ANALYZE показывал реальную разницу Seq Scan / Index Scan.
-- Намеренно НЕ создаём индекс на orders.customer_id сразу -- это делает
-- скрипт 03_indexes_and_explain.py, чтобы показать эффект "до/после".
INSERT INTO customers (name, email, city)
SELECT
    'Customer ' || i,
    'customer' || i || '@example.com',
    (ARRAY['Moscow', 'Saint Petersburg', 'Kazan', 'Novosibirsk', 'Yekaterinburg'])[1 + (i % 5)]
FROM generate_series(1, 2000) AS i
ON CONFLICT DO NOTHING;

INSERT INTO orders (customer_id, status, order_date, total)
SELECT
    1 + (random() * 1999)::int,
    (ARRAY['new', 'paid', 'shipped', 'delivered', 'cancelled'])[1 + (random() * 4)::int],
    CURRENT_DATE - (random() * 700)::int,
    round((random() * 500 + 5)::numeric, 2)
FROM generate_series(1, 200000) AS i
WHERE NOT EXISTS (SELECT 1 FROM orders LIMIT 1);

-- 4. Товары -- пример пессимистичной и оптимистичной блокировки
CREATE TABLE IF NOT EXISTS products (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(150) NOT NULL,
    stock   INT NOT NULL CHECK (stock >= 0),
    version INT NOT NULL DEFAULT 1
);

INSERT INTO products (name, stock) VALUES
    ('Клавиатура', 50),
    ('Мышь', 100),
    ('Монитор', 20)
ON CONFLICT DO NOTHING;

ANALYZE;
