"""
run_in_executor: мост между event loop и блокирующим/CPU-тяжёлым кодом.

Запуск: python main.py
"""
from __future__ import annotations

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def blocking_sync_call(name: str) -> str:
    """Синхронная блокирующая функция без async-версии (например, легаси-либа)."""
    time.sleep(0.3)
    return f"{name}-done"


def cpu_heavy(n: int) -> int:
    return sum(i * i for i in range(n))


async def demo_default_thread_executor() -> None:
    print("--- run_in_executor(None, ...) — дефолтный thread pool ---")
    loop = asyncio.get_running_loop()

    start = time.perf_counter()
    results = await asyncio.gather(
        *(loop.run_in_executor(None, blocking_sync_call, f"job-{i}") for i in range(4))
    )
    print(results)
    print(f"время: {time.perf_counter() - start:.2f}s (конкурентно, а не 4 x 0.3s)\n")


async def demo_process_executor() -> None:
    print("--- run_in_executor с ProcessPoolExecutor — CPU-bound внутри event loop ---")
    loop = asyncio.get_running_loop()

    async def ping_event_loop() -> None:
        """Показывает, что event loop не заблокирован во время CPU-задачи в процессе."""
        for i in range(5):
            await asyncio.sleep(0.05)
            print(f"event loop жив, тик {i}")

    with ProcessPoolExecutor(max_workers=2) as pool:
        cpu_task = loop.run_in_executor(pool, cpu_heavy, 5_000_000)
        await asyncio.gather(cpu_task, ping_event_loop())


async def main() -> None:
    await demo_default_thread_executor()
    await demo_process_executor()


if __name__ == "__main__":
    asyncio.run(main())
