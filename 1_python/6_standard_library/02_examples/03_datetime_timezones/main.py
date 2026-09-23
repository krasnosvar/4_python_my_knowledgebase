"""
datetime, timedelta, aware vs naive, zoneinfo.

Запуск: python main.py
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def demo_naive_vs_aware() -> None:
    print("--- naive vs aware ---")
    naive = datetime(2026, 8, 21, 12, 0, 0)
    aware = datetime(2026, 8, 21, 12, 0, 0, tzinfo=timezone.utc)
    print(f"naive: {naive} (tzinfo={naive.tzinfo})")
    print(f"aware: {aware} (tzinfo={aware.tzinfo})")

    try:
        naive < aware
    except TypeError as e:
        print(f"сравнение naive и aware ломается: {e}")


def demo_zoneinfo() -> None:
    print("\n--- zoneinfo ---")
    utc_now = datetime(2026, 8, 21, 12, 0, 0, tzinfo=timezone.utc)
    moscow = utc_now.astimezone(ZoneInfo("Europe/Moscow"))
    tokyo = utc_now.astimezone(ZoneInfo("Asia/Tokyo"))
    print(f"UTC:    {utc_now.isoformat()}")
    print(f"Moscow: {moscow.isoformat()}")
    print(f"Tokyo:  {tokyo.isoformat()}")


def demo_parsing_formatting() -> None:
    print("\n--- parsing / formatting ---")
    dt = datetime.strptime("2026-08-21 14:30", "%Y-%m-%d %H:%M")
    print(f"strptime: {dt}")
    print(f"strftime: {dt.strftime('%d.%m.%Y %H:%M')}")

    dt2 = datetime.fromisoformat("2026-08-21T14:30:00+00:00")
    print(f"fromisoformat: {dt2}")


def demo_timedelta() -> None:
    print("\n--- timedelta ---")
    now = datetime.now(timezone.utc)
    in_a_week = now + timedelta(days=7)
    diff = in_a_week - now
    print(f"через неделю: {in_a_week.date()}, разница в секундах: {diff.total_seconds()}")


def main() -> None:
    demo_naive_vs_aware()
    demo_zoneinfo()
    demo_parsing_formatting()
    demo_timedelta()


if __name__ == "__main__":
    main()
