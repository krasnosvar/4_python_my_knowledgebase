"""
Задача: реализовать RateLimiter (token bucket) и использовать его, чтобы
сделать 12 конкурентных "вызовов API" с ограничением не более 4 вызовов
в секунду. Нужно доказать, что общее время выполнения соответствует лимиту.

Запусти: python main.py
"""
from __future__ import annotations

import asyncio
import time


class RateLimiter:
    def __init__(self, rate: float) -> None:
        self._interval = 1.0 / rate
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def acquire(self) -> None:
        """
        TODO: под self._lock посчитать, сколько нужно подождать, чтобы
        не превысить self._interval между вызовами (см. паттерн rate
        limiting в теории/примерах), и обновить self._next_allowed.
        """
        raise NotImplementedError


async def call_api(limiter: RateLimiter, n: int, timestamps: list[float]) -> None:
    await limiter.acquire()
    timestamps.append(time.monotonic())


async def main() -> None:
    limiter = RateLimiter(rate=4)
    timestamps: list[float] = []

    start = time.monotonic()
    await asyncio.gather(*(call_api(limiter, i, timestamps) for i in range(12)))
    elapsed = time.monotonic() - start

    # 12 вызовов при лимите 4/сек должны занять не меньше ~2.75s (11 интервалов по 0.25s)
    assert elapsed >= 2.5, f"rate limiter не сработал, elapsed={elapsed:.2f}"
    assert len(timestamps) == 12

    print(f"12 вызовов при лимите 4/сек заняли {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
