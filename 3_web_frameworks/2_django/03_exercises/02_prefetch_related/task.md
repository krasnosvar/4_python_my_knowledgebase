# Задание 2: N+1 через ManyToMany

Команда `list_books_with_tags.py` печатает для каждой книги список тегов
(`tags` — `ManyToManyField`). Обращение к `book.tags.all()` внутри цикла
без предзагрузки — отдельный запрос на каждую книгу.

## Что сделать

1. Скопировать `command.py` в `../../02_examples/library/management/commands/task02_list_books_tags.py`.
2. Перед запуском добавь тегам хотя бы по одному значению (иначе список
   будет пуст, но запросы всё равно будут выполняться) — например, в
   `python manage.py shell`:

   ```python
   from library.models import Book, Tag
   fiction = Tag.objects.create(name="fiction")
   for book in Book.objects.all():
       book.tags.add(fiction)
   ```

3. Запустить и убедиться, что число запросов равно `1 + количество книг`:

   ```bash
   cd ../../02_examples
   python manage.py task02_list_books_tags
   ```

4. Найти строку с `# TODO` в `command.py` и заменить
   `Book.objects.all()` на вариант с `prefetch_related`.

   Важно: для `ManyToMany` `select_related` не подходит — Django поднимет
   ошибку, потому что такую связь нельзя развернуть в обычный JOIN без
   дублирования строк. Разница объяснена в
   [01_theory/03_select_related_prefetch_related.md](../../01_theory/03_select_related_prefetch_related.md).

5. Запустить снова — число запросов должно стать равным `2`, независимо
   от числа книг.
