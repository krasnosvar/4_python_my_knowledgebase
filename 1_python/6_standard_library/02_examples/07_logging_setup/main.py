"""
logging: базовая настройка, уровни, handlers, formatters.

Запуск: python main.py
"""
from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path


def build_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("myapp.demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()  # чтобы повторный вызов в демо не плодил дубли handler'ов

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)   # в консоль — только INFO и выше
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)      # в файл — вообще всё, включая DEBUG
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "app.log"
        logger = build_logger(log_file)

        logger.debug("детальная отладочная информация (только в файл)")
        logger.info("сервис запущен (в консоль и в файл)")
        logger.warning("конфиг не найден, использую дефолт")
        logger.error("не удалось подключиться к БД")

        print("\n--- содержимое файла лога (включая DEBUG) ---")
        print(log_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
