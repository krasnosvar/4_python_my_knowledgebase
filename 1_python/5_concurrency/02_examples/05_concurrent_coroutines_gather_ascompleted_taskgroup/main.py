"""
gather vs as_completed vs TaskGroup — три способа запустить корутины
конкурентно, с разной семантикой порядка и обработки ошибок.

Требует Python 3.11+ (TaskGroup).
Запуск: python main.py
"""
from __future__ import annotations

import asyncio


async def fetch(name: str, delay: float, fail: bool = False) -> str:
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"{name} failed")
    return f"{name}-result"


async def demo_gather() -> None:
    print("--- gather: порядок результатов = порядок аргументов ---")
    results = await asyncio.gather(
        fetch("a", 0.3), fetch("b", 0.1), fetch("c", 0.2),
    )
    print(results)  # всегда [a-result, b-result, c-result], хотя b быстрее всех


async def demo_gather_with_exceptions() -> None:
    print("\n--- gather(return_exceptions=True): ошибки как значения ---")
    results = await asyncio.gather(
        fetch("a", 0.1), fetch("bad", 0.05, fail=True), fetch("c", 0.1),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"ошибка: {r}")
        else:
            print(f"ок: {r}")


async def demo_as_completed() -> None:
    print("\n--- as_completed: порядок по готовности ---")
    coros = [fetch("a", 0.3), fetch("b", 0.1), fetch("c", 0.2)]
    for coro in asyncio.as_completed(coros):
        result = await coro
        print(f"готово: {result}")  # первым будет b (самый короткий delay)


async def demo_taskgroup() -> None:
    print("\n--- TaskGroup: структурная конкурентность (3.11+) ---")
    results: list[str] = []

    async def run(name: str, delay: float) -> None:
        results.append(await fetch(name, delay))

    async with asyncio.TaskGroup() as tg:
        tg.create_task(run("a", 0.2))
        tg.create_task(run("b", 0.1))
        tg.create_task(run("c", 0.15))
    print(f"все задачи завершены: {sorted(results)}")


async def demo_taskgroup_cancels_siblings() -> None:
    print("\n--- TaskGroup: ошибка одной задачи отменяет остальные ---")
    cancelled = {"long_task": False}

    async def long_task() -> None:
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            cancelled["long_task"] = True
            raise

    async def failing_task() -> None:
        await asyncio.sleep(0.05)
        raise ValueError("boom")

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(long_task())
            tg.create_task(failing_task())
    except* ValueError as eg:
        print(f"поймано исключений в группе: {len(eg.exceptions)}")

    assert cancelled["long_task"], "долгая задача должна быть отменена при ошибке соседа"


async def main() -> None:
    await demo_gather()
    await demo_gather_with_exceptions()
    await demo_as_completed()
    await demo_taskgroup()
    await demo_taskgroup_cancels_siblings()


if __name__ == "__main__":
    asyncio.run(main())
