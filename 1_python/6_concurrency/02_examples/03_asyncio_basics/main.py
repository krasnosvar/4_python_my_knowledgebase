"""
Базовый event loop: корутины, await, create_task.

Запуск: python main.py
"""
from __future__ import annotations

import asyncio
import time


async def worker(name: str, delay: float) -> str:
    print(f"[{name}] старт")
    await asyncio.sleep(delay)  # точка переключения — event loop может уйти к другой задаче
    print(f"[{name}] финиш")
    return f"{name}-done"


async def sequential_await() -> float:
    """await по очереди — НЕ конкурентно, суммарное время растёт линейно."""
    start = time.perf_counter()
    await worker("seq-1", 0.3)
    await worker("seq-2", 0.3)
    return time.perf_counter() - start


async def concurrent_with_tasks() -> float:
    """create_task планирует выполнение немедленно — задачи идут конкурентно."""
    start = time.perf_counter()
    t1 = asyncio.create_task(worker("task-1", 0.3))
    t2 = asyncio.create_task(worker("task-2", 0.3))
    await t1
    await t2
    return time.perf_counter() - start


async def main() -> None:
    seq_time = await sequential_await()
    print(f"Последовательный await: {seq_time:.2f}s\n")

    conc_time = await concurrent_with_tasks()
    print(f"\nС create_task: {conc_time:.2f}s")

    assert conc_time < seq_time, "конкурентный запуск должен быть быстрее последовательного await"


if __name__ == "__main__":
    asyncio.run(main())
