# unittest vs pytest

`unittest` — часть стандартной библиотеки (вдохновлён JUnit), `pytest` —
сторонняя библиотека, ставшая де-факто стандартом в экосистеме Python.
Знать `unittest` важно, потому что легаси-код и некоторые корпоративные
codebase всё ещё на нём построены, и pytest умеет запускать `unittest`-тесты
без изменений.

## unittest: пример

```python
import unittest

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(balance=100)

    def tearDown(self):
        self.account.close()

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_withdraw_raises_on_overdraft(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

if __name__ == "__main__":
    unittest.main()
```

## Тот же тест на pytest

```python
import pytest

@pytest.fixture
def account():
    acc = Account(balance=100)
    yield acc
    acc.close()

def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70

def test_withdraw_raises_on_overdraft(account):
    with pytest.raises(ValueError):
        account.withdraw(1000)
```

## Ключевые отличия

| | `unittest` | `pytest` |
|---|---|---|
| Стиль ассертов | `self.assertEqual(a, b)`, `self.assertTrue(x)` — десятки методов | обычный `assert a == b` — pytest сам делает подробный diff |
| Setup/teardown | `setUp`/`tearDown` методы класса, фиксированный жизненный цикл | fixtures — гибкие scope, композиция, переиспользование между файлами |
| Параметризация | нет из коробки (нужен `subTest` или сторонние библиотеки) | `@pytest.mark.parametrize` — из коробки |
| Структура | обязательно классы `TestCase` | простые функции, классы опциональны |
| Плагины/экосистема | ограниченная | огромная (`pytest-cov`, `pytest-mock`, `pytest-asyncio`, `pytest-xdist` и т.д.) |
| Обнаружение тестов | явный `unittest.main()` или `TestLoader` | автоматическое по соглашению об именах |
| Поддержка | стандартная библиотека, стабильна, но развивается медленно | активная разработка, быстрее покрывает новые практики |

## subTest в unittest — частичный аналог parametrize

```python
class TestAdd(unittest.TestCase):
    def test_add_various(self):
        cases = [(2, 3, 5), (-1, 1, 0), (0, 0, 0)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(add(a, b), expected)
```

`subTest` группирует несколько проверок в одном тесте так, что падение
одной не останавливает остальные — но это менее выразительно, чем
`parametrize`: все случаи всё равно один "тест" в отчёте, без отдельных id.

## pytest умеет запускать unittest-тесты как есть

```bash
pytest tests/  # найдёт и unittest.TestCase, и обычные test_* функции
```

Это позволяет мигрировать легаси-код постепенно: новые тесты пишутся на
pytest, старые `TestCase` продолжают работать без переписывания, пока не
дойдут руки.

## Когда выбрать unittest

- Стандартная библиотека без дополнительных зависимостей — важно для
  очень консервативных окружений.
- Команда/codebase уже полностью на `unittest`, миграция не оправдана.

Для нового кода в подавляющем большинстве случаев выбор — `pytest`: меньше
шаблонного кода, удобнее параметризация и fixtures, богаче экосистема.
