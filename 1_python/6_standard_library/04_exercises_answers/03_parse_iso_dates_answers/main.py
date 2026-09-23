"""Решение: 03_parse_iso_dates"""
from __future__ import annotations

from datetime import datetime


RAW_DATES = [
    "2026-08-21T09:00:00+00:00",
    "2026-08-21T05:30:00-03:00",
    "2026-08-21T12:15:00+03:00",
]


def parse_and_analyze(raw_dates: list[str]) -> float:
    parsed = sorted(datetime.fromisoformat(d) for d in raw_dates)
    return (parsed[-1] - parsed[0]).total_seconds()


def main() -> None:
    diff_seconds = parse_and_analyze(RAW_DATES)

    assert diff_seconds == 45 * 60, f"ожидали 2700.0, получили {diff_seconds}"

    print(f"Разница между самой ранней и самой поздней датой: {diff_seconds}s")


if __name__ == "__main__":
    main()
