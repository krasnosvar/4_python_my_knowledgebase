"""
Задача: используя tracemalloc, сравнить два снапшота "до" и "после"
работы функции-утечки и найти строку кода с наибольшим приростом памяти.

Запусти: python main.py
"""
from __future__ import annotations

import tracemalloc


_leaky_cache: list[str] = []


def leaky_operation(n: int) -> None:
    """Намеренная "утечка": добавляет в глобальный список и никогда не чистит."""
    for i in range(n):
        _leaky_cache.append(f"leaked-item-{i}")


def find_leak_line() -> str:
    """
    TODO:
      1. tracemalloc.start()
      2. snapshot1 = tracemalloc.take_snapshot()
      3. Вызвать leaky_operation(10_000)
      4. snapshot2 = tracemalloc.take_snapshot()
      5. diff = snapshot2.compare_to(snapshot1, "lineno")
      6. Вернуть str(diff[0]) — самую "тяжёлую" по приросту строку.
      7. tracemalloc.stop()
    """
    raise NotImplementedError


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
