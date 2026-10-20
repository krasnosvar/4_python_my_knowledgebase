"""
cProfile: находим, какая функция расходует больше всего времени.

Запуск: python main.py
"""
from __future__ import annotations

import cProfile
import pstats
import io


def compute_squares(n: int) -> list[int]:
    return [i * i for i in range(n)]


def compute_primes(n: int) -> list[int]:
    primes = []
    for candidate in range(2, n):
        is_prime = all(candidate % p != 0 for p in primes if p * p <= candidate)
        if is_prime:
            primes.append(candidate)
    return primes


def do_work() -> None:
    compute_squares(200_000)
    compute_primes(20_000)  # заведомо более "тяжёлая" функция


def main() -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    do_work()
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
    stats.print_stats(5)
    print(stream.getvalue())

    print("Ожидаемо compute_primes окажется дороже compute_squares по tottime")


if __name__ == "__main__":
    main()
