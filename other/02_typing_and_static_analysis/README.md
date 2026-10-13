# Типизация и статический анализ (type hints, mypy, ruff, black)

Запись вида `def f(x: int) -> str:` встречается почти во всех примерах
репозитория. Здесь разобрано, что означают эти аннотации типов (коротко:
Python их при запуске не проверяет, это подсказки для людей и
инструментов), как `mypy` находит по ним ошибки до запуска кода и как
линтеры и форматтеры (`ruff`, `black`) держат код единообразным.

## Структура

- **[01_theory/](./01_theory/)** — теория, по порядку:
  - [01_type_hints_and_mypy.md](./01_theory/01_type_hints_and_mypy.md) —
    почему аннотации сами ничего не проверяют, синтаксис и модуль
    `typing`, запуск `mypy`, что он ловит и что нет, неочевидные ловушки.
  - [02_linters_formatters.md](./01_theory/02_linters_formatters.md) —
    зачем статический анализ помимо типов, `ruff`, `black`, типичный набор
    для нового проекта, `pre-commit`.
- **[02_examples/](./02_examples/)** — `untyped_example.py` и
  `typed_example.py` бок о бок, `pyproject.toml` с настройками mypy/ruff.

Упражнений нет — это справочный материал.

## Как использовать

- Встретили непонятную аннотацию (`list[str]`, `int | None`, `Protocol`) —
  загляните в `01_type_hints_and_mypy.md`.
- Подключаете проверки к своему проекту — `02_linters_formatters.md` и
  `02_examples/pyproject.toml`.
- Чтобы увидеть mypy в деле (после `pip install mypy`, см.
  [01_environments_and_packaging](../01_environments_and_packaging/README.md)):
  ```bash
  mypy 02_examples/typed_example.py
  ```

[К разделу other](../README.md).
