"""Задание 4 (опционально): pessimistic vs optimistic locking.

Стенд: тот же docker-compose из ../02_examples, та же схема (таблица
products со столбцами stock и version). Запускайте после
`docker compose up -d` и применения schema.sql из ../02_examples/.

Сценарий: несколько потоков одновременно пытаются списать 1 единицу товара
со склада. Нужно реализовать два способа сделать это безопасно под
конкуренцией и убедиться, что stock никогда не уходит в минус.

Запуск: python task_4_locking.py
"""
from __future__ import annotations

import os
import threading
import time

import psycopg

PG_DSN = (
    f"host={os.getenv('PG_HOST', 'localhost')} "
    f"port={os.getenv('PG_PORT', '5432')} "
    f"dbname={os.getenv('PG_DB', 'kb_shop')} "
    f"user={os.getenv('PG_USER', 'kb_user')} "
    f"password={os.getenv('PG_PASSWORD', 'kb_password')}"
)

PRODUCT_NAME = "Клавиатура"


def reset_stock(product_name: str, stock: int) -> None:
    with psycopg.connect(PG_DSN, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE products SET stock = %s, version = 1 WHERE name = %s",
                (stock, product_name),
            )


def get_stock(product_name: str) -> int:
    with psycopg.connect(PG_DSN, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT stock FROM products WHERE name = %s", (product_name,))
            (stock,) = cur.fetchone()
    return stock


def decrement_stock_pessimistic(product_name: str) -> bool:
    """Списать 1 единицу товара через SELECT ... FOR UPDATE.

    TODO:
    1. Открыть транзакцию (новое соединение на вызов -- это ОК, имитируем
       отдельный процесс/запрос).
    2. SELECT stock FROM products WHERE name = %s FOR UPDATE -- это
       заблокирует строку до конца транзакции; конкурентные вызовы этой же
       функции для того же товара будут ждать здесь своей очереди.
    3. Если stock <= 0 -- откатить транзакцию и вернуть False (списывать
       нечего).
    4. Иначе UPDATE products SET stock = stock - 1 WHERE name = %s,
       закоммитить и вернуть True.
    """
    # TODO: реализовать
    raise NotImplementedError


def decrement_stock_optimistic(product_name: str, max_retries: int = 5) -> bool:
    """Списать 1 единицу товара через столбец version (optimistic locking).

    TODO:
    1. Прочитать текущие stock и version БЕЗ блокировки (обычный SELECT).
    2. Если stock <= 0 -- вернуть False.
    3. Выполнить UPDATE products SET stock = stock - 1, version = version + 1
       WHERE name = %s AND version = %s (то самое значение version, что
       прочитали на шаге 1).
    4. Проверить количество затронутых строк (cur.rowcount). Если 0 --
       значит, кто-то другой обновил строку первым; нужно повторить
       попытку с начала (заново прочитать stock/version), но не более
       max_retries раз. Если retries исчерпаны -- вернуть False.
    5. Если UPDATE затронул 1 строку -- закоммитить и вернуть True.
    """
    # TODO: реализовать
    raise NotImplementedError


def run_concurrent_demo(decrement_fn, initial_stock: int, workers: int) -> int:
    """Запускает `workers` потоков, каждый пытается списать 1 единицу
    товара через decrement_fn. Возвращает итоговый stock в БД."""
    reset_stock(PRODUCT_NAME, initial_stock)

    def worker() -> None:
        decrement_fn(PRODUCT_NAME)

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    final_stock = get_stock(PRODUCT_NAME)
    print(f"  workers={workers}, initial_stock={initial_stock}, "
          f"final_stock={final_stock}, elapsed={elapsed:.3f}s")
    return final_stock


if __name__ == "__main__":
    print("=== Pessimistic locking (SELECT ... FOR UPDATE) ===")
    final = run_concurrent_demo(decrement_stock_pessimistic, initial_stock=5, workers=10)
    assert final >= 0, "Сток не должен уходить в минус!"
    assert final == 0, "При 10 воркерах на 5 единиц стока итог должен быть 0"

    print("\n=== Optimistic locking (version column) ===")
    final = run_concurrent_demo(decrement_stock_optimistic, initial_stock=5, workers=10)
    assert final >= 0, "Сток не должен уходить в минус!"
    assert final == 0, "При 10 воркерах на 5 единиц стока итог должен быть 0"

    print("\nOK: оба варианта дают корректный итоговый stock под конкуренцией")
