"""
Задача: распарсить строки лога вида
"2026-08-21 12:00:01 ERROR user_service: connection timeout"
в структуру {"timestamp": ..., "level": ..., "component": ..., "message": ...}
с помощью именованных групп re.

Запусти: python main.py
"""
from __future__ import annotations


LOG_LINES = [
    "2026-08-21 12:00:00 INFO auth_service: user logged in",
    "2026-08-21 12:00:01 ERROR user_service: connection timeout",
    "2026-08-21 12:00:02 WARNING cache: eviction rate high",
]


def parse_log_line(line: str) -> dict[str, str]:
    """
    TODO: с помощью re.compile и именованных групп
    (?P<timestamp>...), (?P<level>...), (?P<component>...), (?P<message>...)
    распарсить строку и вернуть m.groupdict().

    Формат: "<timestamp> <LEVEL> <component>: <message>"
    где timestamp — "YYYY-MM-DD HH:MM:SS", LEVEL — одно из
    DEBUG/INFO/WARNING/ERROR/CRITICAL, component — слово без пробелов.
    """
    raise NotImplementedError


def parse_all(lines: list[str]) -> list[dict[str, str]]:
    return [parse_log_line(line) for line in lines]


def main() -> None:
    parsed = parse_all(LOG_LINES)

    assert parsed[1]["level"] == "ERROR"
    assert parsed[1]["component"] == "user_service"
    assert parsed[1]["message"] == "connection timeout"
    assert parsed[0]["timestamp"] == "2026-08-21 12:00:00"

    for entry in parsed:
        print(entry)


if __name__ == "__main__":
    main()
