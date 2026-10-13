# Тема 06. Исключения

Что происходит, когда код падает, как читать traceback, как перехватить
ожидаемую ошибку через `try`/`except` и как выбросить свою через `raise`.
Без этой темы невозможно читать код дальше в репозитории: `try`/`except`
встречается почти в каждом следующем разделе.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_exceptions.md](./01_theory/01_exceptions.md) — traceback, частые
    встроенные исключения, `try`/`except`, почему голый `except` вреден,
    `as e`, `else`/`finally`, цикл проверки ввода, `raise` и повторный
    `raise`.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_safe_calculator.py](./02_examples/01_safe_calculator.py) — деление
    строк из «ввода» с обработкой `ValueError`/`ZeroDivisionError` и своя
    проверка через `raise`.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой `PASS`/`FAIL`:
  - `01_safe_int` — перехват `ValueError` и значение по умолчанию.
  - `02_check_age` — собственная проверка через `raise ValueError`.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию:
   [01_exceptions.md](./01_theory/01_exceptions.md).
2. Запустите пример:
   ```bash
   python 02_examples/01_safe_calculator.py
   ```
3. Выполните задачи в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/01_safe_int.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

## Когда двигаться дальше

Если ты можешь по traceback найти строку с ошибкой, перехватить
конкретный тип исключения и объяснить, почему голый `except:` опасен —
переходи к теме [07_modules_and_imports](../07_modules_and_imports/README.md).
