"""
Демонстрация основных структур данных Redis через redis-py: string, hash,
list, set и sorted set. Каждый блок выполняет несколько операций и печатает
результат, чтобы поведение было видно сразу, без необходимости открывать
redis-cli отдельно.

Запуск:
    docker compose up -d
    pip install -r requirements.txt
    python 01_data_structures.py
"""

from __future__ import annotations

import redis


def get_client() -> redis.Redis:
    """Создаёт клиент redis-py. decode_responses=True — чтобы получать
    обычные str, а не bytes, что удобнее для учебных примеров."""
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def demo_string(r: redis.Redis) -> None:
    print("\n=== String ===")
    r.set("user:100:name", "Alice")
    print("SET user:100:name Alice")
    print("GET user:100:name ->", r.get("user:100:name"))

    r.delete("views:article:42")
    r.incr("views:article:42")
    r.incrby("views:article:42", 10)
    print("INCR + INCRBY views:article:42 ->", r.get("views:article:42"))

    r.setex("session:abc123", 30, "<session-data>")
    print("SETEX session:abc123 30 <...> -> TTL:", r.ttl("session:abc123"), "сек")


def demo_hash(r: redis.Redis) -> None:
    print("\n=== Hash ===")
    key = "user:100"
    r.delete(key)
    r.hset(key, mapping={"name": "Alice", "email": "alice@example.com", "age": "25"})
    print("HSET user:100 name/email/age")
    print("HGET user:100 name ->", r.hget(key, "name"))
    print("HGETALL user:100 ->", r.hgetall(key))

    r.hincrby(key, "login_count", 1)
    r.hincrby(key, "login_count", 1)
    print("HINCRBY login_count дважды ->", r.hget(key, "login_count"))


def demo_list(r: redis.Redis) -> None:
    print("\n=== List (как очередь последних поисков) ===")
    key = "recent:searches:user:100"
    r.delete(key)

    for query in ["redis", "python asyncio", "fastapi vs django", "sql joins"]:
        r.lpush(key, query)
        r.ltrim(key, 0, 9)  # держим не больше 10 последних запросов

    print("LRANGE recent:searches:user:100 0 -1 (от новых к старым) ->")
    print(" ", r.lrange(key, 0, -1))

    print("LLEN ->", r.llen(key))

    print("\n=== List (как простая очередь задач) ===")
    queue_key = "queue:tasks"
    r.delete(queue_key)
    r.rpush(queue_key, "task-1", "task-2", "task-3")
    print("RPUSH task-1 task-2 task-3")
    print("LPOP ->", r.lpop(queue_key), "(забрали самую старую задачу — FIFO)")
    print("Осталось в очереди ->", r.lrange(queue_key, 0, -1))


def demo_set(r: redis.Redis) -> None:
    print("\n=== Set (теги статьи) ===")
    key = "tags:article:42"
    r.delete(key)
    r.sadd(key, "redis", "caching", "python")
    r.sadd(key, "redis")  # дубликат, будет проигнорирован
    print("SADD redis caching python (+ повтор redis)")
    print("SMEMBERS ->", r.smembers(key))
    print("SCARD (количество уникальных тегов) ->", r.scard(key))
    print("SISMEMBER 'redis' ->", r.sismember(key, "redis"))
    print("SISMEMBER 'kafka' ->", r.sismember(key, "kafka"))

    other_key = "tags:article:43"
    r.delete(other_key)
    r.sadd(other_key, "python", "web", "django")
    print("\nПересечение тегов двух статей (общие интересы читателей):")
    print("SINTER ->", r.sinter(key, other_key))


def demo_sorted_set(r: redis.Redis) -> None:
    print("\n=== Sorted Set (лидерборд) ===")
    key = "leaderboard"
    r.delete(key)
    r.zadd(key, {"alice": 1100, "bob": 950, "charlie": 920, "diana": 850})
    print("ZADD alice=1100 bob=950 charlie=920 diana=850")

    print("Топ-3 (ZREVRANGE ... WITHSCORES) ->")
    for member, score in r.zrevrange(key, 0, 2, withscores=True):
        print(f"  {member}: {int(score)}")

    rank = r.zrevrank(key, "bob")
    print(f"Позиция bob в таблице (0 = первое место) -> {rank}")

    r.zincrby(key, 200, "bob")
    new_rank = r.zrevrank(key, "bob")
    print(f"После ZINCRBY bob +200: новая позиция -> {new_rank}")


def main() -> None:
    r = get_client()
    r.ping()
    demo_string(r)
    demo_hash(r)
    demo_list(r)
    demo_set(r)
    demo_sorted_set(r)


if __name__ == "__main__":
    main()
