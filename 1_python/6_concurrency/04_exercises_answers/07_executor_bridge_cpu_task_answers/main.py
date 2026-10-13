"""Решение: 07_executor_bridge_cpu_task"""
from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy(n: int) -> int:
    return sum(i * i for i in range(n))


async def run_cpu_task_without_blocking(n: int) -> tuple[int, int]:
    loop = asyncio.get_running_loop()

    async def ticker() -> int:
        ticks = 0
        for _ in range(10):
            await asyncio.sleep(0.01)
            ticks += 1
        return ticks

    with ProcessPoolExecutor(max_workers=1) as pool:
        cpu_future = loop.run_in_executor(pool, cpu_heavy, n)
        result, ticks = await asyncio.gather(cpu_future, ticker())

    return result, ticks


async def main() -> None:
    result, ticks = await run_cpu_task_without_blocking(3_000_000)

    expected = sum(i * i for i in range(3_000_000))
    assert result == expected
    assert ticks == 10, "event loop должен был успеть сделать все тики, пока считался CPU-таск"

    print(f"Результат: {result}, тиков event loop: {ticks}")


if __name__ == "__main__":
    asyncio.run(main())
