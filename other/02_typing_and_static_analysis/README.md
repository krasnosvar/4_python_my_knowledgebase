# Тема 02. Типизация и статический анализ (type hints, mypy, ruff, black)

## Зачем этот раздел

Запись вида `def f(x: int) -> str:` встречается почти во всех примерах
репозитория. Здесь разобрано, что означают эти аннотации типов (коротко:
Python их при запуске не проверяет, это подсказки для людей и
инструментов), как `mypy` находит по ним ошибки до запуска кода и как
линтеры и форматтеры (`ruff`, `black`) держат код единообразным. После
темы вы сможете читать аннотации в любом разделе репозитория и находить
ошибки типов до запуска кода.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — синтаксис аннотаций с версиями Python, mypy, ruff, black.

## Что нужно знать заранее

- Функции и базовые аннотации типов — тема про функции в
  [1_python_fundamentals](../../1_python/1_python_fundamentals/).
- Для `Protocol` и дженериков из теории полезно знать классы
  ([3_oop](../../1_python/3_oop/)), но это не обязательно для основной части.
- Виртуальное окружение, чтобы поставить `mypy`/`ruff` —
  [01_environments_and_packaging](../01_environments_and_packaging/README.md).

## Структура

- **[01_theory/](./01_theory/)** — теория, по порядку:
  - [01_type_hints_and_mypy.md](./01_theory/01_type_hints_and_mypy.md) —
    почему аннотации сами ничего не проверяют, синтаксис и модуль
    `typing`, запуск `mypy`, что он ловит и что нет, неочевидные ловушки.
  - [02_linters_formatters.md](./01_theory/02_linters_formatters.md) —
    зачем статический анализ помимо типов, `ruff`, `black`, типичный набор
    для нового проекта, `pre-commit`.
- **[02_examples/](./02_examples/)** —
  [untyped_example.py](./02_examples/untyped_example.py) и
  [typed_example.py](./02_examples/typed_example.py) бок о бок,
  [pyproject.toml](./02_examples/pyproject.toml) с настройками mypy/ruff.

> **Оба примера намеренно падают с `TypeError` при запуске через
> `python3`** — в них специально передана строка вместо числа. Это не
> поломка: так видно, что аннотации сами по себе ничего не проверяют.
> Смысл в сравнении — для `typed_example.py` команда `mypy` находит ту же
> ошибку до запуска.

Упражнений нет — это справочный материал.

## Как проходить

- Встретили непонятную аннотацию (`list[str]`, `int | None`, `Protocol`) —
  загляните в `01_type_hints_and_mypy.md`.
- Подключаете проверки к своему проекту — `02_linters_formatters.md` и
  `02_examples/pyproject.toml`.
- Чтобы увидеть mypy в деле (после `pip install mypy`, см.
  [01_environments_and_packaging](../01_environments_and_packaging/README.md)):
  ```bash
  mypy 02_examples/typed_example.py
  ```

## Когда двигаться дальше

Когда можете прочитать аннотацию вида `dict[str, list[int]] | None`,
запустить `mypy` на своём файле и понять его сообщение об ошибке —
возвращайтесь к основному курсу; к `02_linters_formatters.md` — при
настройке собственного проекта.

[К разделу other](../README.md).
