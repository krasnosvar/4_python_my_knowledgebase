"""
Задача: посчитать, сколько простых чисел среди заданного списка больших
чисел, используя multiprocessing.Pool, чтобы задействовать все ядра CPU.

Запусти: python main.py
"""
from __future__ import annotations

import time
from multiprocessing import cpu_count


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes_parallel(numbers: list[int]) -> int:
    """
    TODO: использовать multiprocessing.Pool(processes=cpu_count()) и
    pool.map(is_prime, numbers), чтобы распределить проверку чисел по
    процессам. Вернуть количество простых чисел (сумму True в результатах).
    """
    raise NotImplementedError


def main() -> None:
    numbers = [100_003 + i for i in range(200)]

    start = time.perf_counter()
    count = count_primes_parallel(numbers)
    elapsed = time.perf_counter() - start

    expected = sum(1 for n in numbers if is_prime(n))
    assert count == expected, f"ожидали {expected} простых, получили {count}"

    print(f"Найдено простых: {count} из {len(numbers)}, время: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
