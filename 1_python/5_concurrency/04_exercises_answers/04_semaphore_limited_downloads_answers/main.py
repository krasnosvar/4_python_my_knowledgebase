"""Решение: 04_semaphore_limited_downloads"""
from __future__ import annotations

import asyncio


async def download(file_id: int, sem: asyncio.Semaphore, active: dict) -> str:
    async with sem:
        active["count"] += 1
        active["max"] = max(active["max"], active["count"])
        await asyncio.sleep(0.05)
        active["count"] -= 1
    return f"file-{file_id}-downloaded"


async def download_all(file_ids: list[int], max_concurrent: int) -> list[str]:
    sem = asyncio.Semaphore(max_concurrent)
    active = {"count": 0, "max": 0}
    results = await asyncio.gather(*(download(fid, sem, active) for fid in file_ids))
    assert active["max"] <= max_concurrent
    return list(results)


async def main() -> None:
    file_ids = list(range(20))
    results = await download_all(file_ids, max_concurrent=3)

    assert len(results) == 20
    assert all(r.endswith("downloaded") for r in results)
    print(f"Скачано файлов: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
