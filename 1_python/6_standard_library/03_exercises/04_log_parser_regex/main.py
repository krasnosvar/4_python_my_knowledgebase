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
    checks_passed = 0
    total_checks = 4
    parsed = parse_all(LOG_LINES)

    assert parsed[1]["level"] == "ERROR"
    checks_passed += 1
    assert parsed[1]["component"] == "user_service"
    checks_passed += 1
    assert parsed[1]["message"] == "connection timeout"
    checks_passed += 1
    assert parsed[0]["timestamp"] == "2026-08-21 12:00:00"
    checks_passed += 1

    for entry in parsed:
        print(entry)
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
