# Задание 1: N+1 через прямой ForeignKey

Команда `list_books_with_tags_count.py` печатает для каждой книги имя её
автора. Она использует `Book.objects.all()` без предзагрузки, поэтому
каждое обращение к `book.author.name` внутри цикла — отдельный SQL-запрос.

## Что сделать

1. Скопировать `command.py` в `../../02_examples/library/management/commands/task01_list_books.py`.
2. Запустить и убедиться, что число запросов равно `1 + количество книг`:

   ```bash
   cd ../../02_examples
   python manage.py task01_list_books
   ```

3. Найти строку с `# TODO` в `command.py` и заменить
   `Book.objects.all()` на вариант с `select_related`.
4. Запустить снова — число запросов должно стать равным `1`, независимо от
   числа книг.

Проверка использует `CaptureQueriesContext` — как именно, см.
[01_theory/01_lazy_querysets.md](../../01_theory/01_lazy_querysets.md).
