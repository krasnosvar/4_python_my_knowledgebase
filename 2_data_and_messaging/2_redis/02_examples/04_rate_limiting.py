"""
Два способа ограничения частоты запросов (rate limiting) в Redis:

1. fixed_window_allow  — INCR + EXPIRE, дёшево, но с изъяном на границе окна.
2. sliding_window_allow — sorted set с timestamp'ами, точнее, но дороже.

В конце main() воспроизводится ровно тот сценарий "всплеска на границе
окна", который описан в теории: два всплеска запросов, посланных вплотную
к границе fixed-window окна, суммарно проходят почти вдвое больше лимита у
fixed window, тогда как sliding window честно отклоняет лишние запросы,
потому что видит их в одном и том же скользящем окне.

Запуск:
    docker compose up -d
    pip install -r requirements.txt
    python 04_rate_limiting.py
"""

from __future__ import annotations

import time
import uuid

import redis


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def fixed_window_allow(r: redis.Redis, identity: str, limit: int, window_seconds: int) -> bool:
    """Fixed window counter: считаем запросы в текущем "календарном" окне
    (например, текущие N секунд от начала эпохи, поделенные на размер окна).
    Дёшево (одна INCR), но окно жёстко сбрасывается, а не "едет" во времени —
    отсюда возможность двойного всплеска на стыке двух окон."""
    window_id = int(time.time() // window_seconds)
    key = f"ratelimit:fixed:{identity}:{window_id}"

    count = r.incr(key)
    if count == 1:
        # TTL выставляем только при создании счётчика (первый INCR), чтобы
        # не продлевать жизнь ключа на каждый последующий запрос.
        r.expire(key, window_seconds)

    return count <= limit


def sliding_window_allow(r: redis.Redis, identity: str, limit: int, window_seconds: int) -> bool:
    """Sliding window через sorted set: каждый запрос — элемент со
    score = его timestamp. Окно всегда "последние window_seconds секунд от
    текущего момента", а не привязано к границам календарного окна."""
    key = f"ratelimit:sliding:{identity}"
    now = time.time()
    window_start = now - window_seconds
    request_id = f"{now}:{uuid.uuid4().hex[:8]}"

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, "-inf", window_start)  # выкинуть устаревшие
    pipe.zadd(key, {request_id: now})                  # зафиксировать запрос
    pipe.zcard(key)                                     # сколько в окне сейчас
    pipe.expire(key, window_seconds)                    # само-очистка простоя
    _, _, count, _ = pipe.execute()

    if count > limit:
        r.zrem(key, request_id)  # откатываем "неудавшийся" запрос
        return False
    return True


def wait_until_shortly_before_window_boundary(window_seconds: int, buffer: float = 0.05) -> None:
    """Ждёт до момента, отстоящего от следующей границы fixed-window окна
    на `buffer` секунд — чтобы следующий всплеск запросов гарантированно
    попал вплотную к границе."""
    now = time.time()
    remainder = now % window_seconds
    time_to_wait = window_seconds - remainder - buffer
    if time_to_wait > 0:
        time.sleep(time_to_wait)


def demo_boundary_burst(r: redis.Redis) -> None:
    window_seconds = 2
    limit = 5
    run_id = uuid.uuid4().hex[:6]  # чтобы повторные запуски скрипта не мешали друг другу
    fixed_identity = f"demo-fixed-{run_id}"
    sliding_identity = f"demo-sliding-{run_id}"

    print(f"=== Всплеск на границе окна (limit={limit}, window={window_seconds}с) ===\n")

    print("Ждём момент вплотную к границе fixed-window окна...")
    wait_until_shortly_before_window_boundary(window_seconds)

    print(f"\n-- Burst 1: {limit} запросов вплотную ДО границы окна --")
    fixed_results_1 = [fixed_window_allow(r, fixed_identity, limit, window_seconds) for _ in range(limit)]
    sliding_results_1 = [sliding_window_allow(r, sliding_identity, limit, window_seconds) for _ in range(limit)]
    print("fixed_window_allow  ->", fixed_results_1)
    print("sliding_window_allow ->", sliding_results_1)

    # Небольшая пауза, чтобы гарантированно пересечь границу окна.
    time.sleep(0.15)

    print(f"\n-- Burst 2: ещё {limit} запросов сразу ПОСЛЕ границы окна --")
    fixed_results_2 = [fixed_window_allow(r, fixed_identity, limit, window_seconds) for _ in range(limit)]
    sliding_results_2 = [sliding_window_allow(r, sliding_identity, limit, window_seconds) for _ in range(limit)]
    print("fixed_window_allow  ->", fixed_results_2)
    print("sliding_window_allow ->", sliding_results_2)

    total_allowed_fixed = sum(fixed_results_1) + sum(fixed_results_2)
    total_allowed_sliding = sum(sliding_results_1) + sum(sliding_results_2)

    print(f"\nИтого за ~0.2 секунды реального времени (лимит = {limit} на {window_seconds}с):")
    print(f"  fixed window разрешил:   {total_allowed_fixed} запросов "
          f"{'(изъян: почти 2x лимита!)' if total_allowed_fixed > limit else ''}")
    print(f"  sliding window разрешил: {total_allowed_sliding} запросов "
          f"{'(корректно ограничил, несмотря на границу)' if total_allowed_sliding <= limit else ''}")


def main() -> None:
    r = get_client()
    r.ping()
    demo_boundary_burst(r)


if __name__ == "__main__":
    main()
