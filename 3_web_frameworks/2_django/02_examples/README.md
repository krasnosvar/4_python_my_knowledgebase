# Пример: N+1 в Django ORM, до/после

Минимальное Django-приложение `library` (Author, Book, Tag, Review),
которое показывает разницу в количестве SQL-запросов до и после
`select_related`/`prefetch_related`.

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py demo_n_plus_one
```

Первый запуск `demo_n_plus_one` сам создаёт тестовые данные (5 авторов,
10 книг, по 3 отзыва на книгу) — при повторных запусках они переиспользуются.

## Ожидаемый вывод

```
=== select_related: Book -> Author (прямой ForeignKey) ===
book.author.name для каждой книги:
  naive:     11 запрос(ов)
  optimized: 1 запрос(ов)

=== prefetch_related: Book -> Review (обратный ForeignKey) ===
book.reviews.count() для каждой книги:
  naive:     11 запрос(ов)
  optimized: 2 запрос(ов)
```

- **naive**: 1 запрос на список книг + 1 запрос на каждую книгу (10) = 11.
- **select_related**: один запрос с `JOIN` — автор уже в памяти.
- **prefetch_related**: 1 запрос на книги + 1 дополнительный запрос на все
  отзывы разом = 2, независимо от числа книг.

Точные числа могут отличаться на единицу в зависимости от версии Django,
суть — кратный рост числа запросов в naive-варианте пропорционально числу
книг, тогда как в оптимизированном варианте число запросов постоянно.

## Как посмотреть модели в Django Admin (опционально)

```bash
python manage.py createsuperuser
python manage.py runserver
```

Открыть `http://127.0.0.1:8000/admin/`.
