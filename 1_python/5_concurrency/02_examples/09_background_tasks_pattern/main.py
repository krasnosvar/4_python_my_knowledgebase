"""
Паттерн фоновых задач: держим ссылки, чтобы задачу не собрал GC раньше
времени, и логируем исключения, которые иначе молча теряются.

Запуск: python main.py
"""
from __future__ import annotations

import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

background_tasks: set[asyncio.Task] = set()


def spawn(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(_on_done)
    return task


def _on_done(task: asyncio.Task) -> None:
    background_tasks.discard(task)
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logging.error("фоновая задача упала: %r", exc)


async def send_metrics(name: str) -> None:
    await asyncio.sleep(0.1)
    logging.info("метрики отправлены: %s", name)


async def flaky_background_job() -> None:
    await asyncio.sleep(0.05)
    raise RuntimeError("не удалось достучаться до внешнего сервиса")


async def graceful_shutdown() -> None:
    for t in list(background_tasks):
        t.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)


async def main() -> None:
    spawn(send_metrics("request-1"))
    spawn(send_metrics("request-2"))
    spawn(flaky_background_job())

    await asyncio.sleep(0.2)  # даём фоновым задачам время выполниться
    print(f"активных фоновых задач осталось: {len(background_tasks)}")

    await graceful_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
