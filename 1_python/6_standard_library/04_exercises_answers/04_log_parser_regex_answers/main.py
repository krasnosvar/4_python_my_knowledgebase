"""Решение: 04_log_parser_regex"""
from __future__ import annotations

import re


LOG_LINES = [
    "2026-08-21 12:00:00 INFO auth_service: user logged in",
    "2026-08-21 12:00:01 ERROR user_service: connection timeout",
    "2026-08-21 12:00:02 WARNING cache: eviction rate high",
]

PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
    r"(?P<component>\S+): (?P<message>.+)"
)


def parse_log_line(line: str) -> dict[str, str]:
    m = PATTERN.match(line)
    if m is None:
        raise ValueError(f"строка не соответствует формату лога: {line!r}")
    result = m.groupdict()
    result["component"] = result["component"].rstrip(":")
    return result


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
