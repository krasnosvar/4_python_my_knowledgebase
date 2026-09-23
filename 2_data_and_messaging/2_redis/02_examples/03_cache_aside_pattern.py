"""
Cache-aside (lazy loading) паттерн на практике: имитируем "медленную" БД
(time.sleep), оборачиваем чтение в get_user(), которая сначала проверяет
Redis, и на промахе идёт в "БД" и заполняет кеш с TTL. Демонстрируем разницу
по времени между холодным (cache miss) и тёплым (cache hit) вызовом, а
также инвалидацию через delete-on-write при обновлении данных.

Запуск:
    docker compose up -d
    pip install -r requirements.txt
    python 03_cache_aside_pattern.py
"""

from __future__ import annotations

import json
import time
from typing import Any

import redis

CACHE_TTL_SECONDS = 60
SIMULATED_DB_LATENCY = 0.4  # секунды — имитация "медленного" похода в БД

# "База данных" — просто словарь в памяти процесса, чтобы пример был
# самодостаточным и не требовал поднимать настоящую БД.
_FAKE_DB: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def slow_fetch_user_from_db(user_id: int) -> dict[str, Any] | None:
    """Имитация медленного запроса к реальной БД (сеть + диск + парсинг)."""
    time.sleep(SIMULATED_DB_LATENCY)
    return _FAKE_DB.get(user_id)


def cache_key_for(user_id: int) -> str:
    return f"user:{user_id}"


def get_user(r: redis.Redis, user_id: int) -> dict[str, Any] | None:
    """Cache-aside чтение: проверяем кеш, на промахе читаем "БД" и
    заполняем кеш с TTL, чтобы устаревшие данные не жили вечно."""
    key = cache_key_for(user_id)

    cached = r.get(key)
    if cached is not None:
        return json.loads(cached)  # cache HIT

    user = slow_fetch_user_from_db(user_id)  # cache MISS
    if user is not None:
        r.set(key, json.dumps(user), ex=CACHE_TTL_SECONDS)
    return user


def update_user(r: redis.Redis, user_id: int, **fields: Any) -> None:
    """Запись идёт напрямую в "БД", а кеш не обновляется значением — он
    просто удаляется (delete-on-write). Следующий get_user() увидит MISS,
    честно перечитает уже обновлённые данные из "БД" и сам заполнит кеш
    актуальным значением. Это надёжнее, чем пытаться записать новое
    значение в кеш прямо тут: не нужно гадать, не обогнала ли эта запись
    какую-то параллельную (см. раздел 5 теории про race condition)."""
    if user_id in _FAKE_DB:
        _FAKE_DB[user_id].update(fields)
    r.delete(cache_key_for(user_id))


def main() -> None:
    r = get_client()
    r.ping()
    r.delete(cache_key_for(1), cache_key_for(2))

    print("=== Холодный вызов (cache MISS -> идём в 'БД') ===")
    start = time.perf_counter()
    user = get_user(r, 1)
    elapsed_cold = time.perf_counter() - start
    print(f"Результат: {user}")
    print(f"Время: {elapsed_cold:.3f} сек (заплатили за SIMULATED_DB_LATENCY)")

    print("\n=== Тёплый вызов (cache HIT -> Redis) ===")
    start = time.perf_counter()
    user = get_user(r, 1)
    elapsed_warm = time.perf_counter() - start
    print(f"Результат: {user}")
    print(f"Время: {elapsed_warm:.4f} сек")

    speedup = elapsed_cold / elapsed_warm if elapsed_warm > 0 else float("inf")
    print(f"\nУскорение тёплого вызова относительно холодного: ~{speedup:.0f}x")

    print("\n=== Инвалидация при обновлении (delete-on-write) ===")
    print("Обновляем email пользователя 1 в 'БД'...")
    update_user(r, 1, email="alice+new@example.com")
    print("Ключ в кеше удалён. Следующий get_user() снова будет MISS:")

    start = time.perf_counter()
    user = get_user(r, 1)
    elapsed_after_update = time.perf_counter() - start
    print(f"Результат: {user}")
    print(f"Время: {elapsed_after_update:.3f} сек "
          f"(снова медленно — кеш пуст после инвалидации, это ожидаемо)")


if __name__ == "__main__":
    main()
