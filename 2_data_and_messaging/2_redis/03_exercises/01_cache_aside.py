"""
Упражнение 1: реализуйте cache-aside обёртку вокруг "медленной" функции.

См. задание в README.md (раздел 1).
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
    """Дано: имитация медленного похода в БД. Не изменяйте эту функцию."""
    time.sleep(0.4)
    return _FAKE_DB.get(product_id)


def cache_key_for(product_id: int) -> str:
    return f"product:{product_id}"


def cached_get_product(r: redis.Redis, product_id: int) -> dict[str, Any] | None:
    """
    TODO: реализовать cache-aside чтение:
      1. Проверить Redis по ключу cache_key_for(product_id).
      2. Если есть (cache HIT) — вернуть распарсенное значение, не вызывая
         slow_fetch_product вообще.
      3. Если нет (cache MISS) — вызвать slow_fetch_product, если результат
         не None — сохранить его в Redis с TTL = PRODUCT_CACHE_TTL_SECONDS,
         и вернуть результат.
    """
    raise NotImplementedError("TODO: реализовать cached_get_product")


def invalidate_product(r: redis.Redis, product_id: int) -> None:
    """
    TODO: удалить ключ кеша для этого товара (delete-on-write).
    Вызывается после гипотетического обновления товара в БД.
    """
    raise NotImplementedError("TODO: реализовать invalidate_product")


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
