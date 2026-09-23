"""
tracemalloc: находим, где выделяется больше всего памяти, сравниваем
два снапшота, чтобы найти "утечку".

Запуск: python main.py
"""
from __future__ import annotations

import tracemalloc


def allocate_strings(n: int) -> list[str]:
    return [str(i) * 50 for i in range(n)]


def demo_snapshot_top_allocations() -> None:
    print("--- top-5 мест выделения памяти ---")
    tracemalloc.start()

    data = allocate_strings(50_000)

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    for stat in top_stats[:5]:
        print(stat)

    del data
    tracemalloc.stop()


def demo_compare_snapshots() -> None:
    print("\n--- сравнение снапшотов: поиск прироста памяти ---")
    tracemalloc.start()

    snapshot1 = tracemalloc.take_snapshot()

    leaky_cache: list[str] = []
    for _ in range(3):
        leaky_cache.extend(allocate_strings(10_000))  # "утечка", растущая с каждым вызовом

    snapshot2 = tracemalloc.take_snapshot()
    diff = snapshot2.compare_to(snapshot1, "lineno")

    print("строки с наибольшим приростом памяти между снапшотами:")
    for stat in diff[:5]:
        print(stat)

    tracemalloc.stop()


def main() -> None:
    demo_snapshot_top_allocations()
    demo_compare_snapshots()


if __name__ == "__main__":
    main()
