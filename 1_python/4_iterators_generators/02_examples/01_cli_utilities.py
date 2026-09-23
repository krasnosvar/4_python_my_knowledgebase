"""
Потоковая обработка лог-файла через генераторный пайплайн.

Идея: каждая стадия — отдельный генератор, принимающий на вход iterable
и лениво отдающий результат. Данные проходят по одной строке через всю
цепочку, промежуточные списки нигде не создаются.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
import io

RAW_LOG = """\
2026-08-20 10:00:01 INFO  service started
2026-08-20 10:00:02 DEBUG heartbeat
2026-08-20 10:00:05 ERROR connection refused: db-primary
2026-08-20 10:00:07 INFO  retrying connection
2026-08-20 10:00:09 ERROR connection refused: db-primary
2026-08-20 10:00:12 INFO  connection restored
2026-08-20 10:00:20 WARN  slow query: 1200ms
2026-08-20 10:00:33 ERROR disk usage above 90%
"""


def read_lines(source: io.StringIO) -> Iterator[str]:
    """Генератор, лениво отдающий строки файлоподобного объекта."""
    for line in source:
        yield line.rstrip("\n")


def only_level(lines: Iterable[str], level: str) -> Iterator[str]:
    """Фильтрующая стадия пайплайна: пропускает только строки нужного уровня."""
    for line in lines:
        if f" {level} " in line:
            yield line


def extract_message(lines: Iterable[str]) -> Iterator[str]:
    """Преобразующая стадия: оставляет только текст сообщения после уровня."""
    for line in lines:
        _, _, rest = line.partition(" ")  # дата
        _, _, rest = rest.partition(" ")  # время
        _, _, message = rest.partition(" ")  # уровень
        yield message.strip()


def main() -> None:
    source = io.StringIO(RAW_LOG)

    pipeline = extract_message(only_level(read_lines(source), "ERROR"))

    print("Сообщения об ошибках (лениво, построчно):")
    for message in pipeline:
        print(f"  - {message}")


if __name__ == "__main__":
    main()
