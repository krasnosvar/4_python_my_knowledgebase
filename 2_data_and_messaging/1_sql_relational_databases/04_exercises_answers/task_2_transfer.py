"""Решение задания 2: перевод денег с корректной обработкой транзакции.

Ключевая идея: списание, проверка баланса и зачисление живут в ОДНОЙ
транзакции psycopg3 (она открывается неявно первым запросом и живёт до
явного commit()/rollback()). Любая ошибка до commit() -- будь то бизнес-
ошибка (недостаточно средств) или имитация сбоя приложения -- гасится
rollback(), который откатывает ВСЕ изменения транзакции разом, а не только
последнюю операцию. Поэтому частичного состояния (списали, но не
зачислили) в базе не остаётся ни в одном из сценариев.

Запуск: python task_2_transfer.py
"""
from __future__ import annotations

import os

import psycopg
from psycopg import Connection

PG_DSN = (
    f"host={os.getenv('PG_HOST', 'localhost')} "
    f"port={os.getenv('PG_PORT', '5432')} "
    f"dbname={os.getenv('PG_DB', 'kb_shop')} "
    f"user={os.getenv('PG_USER', 'kb_user')} "
    f"password={os.getenv('PG_PASSWORD', 'kb_password')}"
)


class InsufficientFundsError(Exception):
    """Не хватает денег на счёте для списания."""


def reset_demo_balances(conn: Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE accounts SET balance = CASE name
                WHEN 'Alice' THEN 1000.00
                WHEN 'Bob'   THEN 500.00
                WHEN 'Carol' THEN 250.00
                ELSE balance
            END
            WHERE name IN ('Alice', 'Bob', 'Carol')
            """
        )
    conn.commit()


def get_balance(conn: Connection, name: str) -> float:
    with conn.cursor() as cur:
        cur.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
        row = cur.fetchone()
    if row is None:
        raise ValueError(f"Счёт {name} не найден")
    return float(row[0])


def transfer_money(
    conn: Connection,
    from_name: str,
    to_name: str,
    amount: float,
    simulate_crash_after_debit: bool = False,
) -> None:
    """Перевести amount со счёта from_name на счёт to_name.

    FOR UPDATE на SELECT баланса отправителя не даёт двум конкурентным
    переводам с одного счёта прочитать один и тот же "старый" баланс и
    оба списать деньги, которых на самом деле уже не хватает (без этого
    возможна гонка: обе транзакции читают balance=100, обе видят "хватает
    на 80", обе списывают -- итоговый баланс уходит в минус, хотя
    формально каждая проверка была верной на момент чтения).
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT balance FROM accounts WHERE name = %s FOR UPDATE",
                (from_name,),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Счёт {from_name} не найден")
            current_balance = float(row[0])

            if current_balance < amount:
                raise InsufficientFundsError(
                    f"У {from_name} недостаточно средств: {current_balance} < {amount}"
                )

            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE name = %s",
                (amount, from_name),
            )

            if simulate_crash_after_debit:
                raise RuntimeError(
                    "Симулированный сбой между списанием и зачислением"
                )

            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE name = %s",
                (amount, to_name),
            )
    except Exception:
        # Любая ошибка внутри блока -- откатываем ВСЮ транзакцию целиком.
        # Это и есть Atomicity: списание, случившееся выше по коду, но ещё
        # не закоммиченное, откатывается вместе со всем остальным.
        conn.rollback()
        raise
    else:
        conn.commit()


if __name__ == "__main__":
    with psycopg.connect(PG_DSN) as conn:
        reset_demo_balances(conn)

        print("=== Сценарий 1: обычный перевод ===")
        transfer_money(conn, "Alice", "Bob", 200.00)
        print(f"Alice: {get_balance(conn, 'Alice')}, Bob: {get_balance(conn, 'Bob')}")

        print("\n=== Сценарий 2: недостаточно средств ===")
        balance_before = get_balance(conn, "Carol")
        try:
            transfer_money(conn, "Carol", "Bob", 10_000.00)
        except InsufficientFundsError as exc:
            print(f"Ожидаемая ошибка: {exc}")
        balance_after = get_balance(conn, "Carol")
        assert balance_before == balance_after, "Баланс не должен был измениться!"
        print("OK: баланс Carol не изменился")

        print("\n=== Сценарий 3: сбой между списанием и зачислением ===")
        alice_before = get_balance(conn, "Alice")
        bob_before = get_balance(conn, "Bob")
        try:
            transfer_money(conn, "Alice", "Bob", 100.00, simulate_crash_after_debit=True)
        except RuntimeError as exc:
            print(f"'Сбой': {exc}")
        alice_after = get_balance(conn, "Alice")
        bob_after = get_balance(conn, "Bob")
        assert alice_before == alice_after, "Списание должно было откатиться!"
        assert bob_before == bob_after, "Зачисления быть не должно!"
        print("OK: после сбоя не осталось частичного состояния")

        reset_demo_balances(conn)
