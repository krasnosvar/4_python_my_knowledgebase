# Тема 04. Ветвления и циклы

Главное правило Python — отступы определяют блок кода. `if`/`elif`/`else`,
truthy/falsy значения, цикл `for` (перебор элементов, не счётчик), `range()`,
цикл `while`, `break` и `continue`.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_control_flow_basics.md](./01_theory/01_control_flow_basics.md) —
    отступы как блок кода, `if`/`elif`/`else`, truthy/falsy, `for`,
    `range()`, `while`, `break`/`continue`.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_grade_calculator.py](./02_examples/01_grade_calculator.py) —
    классификация баллов через `if`/`elif`/`else` внутри `for`, поиск
    первого совпадения через `break`, сумма через `continue`.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой `PASS`/`FAIL`:
  - `01_classify_number` — три ветки `if`/`elif`/`else`.
  - `02_sum_even_numbers` — цикл `for` с пропуском через `continue`.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию:
   [01_control_flow_basics.md](./01_theory/01_control_flow_basics.md).
2. Запустите пример:
   ```bash
   python 02_examples/01_grade_calculator.py
   ```
3. Выполните задачи в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/01_classify_number.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

Дальше: [функции](../05_functions_basics/).
