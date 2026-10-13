# pyproject.toml и Poetry

## requirements.txt vs pyproject.toml

`requirements.txt` описывает только **список зависимостей для установки** —
он ничего не знает о том, как называется ваш проект, какая у него версия,
как его собрать в пакет, какие есть точки входа (CLI-команды) и т.д.

`pyproject.toml` — единый стандартизированный (PEP 517/518/621) файл
конфигурации проекта: метаданные пакета, зависимости, настройки
инструментов сборки, линтеров, тестраннера — всё в одном месте, одним
форматом (TOML), вместо россыпи `setup.py`, `setup.cfg`, `requirements.txt`,
`pytest.ini`, `.flake8` и т.д.

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "Пример приложения"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115,<0.116",
    "uvicorn[standard]>=0.30,<0.31",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.6"]
```

## Poetry: зависимости + lock-файл + сборка пакета

Poetry — популярный инструмент, который берёт на себя весь жизненный цикл
зависимостей поверх `pyproject.toml`:

```bash
poetry init                 # интерактивно создать pyproject.toml
poetry add requests           # добавить зависимость (обновит pyproject.toml И lock-файл)
poetry add --group dev pytest  # dev-зависимость (не ставится в проде)
poetry install                # установить всё согласно lock-файлу
poetry remove requests         # убрать зависимость
poetry run pytest              # запустить команду внутри виртуального окружения проекта
poetry env activate             # Poetry 2.x: напечатать команду активации окружения
eval $(poetry env activate)     # ...и сразу выполнить её в текущем шелле
```

В Poetry 1.x окружение активировали командой `poetry shell`. С Poetry 2.0
она убрана из основной поставки: либо `poetry env activate` (как выше),
либо отдельный плагин `poetry-plugin-shell`, который возвращает `poetry
shell`.

## poetry.lock: зачем нужен lock-файл

`pyproject.toml` описывает **диапазоны** допустимых версий
(`fastapi>=0.115,<0.116`). `poetry.lock` фиксирует **точные** версии всего
дерева зависимостей (включая транзитивные), которые реально были
разрешены при последней установке — вплоть до хэшей пакетов.

⚠️ Неочевидный, но критичный момент: **`pyproject.toml` без lock-файла не
даёт воспроизводимости**. Два человека, поставившие зависимости по одному
и тому же `pyproject.toml` в разные дни, могут получить разные версии
транзитивных зависимостей — и разное поведение кода. `poetry.lock` (как и
`requirements.txt` с точными версиями, как и `Pipfile.lock`, `pdm.lock`)
решает именно эту проблему — он **обязательно коммитится в git**, в
отличие от `.venv/`.

```bash
poetry lock                  # пересчитать lock-файл (например, после правки диапазонов)
poetry check --lock           # проверить, что lock-файл соответствует pyproject.toml
poetry export -f requirements.txt --output requirements.txt   # экспорт для окружений без poetry
```

Версии Poetry: в 1.x проверка lock-файла называлась `poetry lock --check`,
в 2.x — `poetry check --lock`. `poetry export` в Poetry 2.x тоже не входит
в основную поставку — нужен плагин `poetry-plugin-export`.

## Альтернативы Poetry

- **pip-tools** (`pip-compile`) — минималистичный, просто генерирует
  запиненный `requirements.txt` из `requirements.in`, без управления
  окружением.
- **PDM** — похож на Poetry, полнее следует стандарту PEP 621.
- **uv** — новый инструмент (от создателей Ruff), совместим с
  `pyproject.toml`/`requirements.txt`, заметно быстрее pip/poetry за счёт
  реализации на Rust; на 2026 год — фактически новый стандарт де-факто для
  новых проектов.

Выбор конкретного инструмента менее важен, чем сам принцип: **зависимости
проекта = декларация диапазонов (pyproject.toml) + зафиксированный
lock-файл (коммитится в git) + venv, который из этого lock-файла
воссоздаётся** на любой машине одинаково.
