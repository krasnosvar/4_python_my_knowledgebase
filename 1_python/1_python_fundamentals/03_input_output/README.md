# Тема 03. Ввод и вывод

`print()` и его параметры `sep`/`end`, `input()` и то, что он всегда
возвращает строку, комментарии `#`, форматирование чисел в f-строках.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_input_output.md](./01_theory/01_input_output.md) — `print()`,
    `sep`/`end`, `input()`, комментарии, спецификаторы формата в f-строках.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_greeting_cli.py](./02_examples/01_greeting_cli.py) — небольшой
    интерактивный скрипт, который спрашивает имя и возраст.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой `PASS`/`FAIL`:
  - `01_build_greeting` — сборка строки из нескольких значений разных типов.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию:
   [01_input_output.md](./01_theory/01_input_output.md).
2. Запустите пример (он спросит ваше имя и возраст):
   ```bash
   python 02_examples/01_greeting_cli.py
   ```
3. Выполните задачу в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/01_build_greeting.py
   ```
4. Сверьтесь с эталонным ответом в `04_exercises_answers/`.

Дальше: [ветвления и циклы](../04_control_flow_basics/).
