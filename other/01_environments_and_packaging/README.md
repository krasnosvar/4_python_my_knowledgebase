# Окружения и упаковка (venv, pip, Poetry)

Как устанавливать Python-библиотеки так, чтобы проекты не мешали друг
другу, и как зафиксировать зависимости, чтобы код одинаково работал у вас,
у коллег и на сервере.

**Нужно до первого `pip install -r requirements.txt` в этом репозитории.**
Многие темы (`2_data_and_messaging`, `3_web_frameworks`, примеры с Docker)
просят поставить зависимости — сначала создайте виртуальное окружение по
[01_venv_and_pip.md](./01_theory/01_venv_and_pip.md), иначе библиотеки
встанут глобально в системный Python.

## Структура

- **[01_theory/](./01_theory/)** — теория, по порядку:
  - [01_venv_and_pip.md](./01_theory/01_venv_and_pip.md) — зачем
    изолировать окружение, команды `venv`, `requirements.txt`, зачем
    пиновать версии.
  - [02_pyproject_and_poetry.md](./01_theory/02_pyproject_and_poetry.md) —
    `requirements.txt` vs `pyproject.toml`, команды Poetry (1.x и 2.x),
    зачем lock-файл, альтернативы Poetry.
- **[02_examples/](./02_examples/)** — рабочие файлы: `requirements.in` →
  `requirements.txt` (pip-tools), `requirements-dev.txt`, `pyproject.toml`.

Упражнений нет — это справочный материал.

## Как использовать

1. Перед первым запуском примеров из репозитория прочитайте `01_venv_and_pip.md`
   и создайте окружение:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. `02_pyproject_and_poetry.md` — когда начнёте собственный проект или
   встретите `pyproject.toml`/`poetry.lock` в чужом.

[К разделу other](../README.md).
