"""Готовый модуль — простое файловое хранилище ключ-значение."""
from __future__ import annotations

from pathlib import Path


class FileStorage:
    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, key: str, value: str) -> None:
        (self.directory / f"{key}.txt").write_text(value, encoding="utf-8")

    def read(self, key: str) -> str:
        path = self.directory / f"{key}.txt"
        if not path.exists():
            raise KeyError(key)
        return path.read_text(encoding="utf-8")

    def delete(self, key: str) -> None:
        path = self.directory / f"{key}.txt"
        path.unlink(missing_ok=True)
