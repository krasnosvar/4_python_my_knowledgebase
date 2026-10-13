"""
Паттерн rate limiting: ограничение частоты вызовов во времени
(token bucket) в дополнение к ограничению параллелизма (Semaphore).

Запуск: python main.py
"""
from __future__ import annotations

import asyncio
import time


class RateLimiter:
    """Не больше `rate` вызовов в секунду."""

    def __init__(self, rate: float) -> None:
        self._interval = 1.0 / rate
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = self._next_allowed - now
            if wait > 0:
                await asyncio.sleep(wait)
            self._next_allowed = max(now, self._next_allowed) + self._interval


async def call_api(limiter: RateLimiter, n: int, timestamps: list[float]) -> None:
    await limiter.acquire()
    timestamps.append(time.monotonic())
    print(f"вызов {n} в момент {timestamps[-1]:.3f}")


async def main() -> None:
    limiter = RateLimiter(rate=5)  # не больше 5 вызовов в секунду
    timestamps: list[float] = []

    start = time.monotonic()
    await asyncio.gather(*(call_api(limiter, i, timestamps) for i in range(10)))
    elapsed = time.monotonic() - start

    print(f"\n10 вызовов при лимите 5/сек заняли {elapsed:.2f}s (ожидаем ~2s)")
    assert elapsed >= 1.5, "rate limiter должен растянуть вызовы во времени"


if __name__ == "__main__":
    asyncio.run(main())
