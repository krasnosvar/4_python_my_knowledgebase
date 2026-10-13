# Тема 05. Функции

Объявление через `def`, параметры и аргументы, `return`, значения по
умолчанию, позиционные и именованные аргументы, docstring, аннотации типов.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_functions_basics.md](./01_theory/01_functions_basics.md) — `def`,
    параметры/аргументы, `return`, значения по умолчанию, позиционные и
    именованные аргументы, docstring, аннотации типов.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_temperature_converter.py](./02_examples/01_temperature_converter.py) —
    несколько функций, параметр со значением по умолчанию.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой `PASS`/`FAIL`:
  - `01_is_palindrome` — функция с одним параметром и циклом внутри.
  - `02_apply_discount` — параметр со значением по умолчанию.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию:
   [01_functions_basics.md](./01_theory/01_functions_basics.md).
2. Запустите пример:
   ```bash
   python 02_examples/01_temperature_converter.py
   ```
3. Выполните задачи в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/01_is_palindrome.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

## Когда двигаться дальше

Если ты можешь объявить функцию с параметром по умолчанию и прочитать
её аннотации типов — переходи к теме
[06_exceptions](../06_exceptions/README.md): что делать, когда код
падает с ошибкой.
