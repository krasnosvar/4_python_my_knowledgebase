"""
Задача: реализовать producer/consumer на asyncio.Queue. Producer кладёт
числа от 0 до 49 в очередь, три consumer'а разбирают очередь и складывают
квадраты чисел в общий список результатов.

Запусти: python main.py
"""
from __future__ import annotations

import asyncio


async def producer(queue: asyncio.Queue, n_items: int, n_consumers: int) -> None:
    """
    TODO: положить в очередь числа от 0 до n_items - 1, а затем положить
    n_consumers штук None (по одному sentinel на каждого consumer'а, чтобы
    все они корректно остановились).
    """
    raise NotImplementedError


async def consumer(queue: asyncio.Queue, results: list[int]) -> None:
    """
    TODO: в цикле await queue.get(), пока не придёт None (sentinel) —
    тогда выйти из цикла. Для каждого полученного числа добавить в
    results его квадрат. Не забыть queue.task_done() после обработки
    каждого элемента (включая sentinel).
    """
    raise NotImplementedError


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
