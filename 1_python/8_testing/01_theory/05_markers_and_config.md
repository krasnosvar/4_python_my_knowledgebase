# Маркеры и конфигурация pytest

## Встроенные маркеры

```python
import sys

import pytest

@pytest.mark.skip(reason="функция ещё не реализована")
def test_future_feature():
    ...

@pytest.mark.skipif(sys.platform == "win32", reason="не работает на Windows")
def test_unix_only():
    ...

@pytest.mark.xfail(reason="известный баг, тикет JIRA-123")
def test_known_bug():
    assert buggy_function() == 42  # ожидаемо упадёт, не считается провалом прогона

@pytest.mark.slow
def test_heavy_integration():
    ...
```

- `skip`/`skipif` — тест не запускается вообще.
- `xfail` — тест запускается, но ожидаемое падение не считается провалом
  прогона (`XFAIL` в отчёте); если тест неожиданно **проходит** — это
  `XPASS`, что тоже стоит внимания (можно настроить как провал через
  `strict=True`).
- Пользовательские маркеры (`slow`, `integration`, `smoke`) — способ
  группировать тесты для выборочного запуска.

## Регистрация кастомных маркеров

pytest предупреждает о неизвестных маркерах, если они не зарегистрированы
в конфигурации — это защита от опечаток:

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: помечает медленные тесты",
    "integration: тесты, требующие внешних сервисов",
]
```

## Запуск по маркерам

```bash
pytest -m "not slow"              # пропустить медленные тесты
pytest -m "integration"           # только интеграционные
pytest -m "slow or integration"   # логические выражения над маркерами
```

Типичный CI-паттерн: быстрый прогон `pytest -m "not slow and not integration"`
на каждый коммит, полный прогон (все маркеры) — по расписанию или перед
релизом.

## conftest.py и хуки

`conftest.py` — не только fixtures, но и место для хуков, влияющих на сбор
и запуск тестов:

```python
# conftest.py
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "slow" in item.keywords and not config.getoption("--run-slow"):
            item.add_marker(pytest.mark.skip(reason="нужен флаг --run-slow"))
```

## pytest.ini / pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers -q"
markers = ["slow: медленные тесты"]
```

- `testpaths` — где искать тесты по умолчанию (не нужно указывать путь в CLI).
- `addopts` — опции, применяемые к каждому запуску `pytest` автоматически.
- `--strict-markers` — незарегистрированный маркер становится ошибкой, а
  не предупреждением (полезно, чтобы отловить опечатки в имени маркера).

## Плагины

Экосистема плагинов — одна из причин, почему pytest вытеснил `unittest` на
практике: `pytest-cov` (покрытие), `pytest-asyncio` (тестирование
корутин), `pytest-mock` (обёртка над `unittest.mock` как fixture `mocker`),
`pytest-xdist` (параллельный запуск тестов), `pytest-django`/`pytest-flask`
(интеграция с фреймворками). Устанавливаются как обычные пакеты, pytest
подхватывает их автоматически через точки входа (entry points).
