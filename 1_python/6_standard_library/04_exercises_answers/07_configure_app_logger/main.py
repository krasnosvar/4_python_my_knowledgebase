"""Решение: 07_configure_app_logger"""
from __future__ import annotations

import logging
import tempfile
from pathlib import Path


class ListHandler(logging.Handler):
    def __init__(self, records: list[str]) -> None:
        super().__init__()
        self.records = records

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(self.format(record))


def configure_logger(log_file: Path, in_memory_records: list[str]) -> logging.Logger:
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter("[%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    memory_handler = ListHandler(in_memory_records)
    memory_handler.setLevel(logging.WARNING)
    memory_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(memory_handler)
    return logger


def main() -> None:
    checks_passed = 0
    total_checks = 3
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
    checks_passed += 1
    assert "[INFO] обычная информация" in file_content
    checks_passed += 1
    assert in_memory_records == [
        "[WARNING] что-то подозрительное",
        "[ERROR] критическая ошибка",
    ], in_memory_records
    checks_passed += 1

    print("Файл содержит все уровни, in-memory — только WARNING+:")
    print(in_memory_records)
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
