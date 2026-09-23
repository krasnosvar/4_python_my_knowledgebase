"""
Решение упражнения 2: TTL-based инвалидация с обоснованным сроком жизни.
"""

from __future__ import annotations

import time

import redis

# Обоснование выбора TTL:
# Внешний API обновляет курс не чаще раза в 5 минут (300 секунд).
#   - Если взять TTL сильно МЕНЬШЕ 300с (например, 10с) — мы будем ходить во
#     внешний API в десятки раз чаще, чем у него вообще появляются новые
#     данные: кеш почти не даёт выигрыша, а внешний сервис получает лишнюю
#     нагрузку без всякой пользы (курс между этими вызовами не меняется).
#   - Если взять TTL сильно БОЛЬШЕ 300с (например, час) — есть риск отдавать
#     клиентам курс, устаревший на 55 минут, хотя новый уже давно доступен.
# 300 секунд (=5 минут, ровно интервал обновления источника) — разумный
# компромисс: мы никогда не опережаем реальную частоту обновления данных
# у источника, и при этом не ходим в API чаще, чем есть смысл.
EXCHANGE_RATE_TTL_SECONDS = 300


_EXTERNAL_API_CALL_COUNT = 0


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def slow_fetch_exchange_rate(base: str, target: str) -> float:
    global _EXTERNAL_API_CALL_COUNT
    _EXTERNAL_API_CALL_COUNT += 1
    time.sleep(0.3)
    fake_rates = {("USD", "EUR"): 0.92, ("EUR", "USD"): 1.09}
    return fake_rates.get((base, target), 1.0)


def cache_key_for(base: str, target: str) -> str:
    return f"exchange_rate:{base}:{target}"


def get_exchange_rate(r: redis.Redis, base: str, target: str, ttl_seconds: int) -> float:
    key = cache_key_for(base, target)

    cached = r.get(key)
    if cached is not None:
        return float(cached)

    rate = slow_fetch_exchange_rate(base, target)
    # ttl_seconds — параметр, а не константа EXCHANGE_RATE_TTL_SECONDS
    # напрямую: это позволяет тестировать поведение TTL с маленьким сроком
    # жизни, не дожидаясь реальных 5 минут в проверке ниже.
    r.set(key, str(rate), ex=ttl_seconds)
    return rate


def main() -> None:
    r = get_client()
    r.ping()
    key = cache_key_for("USD", "EUR")
    r.delete(key)

    print(f"Выбранный TTL для продакшена: {EXCHANGE_RATE_TTL_SECONDS} сек")

    print("\n=== Проверка, что TTL реально выставлен на ключе ===")
    get_exchange_rate(r, "USD", "EUR", EXCHANGE_RATE_TTL_SECONDS)
    ttl = r.ttl(key)
    print(f"TTL ключа сразу после записи: {ttl} сек")
    assert 0 < ttl <= EXCHANGE_RATE_TTL_SECONDS

    print("\n=== Проверка самостоятельного истечения кеша (короткий TTL для теста) ===")
    r.delete(key)
    test_ttl = 1
    calls_before = _EXTERNAL_API_CALL_COUNT

    get_exchange_rate(r, "USD", "EUR", test_ttl)
    get_exchange_rate(r, "USD", "EUR", test_ttl)
    calls_after_hit = _EXTERNAL_API_CALL_COUNT
    assert calls_after_hit == calls_before + 1, "Второй вызов должен был попасть в кеш (HIT)"

    time.sleep(test_ttl + 0.2)
    get_exchange_rate(r, "USD", "EUR", test_ttl)
    calls_after_expiry = _EXTERNAL_API_CALL_COUNT
    assert calls_after_expiry == calls_before + 2, (
        "После истечения TTL ожидался новый реальный вызов slow_fetch_exchange_rate"
    )

    print("OK: кеш действительно живёт ровно TTL секунд, не дольше и не короче.")


if __name__ == "__main__":
    main()
