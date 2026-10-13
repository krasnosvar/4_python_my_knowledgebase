"""
Демонстрация разницы O(n) vs O(n^2) на практике, замер времени.

Запуск: python main.py
"""
from __future__ import annotations

import time


def has_duplicate_slow(items: list[int]) -> bool:
    """O(n^2): вложенный цикл сравнивает каждую пару."""
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


def has_duplicate_fast(items: list[int]) -> bool:
    """O(n): один проход + множество для проверки за O(1)."""
    seen: set[int] = set()
    for x in items:
        if x in seen:
            return True
        seen.add(x)
    return False


def main() -> None:
    # без дубликатов -> оба алгоритма проходят весь вход (худший случай)
    data = list(range(4000))

    start = time.perf_counter()
    has_duplicate_slow(data)
    slow_time = time.perf_counter() - start

    start = time.perf_counter()
    has_duplicate_fast(data)
    fast_time = time.perf_counter() - start

    print(f"O(n^2) версия: {slow_time:.4f}s")
    print(f"O(n) версия:   {fast_time:.4f}s")
    print(f"Ускорение: x{slow_time / fast_time:.1f}")

    assert fast_time < slow_time


if __name__ == "__main__":
    main()
