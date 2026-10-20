# Тестирование (pytest) — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.
pytest, `pytest-cov` — сторонние пакеты: `pip install pytest pytest-cov` в venv.

## Запуск

Подробно: [01_pytest_basics_and_structure.md](./01_theory/01_pytest_basics_and_structure.md).

| Задача | Команда |
| :--- | :--- |
| Все тесты | `pytest` |
| Подробно, имя каждого теста | `pytest -v` |
| Остановиться на первом падении | `pytest -x` |
| Только тесты с подстрокой в имени | `pytest -k "withdraw"` |
| Только упавшие в прошлый раз | `pytest --lf` |
| Один тест | `pytest tests/test_account.py::test_withdraw` |
| По маркерам | `pytest -m "not slow"`, `pytest -m "slow or integration"` |
| Сводка по пропущенным / xfail | `pytest -ra` |

Обнаружение: файлы `test_*.py` / `*_test.py`, функции `test_*`, классы `Test*` (без `__init__`).

## Проверки

| Задача | Код |
| :--- | :--- |
| Сравнение | `assert result == expected` (pytest сам показывает diff) |
| Ожидаемое исключение | `with pytest.raises(ValueError, match="insufficient"):` (`match` — regex) |
| Структура теста | Arrange → Act → Assert |

## Fixtures

Подробно: [02_fixtures.md](./01_theory/02_fixtures.md).

```python
@pytest.fixture
def temp_db():
    db = create_test_database()  # setup
    yield db                     # значение для теста
    db.close()                   # teardown — выполнится даже при падении теста
```

| Задача | Синтаксис |
| :--- | :--- |
| Получить fixture | параметр теста с тем же именем: `def test_x(account):` |
| Общие fixtures без импорта | `conftest.py` в каталоге тестов (действует и на подкаталоги) |
| Fixture от fixture | `def user_repo(db_connection): ...` |
| Применить ко всем тестам | `@pytest.fixture(autouse=True)` (только для сквозного: сброс кэша, seed) |
| Несколько объектов с разными параметрами | fixture-фабрика: вернуть внутреннюю функцию `_make(**kw)` |
| Прогнать тесты на нескольких бэкендах | `@pytest.fixture(params=["sqlite", "postgres"])` + `request.param` |

| `scope=` | Экземпляр создаётся | Когда |
| :--- | :--- | :--- |
| `"function"` (по умолчанию) | на каждый тест | почти всегда: полная изоляция |
| `"module"` | один на файл | дорогое соединение, данные не меняются тестами |
| `"session"` | один на весь прогон | контейнер с БД, тяжёлая инициализация |

- ⚠️ Общий `module`/`session` state → тесты проходят только в определённом порядке.

## parametrize

Подробно: [03_parametrize.md](./01_theory/03_parametrize.md).

```python
@pytest.mark.parametrize("value, expected", [
    (0, False),
    (1, True),
    (-5, True),
], ids=["zero", "positive", "negative"])
def test_is_truthy(value, expected):
    assert bool(value) == expected
```

| Задача | Синтаксис |
| :--- | :--- |
| Читаемые имена случаев | `ids=[...]` → `test_is_truthy[zero]` |
| Разные исключения на разных входах | параметр `expected_exception` + `pytest.raises(expected_exception)` |
| Матрица независимых параметров | два декоратора `parametrize` → декартово произведение |

## Моки

Подробно: [04_mocking_unittest_mock_monkeypatch.md](./01_theory/04_mocking_unittest_mock_monkeypatch.md).

| Задача | Код |
| :--- | :--- |
| Подделка с любыми атрибутами | `m = Mock()`; `m.get_user.return_value = {...}` |
| Нужны `__len__`/`__iter__`/`__enter__` | `MagicMock()` |
| Разные ответы по очереди | `m.f.side_effect = [1, ConnectionError("timeout")]` |
| Бросить исключение | `m.f.side_effect = ValueError("bad")` |
| Проверить вызов | `assert_called_once_with(1)`, `assert_not_called()`, `call_count`, `call_args_list` |
| Подменить на время блока | `with patch("myapp.notifier.requests.post") as mock_post:` |
| Подменить декоратором | `@patch("...")` → мок приходит аргументом; несколько `@patch` — снизу вверх |
| Env-переменная в тесте | `monkeypatch.setenv("API_KEY", "test")` / `delenv` |
| Атрибут / функция | `monkeypatch.setattr("myapp.utils.time.time", lambda: 1.0)` |
| Сменить cwd / `sys.path` | `monkeypatch.chdir(tmp)` / `monkeypatch.syspath_prepend(p)` |

