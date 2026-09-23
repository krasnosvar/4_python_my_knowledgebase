"""Реестр команд через декоратор + контекст-менеджер для временного ресурса."""

from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import Callable
from contextlib import contextmanager

COMMANDS: dict[str, Callable[..., None]] = {}


def command(name: str) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """Декоратор-фабрика: регистрирует функцию под именем `name` в реестре команд."""

    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        COMMANDS[name] = func
        return func

    return decorator


@command("hello")
def cmd_hello(who: str = "мир") -> None:
    print(f"Привет, {who}!")


@command("list-files")
def cmd_list_files(directory: str) -> None:
    for entry in sorted(os.listdir(directory)):
        print(f"  - {entry}")


def dispatch(name: str, *args, **kwargs) -> None:
    handler = COMMANDS.get(name)
    if handler is None:
        raise KeyError(f"Неизвестная команда: {name}")
    handler(*args, **kwargs)


@contextmanager
def temporary_workspace():
    """Контекст-менеджер: создаёт временную директорию и гарантированно удаляет её."""
    path = tempfile.mkdtemp(prefix="cli_workspace_")
    print(f"Создана временная директория: {path}")
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
        print(f"Временная директория удалена: {path}")


if __name__ == "__main__":
    print("Зарегистрированные команды:", sorted(COMMANDS))

    dispatch("hello", "разработчик")

    with temporary_workspace() as workspace:
        for name in ("a.txt", "b.txt", "c.log"):
            open(os.path.join(workspace, name), "w").close()
        dispatch("list-files", workspace)

    print("Работа с временным ресурсом завершена")
