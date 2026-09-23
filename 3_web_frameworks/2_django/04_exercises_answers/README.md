# Ответы: найди и исправь N+1

Готовые решения для [../03_exercises](../03_exercises/). Каждый `command.py`
здесь — уже исправленная версия, без `TODO`.

- [task_01_select_related](./task_01_select_related/) — исправлено через
  `select_related("author")`.
- [task_02_prefetch_related](./task_02_prefetch_related/) — исправлено
  через `prefetch_related("tags")`.

Проверить решение можно, скопировав `command.py` в
`../02_examples/library/management/commands/` (как описано в
`task.md` каждого задания) и сравнив вывод "Запросов выполнено" с числом
из комментария в файле.
