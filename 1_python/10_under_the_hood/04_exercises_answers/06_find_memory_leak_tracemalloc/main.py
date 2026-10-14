"""Решение: 06_find_memory_leak_tracemalloc"""
from __future__ import annotations

import tracemalloc


_leaky_cache: list[str] = []


def leaky_operation(n: int) -> None:
    for i in range(n):
        _leaky_cache.append(f"leaked-item-{i}")


def find_leak_line() -> str:
    tracemalloc.start()

    snapshot1 = tracemalloc.take_snapshot()
    leaky_operation(10_000)
    snapshot2 = tracemalloc.take_snapshot()

    diff = snapshot2.compare_to(snapshot1, "lineno")
    result = str(diff[0])

    tracemalloc.stop()
    return result


def main() -> None:
    checks_passed = 0
    total_checks = 1
    leak_line = find_leak_line()
    print(f"Строка с наибольшим приростом памяти:\n{leak_line}")

    assert "leaky_operation" in leak_line or "main.py" in leak_line
    checks_passed += 1

    print(f"\nРазмер утечки: {len(_leaky_cache)} элементов в _leaky_cache")
    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
