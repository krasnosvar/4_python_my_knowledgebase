"""Решение: 05_producer_consumer_queue"""
from __future__ import annotations

import asyncio


async def producer(queue: asyncio.Queue, n_items: int, n_consumers: int) -> None:
    for i in range(n_items):
        await queue.put(i)
    for _ in range(n_consumers):
        await queue.put(None)


async def consumer(queue: asyncio.Queue, results: list[int]) -> None:
    while (item := await queue.get()) is not None:
        results.append(item * item)
        queue.task_done()
    queue.task_done()  # sentinel тоже нужно "закрыть"


async def main() -> None:
    checks_passed = 0
    total_checks = 1

    n_items = 50
    n_consumers = 3
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    results: list[int] = []

    await asyncio.gather(
        producer(queue, n_items, n_consumers),
        *(consumer(queue, results) for _ in range(n_consumers)),
    )

    assert sorted(results) == [i * i for i in range(n_items)]
    checks_passed += 1
    print(f"Обработано элементов: {len(results)}")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    asyncio.run(main())
