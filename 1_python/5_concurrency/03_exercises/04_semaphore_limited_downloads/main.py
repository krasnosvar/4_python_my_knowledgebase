"""
Задача: "скачать" 20 файлов конкурентно, но не более 3 одновременно
(имитация ограничения на число открытых соединений).

Запусти: python main.py
"""
from __future__ import annotations

import asyncio


async def download(file_id: int, sem: asyncio.Semaphore, active: dict) -> str:
    """
    TODO:
      1. Захватить семафор (async with sem).
      2. Увеличить active["count"], обновить active["max"] = max(...).
      3. await asyncio.sleep(0.05) — имитация скачивания.
      4. Уменьшить active["count"].
      5. Вернуть f"file-{file_id}-downloaded".
    """
    raise NotImplementedError


async def download_all(file_ids: list[int], max_concurrent: int) -> list[str]:
    """
    TODO: создать asyncio.Semaphore(max_concurrent) и словарь active =
    {"count": 0, "max": 0}, запустить download(...) для всех file_ids
    конкурентно через gather, вернуть список результатов.
    """
    raise NotImplementedError


async def main() -> None:
    file_ids = list(range(20))
    results = await download_all(file_ids, max_concurrent=3)

    assert len(results) == 20
    assert all(r.endswith("downloaded") for r in results)
    print(f"Скачано файлов: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
