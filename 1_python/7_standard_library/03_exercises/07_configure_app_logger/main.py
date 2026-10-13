"""
Задача: настроить логгер "myapp" так, чтобы:
  - в файл писалось ВСЁ, включая DEBUG;
  - в список in_memory_records (через кастомный handler) попадали только
    сообщения уровня WARNING и выше;
  - формат сообщения включал уровень и текст: "[LEVEL] message".

Запусти: python main.py
"""
from __future__ import annotations

import logging
import tempfile
from pathlib import Path


class ListHandler(logging.Handler):
    """Хендлер, который складывает отформатированные записи в список (для тестов)."""

    def __init__(self, records: list[str]) -> None:
        super().__init__()
        self.records = records

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(self.format(record))


def configure_logger(log_file: Path, in_memory_records: list[str]) -> logging.Logger:
    """
    TODO:
      1. Получить logger = logging.getLogger("myapp"), выставить ему
         setLevel(logging.DEBUG), очистить logger.handlers (logger.handlers.clear()).
      2. Создать FileHandler(log_file) с уровнем DEBUG и Formatter("[%(levelname)s] %(message)s").
      3. Создать ListHandler(in_memory_records) с уровнем WARNING и тем же formatter'ом.
      4. Добавить оба handler'а к логгеру и вернуть логгер.
    """
    raise NotImplementedError


def main() -> None:
    in_memory_records: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "app.log"
        logger = configure_logger(log_file, in_memory_records)

        logger.debug("детали отладки")
        logger.info("обычная информация")
        logger.warning("что-то подозрительное")
        logger.error("критическая ошибка")

        file_content = log_file.read_text(encoding="utf-8")

    assert "[DEBUG] детали отладки" in file_content
    assert "[INFO] обычная информация" in file_content
    assert in_memory_records == [
        "[WARNING] что-то подозрительное",
        "[ERROR] критическая ошибка",
    ], in_memory_records

    print("Файл содержит все уровни, in-memory — только WARNING+:")
    print(in_memory_records)


if __name__ == "__main__":
    main()
