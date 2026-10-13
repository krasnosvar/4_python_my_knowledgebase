# Покрытие тестами: coverage.py

## Что измеряет coverage

`coverage.py` (обычно через плагин `pytest-cov`) отслеживает, какие
строки/ветви кода были выполнены во время прогона тестов. Это метрика
**какой код был затронут тестами**, а не метрика «насколько тесты хороши» —
100% покрытие не означает отсутствие багов, оно лишь показывает, что
каждая строка была выполнена хотя бы раз.

## Запуск

```bash
pip install pytest-cov
pytest --cov=myapp --cov-report=term-missing
```

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
myapp/account.py           42      3    93%   57-59
myapp/services/user.py     30      0   100%
-----------------------------------------------------
TOTAL                      72      3    96%
```

`--cov-report=term-missing` показывает конкретные номера строк, которые не
были выполнены — самый полезный режим для локальной разработки.
`--cov-report=html` генерирует HTML-отчёт с построчной подсветкой.

## Line coverage vs branch coverage

```bash
pytest --cov=myapp --cov-branch --cov-report=term-missing
```

- **Line coverage** — была ли строка выполнена хотя бы раз.
- **Branch coverage** — были ли пройдены **оба** исхода каждого условия
  (условие истинно и условие ложно). Функция может иметь 100% line
  coverage, но так и не проверить один из исходов:

```python
# clamp.py
def clamp_to_zero(n: int) -> int:
    if n < 0:
        n = 0
    return n


# test_clamp.py
def test_negative():
    assert clamp_to_zero(-5) == 0
```

Единственный тест передаёт `-5`: условие `n < 0` истинно, выполняются
**все четыре строки** функции — line coverage 100%. Но случай «условие
ложно» (положительное число, когда строка `n = 0` пропускается) не
проверен ни разу. Line coverage этого не видит, а branch coverage видит:

```text
$ pytest --cov=clamp --cov-report=term-missing
Name       Stmts   Miss  Cover   Missing
clamp.py       4      0   100%

$ pytest --cov=clamp --cov-branch --cov-report=term-missing
Name       Stmts   Miss Branch BrPart  Cover   Missing
clamp.py       4      0      2      1    83%   2->4
```

`2->4` означает: ни разу не выполнился переход со строки 2 (`if`) сразу на
строку 4 (`return`), то есть не проверен исход «условие ложно». Чтобы
закрыть ветку, нужен второй тест, например `clamp_to_zero(7) == 7`.

## Конфигурация

```toml
# pyproject.toml
[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

`fail_under` — CI может завалить сборку, если процент покрытия ниже
порога (`coverage report --fail-under=80` или через `pytest-cov`'s
`--cov-fail-under=80`).

## Как использовать метрику осмысленно

- Высокий процент покрытия — необходимое, но не достаточное условие
  качества тестов: строка может быть «выполнена», но без содержательного
  `assert` на неё.
- Полезнее смотреть на **непокрытые** участки (`--cov-report=term-missing`)
  — они прямо указывают, где тестов не хватает, чем гнаться за конкретным
  процентом.
- Погоня за 100% часто приводит к бессмысленным тестам ради строки покрытия
  (например, тест на `__repr__` без проверки содержимого) — приоритет
  всегда на покрытие бизнес-логики и граничных случаев, а не на метрику
  саму по себе.
