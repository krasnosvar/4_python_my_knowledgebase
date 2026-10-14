"""Решение задания 06: pessimistic vs optimistic locking.

decrement_stock_pessimistic берёт блокировку строки товара сразу при
чтении (SELECT ... FOR UPDATE) -- конкурентные вызовы для того же товара
физически ждут в очереди на уровне БД, поэтому гонка невозможна в принципе,
но под высокой конкуренцией это дороже по времени (потоки блокируют друг
друга).

decrement_stock_optimistic не блокирует ничего заранее: читает stock и
version, пытается обновить строку с условием "version не изменилась с
момента чтения", и если кто-то опередил (rowcount == 0) -- просто повторяет
попытку с начала. Под высокой конкуренцией часть попыток проигрывает гонку
и уходит в retry, но ни один поток не простаивает в ожидании чужой
блокировки -- он либо сразу побеждает, либо сразу узнаёт о проигрыше и
пробует снова.

Запуск: python 06_locking.py
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
    """Списать 1 единицу товара через SELECT ... FOR UPDATE."""
    with psycopg.connect(PG_DSN) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT stock FROM products WHERE name = %s FOR UPDATE",
                    (product_name,),
                )
                (stock,) = cur.fetchone()

                if stock <= 0:
                    conn.rollback()
                    return False

                cur.execute(
                    "UPDATE products SET stock = stock - 1 WHERE name = %s",
                    (product_name,),
                )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise


def decrement_stock_optimistic(product_name: str, max_retries: int = 20) -> bool:
    """Списать 1 единицу товара через столбец version (optimistic locking)."""
    for _ in range(max_retries):
        with psycopg.connect(PG_DSN, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT stock, version FROM products WHERE name = %s",
                    (product_name,),
                )
                stock, version = cur.fetchone()

                if stock <= 0:
                    return False

                cur.execute(
                    """
                    UPDATE products
                    SET stock = stock - 1, version = version + 1
                    WHERE name = %s AND version = %s
                    """,
                    (product_name, version),
                )
                if cur.rowcount == 1:
                    # Никто не успел обновить строку между нашим SELECT
                    # и UPDATE -- версия совпала, списание прошло.
                    return True
                # rowcount == 0: кто-то опередил (version уже другая).
                # Повторяем попытку с чтения актуального состояния.
    return False


def run_concurrent_demo(decrement_fn, initial_stock: int, workers: int) -> int:
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
