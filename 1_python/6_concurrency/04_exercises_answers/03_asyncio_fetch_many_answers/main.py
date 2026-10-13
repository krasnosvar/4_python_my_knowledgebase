"""Решение: 03_asyncio_fetch_many"""
from __future__ import annotations

import asyncio
import time


async def fetch(item_id: int) -> str:
    await asyncio.sleep(0.1)
    return f"data-{item_id}"


async def fetch_all(ids: list[int]) -> dict[int, str]:
    results = await asyncio.gather(*(fetch(i) for i in ids))
    return dict(zip(ids, results))


async def main() -> None:
    ids = list(range(20))

    start = time.perf_counter()
    results = await fetch_all(ids)
    elapsed = time.perf_counter() - start

    assert results == {i: f"data-{i}" for i in ids}
    assert elapsed < 0.5, "20 запросов по 0.1s должны выполниться конкурентно, а не за 2s"

    print(f"Получено {len(results)} результатов за {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
