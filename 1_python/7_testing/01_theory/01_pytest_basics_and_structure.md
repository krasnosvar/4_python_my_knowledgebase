# pytest: основы и структура тестов

pytest — де-факто стандарт тестирования в Python: минимум boilerplate,
обычные `assert` без специальных методов, богатая экосистема плагинов.

## Минимальный тест

```python
# test_calculator.py
def add(a: int, b: int) -> int:
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
```

Запуск: `pytest` (или `pytest test_calculator.py`, `pytest -k add_positive`).
Никакого наследования от `TestCase`, никакого `self.assertEqual` — простой
`assert`. pytest переписывает `assert` во время сбора тестов, чтобы при
падении показать подробный diff (значения переменных, а не просто
«AssertionError»).

## Правила обнаружения тестов

pytest ищет тесты по соглашению об именовании, без явной регистрации:

- файлы: `test_*.py` или `*_test.py`;
- функции: `test_*` внутри этих файлов;
- классы: `Test*` (без `__init__`), методы внутри — `test_*`.

```
tests/
  test_calculator.py
  test_user_service.py
  conftest.py          # общие fixtures для всей директории (и поддиректорий)
```

## Структура теста: Arrange-Act-Assert

```python
def test_withdraw_reduces_balance():
    # Arrange — подготовка данных
    account = Account(balance=100)

    # Act — вызов тестируемого поведения
    account.withdraw(30)

    # Assert — проверка результата
    assert account.balance == 70
```

Явное разделение на три части (даже без комментариев) — стандарт
читаемости: тест должен быть понятен без необходимости запускать его в
отладчике.

## Проверка исключений

```python
import pytest

def test_withdraw_raises_on_insufficient_funds():
    account = Account(balance=10)
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(100)
```

`pytest.raises` — контекстный менеджер, который проверяет, что внутри
блока действительно бросается указанное исключение (и опционально что
сообщение соответствует regex через `match`). Тест **упадёт**, если
исключение не будет брошено — это отличает `pytest.raises` от простого
`try/except` с игнорированием.

## Полезные флаги запуска

```bash
pytest                      # запустить все тесты
pytest -v                   # подробный вывод (имя каждого теста)
pytest -x                   # остановиться на первом упавшем тесте
pytest -k "withdraw"        # запустить только тесты, где "withdraw" в имени
pytest --lf                 # запустить только те тесты, что упали в прошлый раз
pytest tests/test_account.py::test_withdraw_reduces_balance  # конкретный тест
```

## Организация проекта

```
myapp/
  __init__.py
  account.py
tests/
  conftest.py
  test_account.py
pytest.ini   (или pyproject.toml с секцией [tool.pytest.ini_options])
```

`pytest.ini`/`pyproject.toml` задают конфигурацию: пути поиска тестов,
маркеры, опции по умолчанию — чтобы не передавать их каждый раз в CLI.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q"
```
