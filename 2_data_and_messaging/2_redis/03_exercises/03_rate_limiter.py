"""
Упражнение 3: sliding window rate limiter для API-эндпоинта.

См. задание в README.md (раздел 3).
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
        """
        TODO: реализовать проверку лимита:
          1. Посчитать текущий timestamp (time.time()) и границу окна
             (now - self._window_seconds).
          2. Удалить из sorted set записи старше границы окна
             (ZREMRANGEBYSCORE).
          3. Добавить текущий запрос в sorted set (ZADD), member должен
             быть уникальным на каждый вызов (иначе разные запросы в один
             и тот же момент времени "схлопнутся" в один элемент) —
             используйте, например, f"{now}:{uuid.uuid4().hex}".
          4. Посчитать количество элементов в окне (ZCARD).
          5. Если count > self._limit — откатить добавленный элемент
             (ZREM) и вернуть False. Иначе вернуть True.
          6. Не забыть выставить EXPIRE на ключ, чтобы неактивные клиенты
             не оставляли ключи в Redis навсегда.
        """
        raise NotImplementedError("TODO: реализовать SlidingWindowRateLimiter.allow")


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
