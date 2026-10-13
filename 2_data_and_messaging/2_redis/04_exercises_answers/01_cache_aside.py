"""
Решение упражнения 1: cache-aside обёртка вокруг "медленной" функции.
"""

from __future__ import annotations

import json
import time
from typing import Any

import redis

PRODUCT_CACHE_TTL_SECONDS = 300

_FAKE_DB: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Клавиатура", "price": 49.90},
    2: {"id": 2, "name": "Монитор", "price": 219.00},
}


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def slow_fetch_product(product_id: int) -> dict[str, Any] | None:
    time.sleep(0.4)
    return _FAKE_DB.get(product_id)


def cache_key_for(product_id: int) -> str:
    return f"product:{product_id}"


def cached_get_product(r: redis.Redis, product_id: int) -> dict[str, Any] | None:
    key = cache_key_for(product_id)

    # Сначала проверяем кеш — это единственное, что нужно сделать в
    # "горячем" пути (cache HIT). Никакого похода в БД, если значение есть.
    cached = r.get(key)
    if cached is not None:
        return json.loads(cached)

    # Cache MISS: идём в "БД" и на этом же ходу заполняем кеш, чтобы
    # следующий запрос за этим же товаром был уже быстрым. TTL защищает нас
    # от вечно устаревших данных, даже если где-то забудут вызвать
    # invalidate_product при обновлении товара.
    product = slow_fetch_product(product_id)
    if product is not None:
        r.set(key, json.dumps(product), ex=PRODUCT_CACHE_TTL_SECONDS)
    return product


def invalidate_product(r: redis.Redis, product_id: int) -> None:
    # Удаляем, а не перезаписываем новым значением: удаление корректно в
    # любом порядке событий, тогда как запись нового значения из write-пути
    # рискует проиграть гонку с параллельным читателем (см.
    # 01_theory/05_cache_invalidation.md).
    r.delete(cache_key_for(product_id))


def main() -> None:
    r = get_client()
    r.ping()
    r.delete(cache_key_for(1))

    print("=== Холодный вызов ===")
    start = time.perf_counter()
    product = cached_get_product(r, 1)
    elapsed_cold = time.perf_counter() - start
    print(f"Результат: {product}, время: {elapsed_cold:.3f}с")

    print("\n=== Тёплый вызов ===")
    start = time.perf_counter()
    product = cached_get_product(r, 1)
    elapsed_warm = time.perf_counter() - start
    print(f"Результат: {product}, время: {elapsed_warm:.4f}с")

    assert elapsed_warm < elapsed_cold / 2, (
        "Тёплый вызов должен быть значительно быстрее холодного — "
        "проверьте, что cached_get_product действительно читает из кеша "
        "при cache HIT, не вызывая slow_fetch_product."
    )
    print("\nOK: тёплый вызов заметно быстрее холодного.")

    print("\n=== Инвалидация ===")
    _FAKE_DB[1]["price"] = 39.90
    invalidate_product(r, 1)
    start = time.perf_counter()
    product = cached_get_product(r, 1)
    elapsed_after_invalidate = time.perf_counter() - start
    print(f"Результат: {product}, время: {elapsed_after_invalidate:.3f}с")

    assert product is not None and product["price"] == 39.90
    assert elapsed_after_invalidate > elapsed_warm, (
        "После инвалидации ожидался повторный поход в 'БД' (медленный вызов), "
        "проверьте invalidate_product."
    )
    print("\nOK: после инвалидации кеш честно перечитал обновлённые данные.")


if __name__ == "__main__":
    main()
