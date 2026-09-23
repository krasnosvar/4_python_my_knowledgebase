"""
Упражнение 2: TTL-based инвалидация с обоснованным сроком жизни.

См. задание в README.md (раздел 2). Сценарий: курс обмена валют от внешнего
API, который обновляется не чаще раза в 5 минут.
"""

from __future__ import annotations

import time

import redis

# TODO: выберите TTL для кеша курса валют и обоснуйте выбор комментарием
# прямо здесь. Подсказка: внешний API отдаёт новый курс не чаще, чем раз в
# 5 минут — подумайте, что произойдёт при TTL заметно меньше и заметно
# больше этого интервала.
EXCHANGE_RATE_TTL_SECONDS = None  # TODO: заменить на число секунд


_EXTERNAL_API_CALL_COUNT = 0  # для демонстрации — считаем реальные походы "во внешний API"


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def slow_fetch_exchange_rate(base: str, target: str) -> float:
    """Дано: имитация похода во внешний API курсов валют. Не изменяйте эту
    функцию — она также считает количество реальных вызовов в глобальной
    переменной, это нужно для проверки в конце файла."""
    global _EXTERNAL_API_CALL_COUNT
    _EXTERNAL_API_CALL_COUNT += 1
    time.sleep(0.3)
    fake_rates = {("USD", "EUR"): 0.92, ("EUR", "USD"): 1.09}
    return fake_rates.get((base, target), 1.0)


def cache_key_for(base: str, target: str) -> str:
    return f"exchange_rate:{base}:{target}"


def get_exchange_rate(r: redis.Redis, base: str, target: str, ttl_seconds: int) -> float:
    """
    TODO: реализовать cache-aside чтение курса валют:
      1. Проверить Redis по cache_key_for(base, target).
      2. При HIT — вернуть float(значение) без похода во внешний API.
      3. При MISS — вызвать slow_fetch_exchange_rate, сохранить результат
         в Redis с TTL = ttl_seconds (параметр, не константа — это нужно
         для теста ниже с уменьшенным TTL), вернуть результат.
    """
    raise NotImplementedError("TODO: реализовать get_exchange_rate")


def main() -> None:
    assert EXCHANGE_RATE_TTL_SECONDS is not None, (
        "Сначала выберите и обоснуйте EXCHANGE_RATE_TTL_SECONDS в коде выше."
    )

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
    test_ttl = 1  # искусственно маленький TTL только для этой проверки
    calls_before = _EXTERNAL_API_CALL_COUNT

    get_exchange_rate(r, "USD", "EUR", test_ttl)     # MISS -> реальный вызов API
    get_exchange_rate(r, "USD", "EUR", test_ttl)     # HIT -> без вызова API
    calls_after_hit = _EXTERNAL_API_CALL_COUNT
    assert calls_after_hit == calls_before + 1, "Второй вызов должен был попасть в кеш (HIT)"

    time.sleep(test_ttl + 0.2)
    get_exchange_rate(r, "USD", "EUR", test_ttl)     # ключ истёк -> снова MISS
    calls_after_expiry = _EXTERNAL_API_CALL_COUNT
    assert calls_after_expiry == calls_before + 2, (
        "После истечения TTL ожидался новый реальный вызов slow_fetch_exchange_rate"
    )

    print("OK: кеш действительно живёт ровно TTL секунд, не дольше и не короче.")


if __name__ == "__main__":
    main()
