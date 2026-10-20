"""
Задача: дан список строк с датами в ISO-формате с указанием UTC-смещения.
Нужно распарсить их в aware datetime, отсортировать по времени и вернуть
разницу в секундах между самой поздней и самой ранней датой.

Запусти: python main.py
"""
from __future__ import annotations


RAW_DATES = [
    "2026-08-21T09:00:00+00:00",
    "2026-08-21T05:30:00-03:00",  # это 08:30 UTC
    "2026-08-21T12:15:00+03:00",  # это 09:15 UTC
]


def parse_and_analyze(raw_dates: list[str]) -> float:
    """
    TODO:
      1. Распарсить каждую строку через datetime.fromisoformat.
      2. Отсортировать список datetime по времени (сравнение aware
         datetime корректно работает независимо от смещения).
      3. Вернуть (самая_поздняя - самая_ранняя).total_seconds().
    """
    raise NotImplementedError


def main() -> None:
    checks_passed = 0
    total_checks = 1
    diff_seconds = parse_and_analyze(RAW_DATES)

    # самая ранняя: 08:30 UTC, самая поздняя: 09:15 UTC -> разница 45 минут
    assert diff_seconds == 45 * 60, f"ожидали 2700.0, получили {diff_seconds}"
    checks_passed += 1

    print(f"Разница между самой ранней и самой поздней датой: {diff_seconds}s")
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
