"""Решение: 06_taskgroup_error_handling"""
from __future__ import annotations

import asyncio


async def long_running(name: str, was_cancelled: dict) -> None:
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        was_cancelled[name] = True
        raise


async def failing(name: str) -> None:
    await asyncio.sleep(0.05)
    raise ValueError(f"{name} failed")


async def run_group_and_report() -> tuple[int, dict]:
    was_cancelled: dict = {}
    error_count = 0

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(long_running("a", was_cancelled))
            tg.create_task(long_running("b", was_cancelled))
            tg.create_task(failing("c"))
    except* ValueError as eg:
        error_count = len(eg.exceptions)

    return error_count, was_cancelled


async def main() -> None:
    checks_passed = 0
    total_checks = 3

    error_count, was_cancelled = await run_group_and_report()

    assert error_count == 1
    checks_passed += 1
    assert was_cancelled.get("a") is True
    checks_passed += 1
    assert was_cancelled.get("b") is True
    checks_passed += 1

    print(f"Ошибок поймано: {error_count}, отменённые задачи: {list(was_cancelled)}")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    asyncio.run(main())
