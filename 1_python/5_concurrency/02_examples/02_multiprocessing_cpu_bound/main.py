"""
multiprocessing даёт реальный параллелизм по ядрам для CPU-bound работы,
в отличие от threading (см. 01_gil_and_execution_model.md).

Запуск: python main.py
"""
from __future__ import annotations

import time
from multiprocessing import Pool, cpu_count


def count_primes_up_to(n: int) -> int:
    """Чисто CPU-bound работа: без единого системного вызова."""
    count = 0
    for candidate in range(2, n):
        is_prime = True
        for divisor in range(2, int(candidate**0.5) + 1):
            if candidate % divisor == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


def sequential(chunks: list[int]) -> float:
    start = time.perf_counter()
    for n in chunks:
        count_primes_up_to(n)
    return time.perf_counter() - start


def parallel(chunks: list[int]) -> float:
    start = time.perf_counter()
    with Pool(processes=cpu_count()) as pool:
        pool.map(count_primes_up_to, chunks)
    return time.perf_counter() - start


def main() -> None:
    chunks = [50_000] * cpu_count()

    seq_time = sequential(chunks)
    print(f"Последовательно: {seq_time:.2f}s")

    par_time = parallel(chunks)
    print(f"В процессах ({cpu_count()} ядра): {par_time:.2f}s")

    print(f"Ускорение: x{seq_time / par_time:.2f}")


if __name__ == "__main__":
    # multiprocessing на spawn-платформах (Windows/macOS) требует,
    # чтобы точка входа была защищена этим блоком
    main()