**Где патчить.** Модуль `myapp/notifier.py` делает `import requests` →
патчим `"myapp.notifier.requests.post"`; делает `from requests import post` →
патчим `"myapp.notifier.post"`. Правило: там, где имя **используется**.

| | `patch` | `monkeypatch` |
| :--- | :--- | :--- |
| Откат | при выходе из `with` / декоратора | автоматически в teardown |
| Проверка вызовов | есть (`assert_called_*`) | нет — подставляйте `Mock()` как значение |
| Env, cwd, `sys.path` | нет (`patch.dict(os.environ, ...)`) | есть |

- ⚠️ Патч по месту определения, а не использования, не срабатывает, и тест вызывает настоящий код.
- ⚠️ Мокаете 5 из 6 зависимостей — юнит слишком большой, нужен интеграционный тест.
- ⚠️ Проверяете только `return_value` без `assert_called_with` и пропускаете вызов с неверными аргументами.

## Маркеры и конфигурация

Подробно: [05_markers_and_config.md](./01_theory/05_markers_and_config.md).

| Маркер | Эффект |
| :--- | :--- |
| `@pytest.mark.skip(reason=...)` | не запускать |
| `@pytest.mark.skipif(sys.platform == "win32", reason=...)` | не запускать по условию |
| `@pytest.mark.xfail(reason=...)` | падение ожидаемо (`XFAIL`); прошёл → `XPASS`; `strict=True` делает XPASS провалом |
| `@pytest.mark.slow` (свой) | группа для `-m`; регистрировать в `markers` |

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers -q"
markers = ["slow: медленные тесты", "integration: нужны внешние сервисы"]
```

- ⚠️ Без `--strict-markers` опечатка в маркере — лишь предупреждение.
- CI: на каждый коммит `pytest -m "not slow and not integration"`, полный прогон по расписанию.
- Плагины: `pytest-cov`, `pytest-mock` (`mocker`), `pytest-asyncio`, `pytest-xdist` (`-n auto`), `pytest-django`.

## Покрытие

Подробно: [06_coverage.md](./01_theory/06_coverage.md).

| Задача | Команда |
| :--- | :--- |
| Покрытие с номерами непокрытых строк | `pytest --cov=myapp --cov-report=term-missing` |
| Плюс покрытие ветвей | `pytest --cov=myapp --cov-branch --cov-report=term-missing` |
| HTML-отчёт | `pytest --cov=myapp --cov-report=html` |
| Завалить CI ниже порога | `pytest --cov=myapp --cov-fail-under=80` (или `fail_under` в `[tool.coverage.report]`) |
| Исключить строку | `# pragma: no cover` |

- `Missing: 2->4` — переход со строки 2 на 4 ни разу не выполнялся (не проверен исход «условие ложно»).
- ⚠️ 100% line coverage не значит, что проверены обе ветки `if`; и не значит, что есть `assert`.

## unittest ↔ pytest

Подробно: [07_unittest_vs_pytest.md](./01_theory/07_unittest_vs_pytest.md).

| unittest | pytest |
| :--- | :--- |
| `class TestX(unittest.TestCase)` | функция `def test_x():` |
| `self.assertEqual(a, b)` / `assertTrue(x)` | `assert a == b` / `assert x` |
| `with self.assertRaises(E):` | `with pytest.raises(E):` |
| `setUp` / `tearDown` | fixture с `yield` |
| `with self.subTest(a=a):` | `@pytest.mark.parametrize` (у каждого случая свой id) |
| `unittest.main()` / `python -m unittest` | `pytest` (запускает и `TestCase`-тесты без изменений) |

Выбор: новый код — pytest; `unittest` — если нельзя ставить зависимости или вся кодовая база уже на нём.
