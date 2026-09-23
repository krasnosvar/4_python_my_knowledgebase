"""
Упражнение 4: выбор правильной структуры данных.

Задача: хранить 10 последних поисковых запросов каждого пользователя,
от нового к старому, без неограниченного роста истории.

TODO: перед тем как писать код, ответьте здесь комментарием:
  - Какая структура данных Redis для этого естественна и почему?
  - Почему НЕ подходит Set? (подсказка: подумайте про порядок и дубликаты)
  - Почему НЕ String с JSON-массивом внутри? (подсказка: подумайте, что
    придётся делать при каждой новой записи, чтобы добавить один элемент
    и обрезать список до 10 — сколько операций и насколько это атомарно)

Ваш ответ:
    TODO: ...
"""

from __future__ import annotations

import redis


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


MAX_RECENT_SEARCHES = 10


def key_for(user_id: int) -> str:
    return f"recent:searches:user:{user_id}"


def record_search(r: redis.Redis, user_id: int, query: str) -> None:
    """
    TODO: записать новый поисковый запрос так, чтобы:
      - самый новый запрос был первым при последующем чтении;
      - в списке хранилось не больше MAX_RECENT_SEARCHES элементов.
    """
    raise NotImplementedError("TODO: реализовать record_search")


def get_recent_searches(r: redis.Redis, user_id: int) -> list[str]:
    """
    TODO: вернуть последние поисковые запросы пользователя,
    от самого нового к самому старому.
    """
    raise NotImplementedError("TODO: реализовать get_recent_searches")


def main() -> None:
    r = get_client()
    r.ping()
    user_id = 100
    r.delete(key_for(user_id))

    queries = [f"query-{i}" for i in range(1, 16)]  # 15 запросов подряд
    for q in queries:
        record_search(r, user_id, q)

    recent = get_recent_searches(r, user_id)
    print(f"Последние запросы пользователя {user_id}: {recent}")

    assert len(recent) == MAX_RECENT_SEARCHES, (
        f"Ожидалось ровно {MAX_RECENT_SEARCHES} запросов, получили {len(recent)}"
    )
    expected = list(reversed(queries[-MAX_RECENT_SEARCHES:]))
    assert recent == expected, f"Ожидался порядок {expected}, получили {recent}"

    print(f"\nOK: хранится ровно {MAX_RECENT_SEARCHES} последних запросов "
          f"в правильном порядке (от нового к старому).")


if __name__ == "__main__":
    main()
