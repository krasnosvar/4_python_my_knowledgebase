# SQL за 5 минут

Остальные уроки темы опираются на базовый SQL: в них сразу встречаются
`SELECT`, `WHERE`, `JOIN`, `PRIMARY KEY`. Этот урок даёт этот минимум с нуля.
Если SQL уже знаком, урок можно пропустить и начать с
[02_relational_model.md](./02_relational_model.md).

## Где всё это запускать

Поднимите стенд из [`../02_examples/`](../02_examples/) и откройте консоль
PostgreSQL (`psql`) внутри контейнера:

```bash
cd ../02_examples
docker compose up -d
docker compose exec postgres psql -U kb_user -d kb_shop
```

Каждая команда SQL заканчивается точкой с запятой `;`. Выйти из `psql` —
команда `\q`. Примеры ниже используют свои учебные таблицы `writers` и
`novels`, чтобы не пересекаться с таблицами из `schema.sql`.

## Таблица, строка, столбец

База данных хранит данные в **таблицах**. Таблица похожа на лист в
электронной таблице:

- **столбец** (column) — одно свойство с фиксированным типом: `name` —
  текст, `year` — число;
- **строка** (row) — одна запись: один писатель, одна книга.

```sql
CREATE TABLE writers (
    id   INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE novels (
    id        INT PRIMARY KEY,
    writer_id INT REFERENCES writers(id),
    title     TEXT NOT NULL,
    year      INT
);
```

- **`PRIMARY KEY`** (первичный ключ) — столбец, по которому строку можно
  однозначно найти: два писателя не могут иметь одинаковый `id`, и `id` не
  может быть пустым.
- **`NOT NULL`** — значение обязано быть заполнено. `NULL` в SQL означает
  «значения нет».
- **`REFERENCES writers(id)`** — внешний ключ: в `novels.writer_id` можно
  записать только `id`, который реально есть в `writers`. Так таблицы
  связываются между собой (подробнее — в
  [02_relational_model.md](./02_relational_model.md)).

## INSERT — добавить строки

```sql
INSERT INTO writers (id, name) VALUES
    (1, 'Пушкин'),
    (2, 'Толстой'),
    (3, 'Чехов');

INSERT INTO novels (id, writer_id, title, year) VALUES
    (1, 1, 'Евгений Онегин',    1833),
    (2, 1, 'Капитанская дочка', 1836),
    (3, 2, 'Война и мир',       1869);
```

У Чехова пока нет ни одной строки в `novels` — это пригодится ниже, когда
дойдём до `LEFT JOIN`.

## SELECT — прочитать строки

```sql
SELECT * FROM novels;                     -- все столбцы, все строки
SELECT title, year FROM novels;           -- только нужные столбцы

SELECT title FROM novels WHERE year < 1850;      -- фильтр строк
SELECT title FROM novels ORDER BY year DESC;     -- сортировка, новые первыми
SELECT title FROM novels ORDER BY year LIMIT 2;  -- только первые 2 строки
```

- `WHERE` оставляет только строки, для которых условие истинно. Условия
  комбинируются через `AND`/`OR`: `WHERE year > 1830 AND writer_id = 1`.
- `ORDER BY` сортирует результат (`ASC` — по возрастанию, по умолчанию;
  `DESC` — по убыванию). Без `ORDER BY` порядок строк **не гарантирован**.
- `LIMIT n` обрезает результат до `n` строк.
- `--` начинает комментарий до конца строки.

## UPDATE и DELETE — изменить и удалить

```sql
UPDATE novels SET year = 1837 WHERE id = 2;   -- изменить одну строку
DELETE FROM novels WHERE id = 3;              -- удалить одну строку
```

Главная ловушка: **без `WHERE` команда применяется ко всем строкам таблицы**.
`DELETE FROM novels;` удалит все книги. Перед `UPDATE`/`DELETE` полезно
сначала выполнить `SELECT` с тем же `WHERE` и убедиться, что выбираются
ровно те строки, что нужно.

Дальше в примерах нужна «Война и мир». Если вы выполнили `DELETE` выше, верните
строку обратно:

```sql
INSERT INTO novels (id, writer_id, title, year) VALUES (3, 2, 'Война и мир', 1869);
```

## JOIN — соединить две таблицы

Название книги лежит в `novels`, а имя автора — в `writers`. Чтобы получить
их вместе, таблицы соединяют по связи `novels.writer_id = writers.id`:

```sql
SELECT w.name, n.title
FROM writers w
JOIN novels n ON n.writer_id = w.id;
```

```
  name   |       title
---------+-------------------
 Пушкин  | Евгений Онегин
 Пушкин  | Капитанская дочка
 Толстой | Война и мир
```

`w` и `n` — короткие псевдонимы таблиц, чтобы не писать имя целиком. `JOIN`
(он же `INNER JOIN`) возвращает только **пары, для которых нашлось
совпадение**. Поэтому Чехова в результате нет: у него нет книг.

`LEFT JOIN` возвращает **все строки левой таблицы**, даже без пары. Там, где
пары нет, столбцы правой таблицы заполняются `NULL`:

```sql
SELECT w.name, n.title
FROM writers w
LEFT JOIN novels n ON n.writer_id = w.id;
```

```
  name   |       title
---------+-------------------
 Пушкин  | Евгений Онегин
 Пушкин  | Капитанская дочка
 Толстой | Война и мир
 Чехов   |                      <- NULL: книг нет, но писатель в выдаче есть
```

## GROUP BY и COUNT — посчитать по группам

`GROUP BY` собирает строки с одинаковым значением в группы, а агрегатная
функция (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) считает что-то по каждой
группе:

```sql
SELECT w.name, COUNT(n.id) AS novels_count
FROM writers w
LEFT JOIN novels n ON n.writer_id = w.id
GROUP BY w.name
ORDER BY novels_count DESC;
```

```
  name   | novels_count
---------+--------------
 Пушкин  |            2
 Толстой |            1
 Чехов   |            0
```

`COUNT(n.id)` считает только не-`NULL` значения, поэтому у Чехова честный
`0`. `AS novels_count` даёт столбцу результата понятное имя.

## Убрать за собой

```sql
DROP TABLE novels;
DROP TABLE writers;
```

`novels` удаляется первой: она ссылается на `writers`, и PostgreSQL не даст
удалить таблицу, на которую ещё кто-то ссылается.

## Проверить понимание

Что вернёт запрос, и почему в нём нет Чехова?

```sql
SELECT w.name, COUNT(n.id)
FROM writers w
JOIN novels n ON n.writer_id = w.id
GROUP BY w.name;
```

<details>
<summary>Разбор</summary>

Вернёт две строки: `Пушкин 2` и `Толстой 1`. Здесь обычный `JOIN`, а он
оставляет только писателей, у которых нашлась хотя бы одна книга. Строка
Чехова отбрасывается ещё до группировки, поэтому до `COUNT` она не доходит
вообще. Чтобы увидеть `Чехов 0`, нужен `LEFT JOIN`, как в примере выше.

</details>

Дальше: [реляционная модель](./02_relational_model.md).
