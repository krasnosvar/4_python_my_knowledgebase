"""Решение: 08_rate_limited_api_client"""
from __future__ import annotations

import asyncio
import time


class RateLimiter:
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


async def main() -> None:
    checks_passed = 0
    total_checks = 2

    limiter = RateLimiter(rate=4)
    timestamps: list[float] = []

    start = time.monotonic()
    await asyncio.gather(*(call_api(limiter, i, timestamps) for i in range(12)))
    elapsed = time.monotonic() - start

    assert elapsed >= 2.5, f"rate limiter не сработал, elapsed={elapsed:.2f}"
    checks_passed += 1
    assert len(timestamps) == 12
    checks_passed += 1

    print(f"12 вызовов при лимите 4/сек заняли {elapsed:.2f}s")
    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    asyncio.run(main())
