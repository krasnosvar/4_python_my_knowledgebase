"""
ThreadPoolExecutor и ProcessPoolExecutor: единый API concurrent.futures
для I/O-bound (потоки) и CPU-bound (процессы) работы.

Запуск: python main.py
"""
from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def fake_io(name: str) -> str:
    time.sleep(0.2)
    return f"{name}-fetched"


def cpu_heavy(n: int) -> int:
    return sum(i * i for i in range(n))


def demo_thread_pool() -> None:
    print("--- ThreadPoolExecutor: I/O-bound ---")
    names = [f"job-{i}" for i in range(6)]

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fake_io, name): name for name in names}
        for future in as_completed(futures):
            print(f"готово: {future.result()}")
    print(f"время: {time.perf_counter() - start:.2f}s (не 6 x 0.2s благодаря потокам)\n")


def demo_process_pool() -> None:
    print("--- ProcessPoolExecutor: CPU-bound ---")
    sizes = [2_000_000] * 4

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(cpu_heavy, sizes))
    print(f"результаты (первые 4): {[r for r in results]}")
    print(f"время в процессах: {time.perf_counter() - start:.2f}s")


def main() -> None:
    demo_thread_pool()
    demo_process_pool()


if __name__ == "__main__":
    main()
