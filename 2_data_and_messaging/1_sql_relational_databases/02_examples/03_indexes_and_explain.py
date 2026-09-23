"""Демонстрация влияния индекса на план запроса через EXPLAIN ANALYZE.

Запускает один и тот же фильтрующий запрос по orders.customer_id:
1. До создания индекса -- ожидаем Seq Scan по ~200 000 строкам таблицы orders.
2. После CREATE INDEX (+ ANALYZE) -- ожидаем Index Scan или Bitmap Heap Scan.

Запуск: python 03_indexes_and_explain.py
Предполагает, что schema.sql уже применён и в orders ~200 000 строк
(на маленькой таблице планировщик может честно выбрать Seq Scan даже
после создания индекса -- см. раздел про планировщик в 01_theory/README.md).
"""
from __future__ import annotations

import psycopg

from db_config import PSYCOPG_DSN

FILTER_QUERY = "SELECT * FROM orders WHERE customer_id = %s"
TARGET_CUSTOMER_ID = 777
INDEX_NAME = "idx_orders_customer_id"


def run_explain(conn: psycopg.Connection, label: str) -> str:
    with conn.cursor() as cur:
        cur.execute(f"EXPLAIN ANALYZE {FILTER_QUERY}", (TARGET_CUSTOMER_ID,))
        plan_lines = [row[0] for row in cur.fetchall()]
    plan_text = "\n".join(plan_lines)

    print(f"\n=== {label} ===")
    print(plan_text)

    if "Index Only Scan" in plan_text or "Index Scan" in plan_text or "Bitmap Heap Scan" in plan_text:
        print(">> Использован индекс")
    elif "Seq Scan" in plan_text:
        print(">> Индекс НЕ используется -- полное сканирование таблицы (Seq Scan)")
    return plan_text


def drop_index(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(f"DROP INDEX IF EXISTS {INDEX_NAME}")


def create_index(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(f"CREATE INDEX {INDEX_NAME} ON orders (customer_id)")


def main() -> None:
    with psycopg.connect(PSYCOPG_DSN, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM orders")
            (total,) = cur.fetchone()
        print(f"Всего строк в orders: {total}")

        drop_index(conn)
        run_explain(conn, "ДО создания индекса (ожидаем Seq Scan)")

        create_index(conn)
        # ANALYZE обновляет статистику планировщика после появления нового
        # индекса, чтобы cost-based optimizer сразу учитывал новый путь доступа.
        with conn.cursor() as cur:
            cur.execute("ANALYZE orders")
        run_explain(conn, "ПОСЛЕ создания индекса (ожидаем Index/Bitmap Scan)")


if __name__ == "__main__":
    main()
