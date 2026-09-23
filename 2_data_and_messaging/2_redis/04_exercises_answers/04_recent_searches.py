"""
Решение упражнения 4: выбор правильной структуры данных.

Ответ на вопрос из задания:

  Естественная структура — List. Нам важен ПОРЯДОК (от нового к старому)
  и ограниченный размер (последние 10), а не уникальность значений
  (одинаковый поисковый запрос вполне может повторяться в истории). List
  даёт готовую пару операций именно под эту задачу: LPUSH добавляет новый
  элемент в начало за O(1), а LTRIM сразу после — обрезает список до
  первых 10 элементов, тоже за O(N) от размера обрезаемого хвоста, что
  здесь пренебрежимо мало.

  Почему НЕ Set: Set не хранит порядок вставки вообще, и он бы схлопнул
  повторяющиеся запросы в один и тот же элемент (уникальность — это плюс
  для тегов, но не то, что нужно для истории "что человек искал и когда").

  Почему НЕ String с JSON-массивом внутри: чтобы добавить один новый
  элемент и обрезать список, пришлось бы на каждый record_search делать
  GET (прочитать весь текущий JSON) -> распарсить в Python -> вставить
  элемент в начало списка -> обрезать до 10 -> сериализовать обратно ->
  SET. Это не только больше операций и данных гоняется туда-обратно по
  сети при каждом вызове, но и НЕ атомарно: если два запроса от одного
  пользователя прилетят почти одновременно, они оба прочитают одно и то
  же состояние, и один из них перезапишет результат другого — запись
  потеряется. LPUSH+LTRIM в Redis атомарны сами по себе, отдельная
  синхронизация не нужна.
"""

from __future__ import annotations

import redis


def get_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


MAX_RECENT_SEARCHES = 10


def key_for(user_id: int) -> str:
    return f"recent:searches:user:{user_id}"


def record_search(r: redis.Redis, user_id: int, query: str) -> None:
    key = key_for(user_id)
    r.lpush(key, query)
    # LTRIM оставляет индексы [0, MAX_RECENT_SEARCHES - 1] — то есть ровно
    # MAX_RECENT_SEARCHES самых свежих элементов (LPUSH кладёт новые в
    # начало, поэтому "первые N" всегда означает "N самых новых").
    r.ltrim(key, 0, MAX_RECENT_SEARCHES - 1)


def get_recent_searches(r: redis.Redis, user_id: int) -> list[str]:
    key = key_for(user_id)
    # 0..-1 = весь список; благодаря LTRIM в record_search он никогда не
    # превышает MAX_RECENT_SEARCHES элементов, поэтому диапазон можно не
    # ограничивать дополнительно здесь.
    return r.lrange(key, 0, -1)


def main() -> None:
    r = get_client()
    r.ping()
    user_id = 100
    r.delete(key_for(user_id))

    queries = [f"query-{i}" for i in range(1, 16)]
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
