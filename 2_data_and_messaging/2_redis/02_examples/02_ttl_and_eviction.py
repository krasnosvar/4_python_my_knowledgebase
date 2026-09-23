"""
Демонстрация TTL (истечение ключей) и политик вытеснения (eviction policies)
при нехватке памяти.

Часть 1 показывает базовые операции с TTL: SET с истечением, EXPIRE,
проверку оставшегося времени (TTL) и снятие TTL (PERSIST).

Часть 2 честно ФОРСИРУЕТ реальное вытеснение: временно выставляет очень
маленький maxmemory на сервере и заливает больше данных, чем помещается,
чтобы увидеть в INFO разницу между "сколько ключей записали" и "сколько
реально осталось" при allkeys-lru. Это меняет конфигурацию Redis
временно и в конце скрипта возвращает её к безопасному состоянию
(maxmemory 0 = без лимита, noeviction) — если параллельно с этим скриптом
кто-то запускает другие примеры на том же инстансе, они на короткое время
тоже попадут под ограничение памяти. Для учебного docker-compose из этого
раздела это не проблема.

Запуск:
    docker compose up -d
    pip install -r requirements.txt
    python 02_ttl_and_eviction.py
"""

from __future__ import annotations

import time

import redis


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def demo_ttl_basics(r: redis.Redis) -> None:
    print("=== TTL: базовые операции ===")

    r.set("session:demo", "<данные сессии>", ex=5)
    print("SET session:demo ... EX 5")
    print("TTL сразу после SET ->", r.ttl("session:demo"), "сек")

    time.sleep(2)
    print("TTL через 2 секунды ->", r.ttl("session:demo"), "сек (уменьшился)")

    r.persist("session:demo")
    print("PERSIST session:demo -> сняли TTL")
    print("TTL после PERSIST ->", r.ttl("session:demo"), "(-1 = ключ без TTL)")

    r.expire("session:demo", 100)
    print("EXPIRE session:demo 100 -> снова выставили TTL")
    print("TTL сейчас ->", r.ttl("session:demo"))

    r.delete("session:no-such-key")
    print("TTL несуществующего ключа ->", r.ttl("session:no-such-key"), "(-2 = ключа нет)")

    print("\nИтог: -1 значит 'ключ есть, TTL не установлен', "
          "-2 значит 'ключа нет вообще' (истёк или никогда не создавался).")


def demo_eviction(r: redis.Redis) -> None:
    print("\n=== Eviction: что происходит при нехватке памяти ===")

    original_maxmemory = r.config_get("maxmemory")["maxmemory"]
    original_policy = r.config_get("maxmemory-policy")["maxmemory-policy"]
    print(f"Исходный maxmemory={original_maxmemory!r}, "
          f"maxmemory-policy={original_policy!r} (сохраняем, чтобы вернуть)")

    prefix = "evict_demo:"
    # На всякий случай подчищаем ключи от предыдущего запуска скрипта.
    for key in r.scan_iter(match=f"{prefix}*"):
        r.delete(key)

    try:
        # Ограничиваем память небольшим значением и включаем LRU-вытеснение
        # среди всех ключей — типичная конфигурация "чистого кеша". Лимит
        # не может быть слишком маленьким: сам Redis (пустая база, буферы
        # клиентов, служебные структуры) уже занимает 1-2 МБ памяти даже
        # без единого нашего ключа, и если maxmemory меньше этого базового
        # расхода — сервер начнёт отказывать в записи ещё ДО того, как
        # дойдёт до вытеснения наших ключей, что смажет всю демонстрацию.
        r.config_set("maxmemory", "20mb")
        r.config_set("maxmemory-policy", "allkeys-lru")
        print("CONFIG SET maxmemory 20mb / maxmemory-policy allkeys-lru")

        payload = "x" * 2000  # ~2 КБ на значение
        total_to_write = 15000  # суммарно ~30 МБ — заведомо больше лимита в 20 МБ

        for i in range(total_to_write):
            r.set(f"{prefix}{i}", payload)

        survived = sum(1 for _ in r.scan_iter(match=f"{prefix}*"))
        info = r.info("stats")
        evicted = info.get("evicted_keys", "н/д")

        print(f"Записали ключей: {total_to_write}")
        print(f"Реально осталось в базе (SCAN по префиксу): {survived}")
        print(f"evicted_keys по данным INFO stats (с последнего рестарта сервера): {evicted}")
        print(
            "\nВывод: с allkeys-lru Redis не отклонил запись и не упал — он "
            "молча вытеснил наименее недавно использованные ключи, чтобы "
            "освободить место под новые. Для сравнения: с maxmemory-policy "
            "noeviction эти же SET начали бы падать с ошибкой "
            "'OOM command not allowed' при достижении лимита."
        )
    finally:
        # Возвращаем конфигурацию сервера в исходное состояние.
        r.config_set("maxmemory", original_maxmemory or "0")
        r.config_set("maxmemory-policy", original_policy or "noeviction")
        for key in r.scan_iter(match=f"{prefix}*"):
            r.delete(key)
        print(f"\nКонфигурация восстановлена: maxmemory={original_maxmemory or '0'}, "
              f"maxmemory-policy={original_policy or 'noeviction'}")


def main() -> None:
    r = get_client()
    r.ping()
    demo_ttl_basics(r)
    demo_eviction(r)


if __name__ == "__main__":
    main()
