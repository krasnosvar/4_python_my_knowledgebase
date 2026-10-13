# Параметризация тестов

`@pytest.mark.parametrize` — один тест на набор входных данных вместо
копирования тела теста под каждый случай.

## Базовый синтаксис

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

pytest запустит функцию три раза, подставляя каждую строку кортежа как
`a`, `b`, `expected`. В выводе каждый запуск виден отдельно
(`test_add[2-3-5]`, `test_add[-1-1-0]`) — падение одного набора данных не
маскирует остальные.

## Именование тестовых случаев (ids)

```python
@pytest.mark.parametrize("value, expected", [
    (0, False),
    (1, True),
    (-5, True),
], ids=["zero", "positive", "negative"])
def test_is_truthy(value, expected):
    assert bool(value) == expected
```

Без `ids` pytest генерирует идентификатор по значениям параметров — для
сложных объектов (не строк/чисел) он может быть нечитаемым (`test_x[obj0]`).
Явные `ids` делают вывод `pytest -v` понятным без чтения кода теста.

## Ожидаемые исключения через parametrize

```python
@pytest.mark.parametrize("amount, expected_exception", [
    (-10, ValueError),
    (10_000, InsufficientFundsError),
])
def test_withdraw_errors(account, amount, expected_exception):
    with pytest.raises(expected_exception):
        account.withdraw(amount)
```

## Комбинация нескольких parametrize (декартово произведение)

```python
@pytest.mark.parametrize("currency", ["USD", "EUR"])
@pytest.mark.parametrize("amount", [10, 100])
def test_convert(amount, currency):
    ...  # запустится 4 раза: все комбинации amount x currency
```

Несколько `parametrize` над одной функцией перемножаются — удобно для
матрицы независимых параметров, но при большом числе комбинаций тестов
становится много (иногда лучше явно вернуться к одному списку кортежей).

## Параметризация fixture

```python
@pytest.fixture(params=["sqlite", "postgres"])
def db_backend(request):
    return create_backend(request.param)

def test_query_works_on_all_backends(db_backend):
    assert db_backend.query("SELECT 1") == 1
```

В отличие от `parametrize` над тестом, параметризованная fixture
переиспользуется во **всех** тестах, которые её запрашивают — каждый такой
тест автоматически прогоняется для каждого значения `params`.

## Когда использовать

- Одна и та же логика теста, разные входные/ожидаемые значения —
  `parametrize` вместо копипасты нескольких похожих `test_*` функций.
- Разные бэкенды/конфигурации, которые должны проходить одинаковый набор
  тестов — параметризованная fixture.
- Не злоупотребляйте: если тестовые случаи требуют существенно разной
  подготовки/проверки — возможно, это разные тесты, а не параметры одного.
