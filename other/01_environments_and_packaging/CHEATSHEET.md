# Окружения и упаковка — шпаргалка

Подробности — в [01_theory/](./01_theory/): venv и pip —
[01_venv_and_pip.md](./01_theory/01_venv_and_pip.md), pyproject и Poetry —
[02_pyproject_and_poetry.md](./01_theory/02_pyproject_and_poetry.md).

## venv

| Задача | Linux / macOS | Windows |
| :--- | :--- | :--- |
| Создать окружение в `.venv` | `python3 -m venv .venv` | `py -m venv .venv` |
| Активировать | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| Выйти | `deactivate` | `deactivate` |
| Какой интерпретатор сейчас активен | `which python` | `where python` |

## pip

| Задача | Команда |
| :--- | :--- |
| Поставить пакет (в активный venv) | `pip install requests` |
| Что установлено | `pip list` |
| Версия, зависимости, путь пакета | `pip show requests` |
| Поставить всё из файла | `pip install -r requirements.txt` |
| Слепок текущего окружения ⚠️ (все транзитивные пакеты) | `pip freeze > requirements.txt` |
| Сгенерировать запиненный `requirements.txt` из `requirements.in` | `pip-compile requirements.in` (pip-tools) |
| Запустить pip именно этого интерпретатора | `python3 -m pip install ...` |

## Пиннинг версий

| Запись | Смысл | Когда |
| :--- | :--- | :--- |
| `requests` | Любая версия | Не использовать — приедет новый мажор |
| `requests==2.32.3` | Точная версия | Lock-файл / слепок приложения |
| `requests>=2.32,<3` | Минорные и патчи, без нового мажора | Прямые зависимости, библиотеки |

## Poetry

| Задача | Команда |
| :--- | :--- |
| Создать `pyproject.toml` | `poetry init` |
| Добавить зависимость (обновит и lock) | `poetry add requests` |
| Dev-зависимость | `poetry add --group dev pytest` |
| Поставить всё по lock-файлу | `poetry install` |
| Удалить зависимость | `poetry remove requests` |
| Команда внутри окружения проекта | `poetry run pytest` |
| Активировать окружение (2.x) | `eval $(poetry env activate)` (в 1.x — `poetry shell`) |
| Пересчитать lock-файл | `poetry lock` |
| Проверить lock против `pyproject.toml` | 2.x: `poetry check --lock`; 1.x: `poetry lock --check` |
| Экспорт в `requirements.txt` (2.x: плагин `poetry-plugin-export`) | `poetry export -f requirements.txt --output requirements.txt` |

## Минимальный pyproject.toml (PEP 621)

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115,<0.116"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.6"]
```

## Что коммитить

| Файл | В git? |
| :--- | :--- |
| `.venv/` | Нет — в `.gitignore`, воссоздаётся |
| `requirements.txt` / `requirements.in` | Да |
| `pyproject.toml` | Да |
| `poetry.lock` / `pdm.lock` / `Pipfile.lock` | **Да** — без него нет воспроизводимости |

## Инструменты

| Инструмент | Что делает |
| :--- | :--- |
| `venv` + `pip` | Встроены; окружение и установка, без lock-файла |
| pip-tools | `requirements.in` → запиненный `requirements.txt`; окружением не управляет |
| Poetry | Зависимости + lock + venv + сборка пакета |
| PDM | Как Poetry, ближе к PEP 621 |
| uv | Совместим с `pyproject.toml`/`requirements.txt`, написан на Rust, сильно быстрее |

## Частые ошибки

- ⚠️ `pip install` без активного venv ставит пакет в системный Python (или падает с `externally managed environment`).
- Активация — это только `PATH` текущей сессии шелла: в другом терминале и в CI её нужно повторить.
- ⚠️ `pip freeze` смешивает прямые и транзитивные зависимости — прямые держите в `requirements.in`/`pyproject.toml`.
- `pyproject.toml` без lock-файла даёт разные версии транзитивных зависимостей в разные дни.
