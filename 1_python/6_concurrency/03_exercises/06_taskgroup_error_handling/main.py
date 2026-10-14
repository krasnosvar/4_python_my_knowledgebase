"""
Задача: используя asyncio.TaskGroup (Python 3.11+), запустить три задачи,
одна из которых падает с ValueError. Нужно:
  1. Поймать ExceptionGroup через except*.
  2. Убедиться, что остальные (не упавшие) задачи были отменены.

Запусти: python main.py
"""
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
    """
    TODO:
      1. Создать словарь was_cancelled = {}.
      2. Внутри try/except* ValueError открыть asyncio.TaskGroup и
         запустить long_running("a", was_cancelled), long_running("b", was_cancelled)
         и failing("c").
      3. В except* ValueError as eg посчитать число исключений в eg.exceptions.
      4. Вернуть (число_исключений, was_cancelled).
    """
    raise NotImplementedError


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
