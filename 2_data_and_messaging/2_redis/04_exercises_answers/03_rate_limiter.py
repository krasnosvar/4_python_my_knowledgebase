"""
Решение упражнения 3: sliding window rate limiter для API-эндпоинта.
"""

from __future__ import annotations

import time
import uuid

import redis


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


class SlidingWindowRateLimiter:
    """Ограничивает `limit` запросов за скользящее окно `window_seconds`
    секунд на один client_id, используя sorted set (score = timestamp)."""

    def __init__(self, r: redis.Redis, limit: int, window_seconds: float) -> None:
        self._r = r
        self._limit = limit
        self._window_seconds = window_seconds

    def _key_for(self, client_id: str) -> str:
        return f"ratelimit:endpoint:{client_id}"

    def allow(self, client_id: str) -> bool:
        key = self._key_for(client_id)
        now = time.time()
        window_start = now - self._window_seconds
        # uuid — чтобы два запроса, случайно попавшие на один и тот же
        # timestamp (или очень близкие), не "схлопнулись" в один и тот же
        # member sorted set: ZADD с одинаковым member перезаписывает score,
        # а не добавляет второй элемент, и мы бы недосчитали запросы.
        request_id = f"{now}:{uuid.uuid4().hex}"

        # Один pipeline — почти вся логика уезжает на сервер одним
        # round-trip'ом вместо четырёх последовательных.
        pipe = self._r.pipeline()
        pipe.zremrangebyscore(key, "-inf", window_start)  # выбросить устаревшее
        pipe.zadd(key, {request_id: now})                  # зафиксировать запрос
        pipe.zcard(key)                                     # сколько сейчас в окне
        pipe.expire(key, int(self._window_seconds) + 1)      # само-очистка простоя
        _, _, count, _ = pipe.execute()

        if count > self._limit:
            # Запрос не прошёл лимит — откатываем его же собственную запись,
            # иначе он будет "засорять" окно и мешать следующим проверкам.
            self._r.zrem(key, request_id)
            return False
        return True


def main() -> None:
    r = get_client()
    r.ping()

    limit = 3
    window_seconds = 5
    client_id = f"test-client-{uuid.uuid4().hex[:6]}"

    limiter = SlidingWindowRateLimiter(r, limit=limit, window_seconds=window_seconds)

    results = [limiter.allow(client_id) for _ in range(limit + 1)]
    print(f"Результаты {limit + 1} запросов подряд (limit={limit}): {results}")

    assert results[:limit] == [True] * limit, (
        f"Первые {limit} запросов должны быть разрешены"
    )
    assert results[limit] is False, (
        f"Запрос номер {limit + 1} (N+1-й) должен быть заблокирован"
    )

    print(f"\nOK: первые {limit} запроса разрешены, {limit + 1}-й корректно заблокирован.")


if __name__ == "__main__":
    main()
