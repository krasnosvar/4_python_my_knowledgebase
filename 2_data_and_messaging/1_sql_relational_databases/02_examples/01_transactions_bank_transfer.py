"""Демонстрация ACID на примере банковского перевода.

Показывает:
1. Как перевод "списать у одного, зачислить другому" в ОДНОЙ транзакции
   гарантирует, что применятся либо обе операции, либо ни одна (Atomicity).
2. Что происходит, если сделать то же самое ДВУМЯ отдельными
   автокоммитными операциями: сбой между ними оставляет базу в
   противоречивом состоянии (деньги "теряются").
3. Явный rollback при недостатке средств (проверка инварианта
   "баланс не может уйти в минус" -- это же гарантирует и CHECK в schema.sql).

Запуск: python 01_transactions_bank_transfer.py
Перед запуском: docker compose up -d, затем применить schema.sql (см. README.md).
"""
from __future__ import annotations

import psycopg
from psycopg import Connection

from db_config import PSYCOPG_DSN


class InsufficientFundsError(Exception):
    """Не хватает денег на счёте для списания."""


def reset_demo_balances(conn: Connection) -> None:
    """Возвращает тестовые счета в исходное состояние перед демонстрацией."""
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


def print_balances(conn: Connection, label: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT name, balance FROM accounts WHERE name IN ('Alice', 'Bob', 'Carol') ORDER BY name"
        )
        rows = cur.fetchall()
    print(f"\n--- {label} ---")
    for name, balance in rows:
        print(f"  {name}: {balance}")


def transfer_money(conn: Connection, from_name: str, to_name: str, amount: float) -> None:
    """Атомарный перевод денег между счетами.

    Обе операции (списание и зачисление) выполняются в рамках одной
    транзакции: psycopg3 по умолчанию не в autocommit-режиме, поэтому
    транзакция открывается неявно первым запросом и живёт до explicit
    commit()/rollback(). Если баланс отправителя не позволяет списание,
    транзакция откатывается целиком -- ни списание, ни зачисление
    не применяются (Atomicity + Consistency: CHECK(balance >= 0) в БД --
    последняя линия обороны, но мы проверяем условие заранее в коде,
    чтобы вернуть осмысленную ошибку, а не голое исключение о constraint).
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT balance FROM accounts WHERE name = %s FOR UPDATE",
            (from_name,),
        )
        row = cur.fetchone()
        if row is None:
            conn.rollback()
            raise ValueError(f"Счёт {from_name} не найден")
        current_balance = row[0]

        if current_balance < amount:
            # Явный rollback: транзакция отменяется целиком, включая
            # блокировку строки, взятую SELECT ... FOR UPDATE.
            conn.rollback()
            raise InsufficientFundsError(
                f"У {from_name} недостаточно средств: {current_balance} < {amount}"
            )

        cur.execute(
            "UPDATE accounts SET balance = balance - %s WHERE name = %s",
            (amount, from_name),
        )
        cur.execute(
            "UPDATE accounts SET balance = balance + %s WHERE name = %s",
            (amount, to_name),
        )

    # Atomicity: обе строки меняются одновременно, либо не меняется ни одна.
    conn.commit()


def transfer_money_unsafe_autocommit(
    conn: Connection,
    from_name: str,
    to_name: str,
    amount: float,
    simulate_crash: bool,
) -> None:
    """Тот же перевод, но БЕЗ единой транзакции -- антипаттерн для контраста.

    В autocommit-режиме каждый execute() коммитится сам по себе сразу после
    выполнения. Если между списанием и зачислением приложение упадёт
    (сеть, OOM, перезапуск пода) -- деньги у отправителя уже списаны, а
    получателю ещё не зачислены. Деньги "потерялись": нарушена Atomicity.
    """
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE name = %s",
                (amount, from_name),
            )
            # Эта строка уже закоммичена в БД -- откатить её отсюда нельзя.

            if simulate_crash:
                raise RuntimeError(
                    "Симулированный сбой между списанием и зачислением "
                    "(например, приложение упало или потеряло сеть)"
                )

            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE name = %s",
                (amount, to_name),
            )
    finally:
        conn.autocommit = False


def main() -> None:
    with psycopg.connect(PSYCOPG_DSN) as conn:
        reset_demo_balances(conn)
        print_balances(conn, "Исходное состояние")

        print("\n=== 1. Корректный перевод в одной транзакции ===")
        transfer_money(conn, "Alice", "Bob", 200.00)
        print_balances(conn, "После перевода Alice -> Bob (200), сумма сохранена")

        print("\n=== 2. Перевод с недостатком средств: rollback ===")
        try:
            transfer_money(conn, "Carol", "Bob", 10_000.00)
        except InsufficientFundsError as exc:
            print(f"Ожидаемая ошибка: {exc}")
        print_balances(conn, "После неудачной попытки (баланс не изменился)")

        print("\n=== 3. Антипаттерн: два отдельных autocommit-запроса ===")
        reset_demo_balances(conn)
        try:
            transfer_money_unsafe_autocommit(conn, "Alice", "Bob", 200.00, simulate_crash=True)
        except RuntimeError as exc:
            print(f"'Сбой' приложения: {exc}")
        print_balances(
            conn,
            "После 'сбоя' -- у Alice деньги списаны, Bob их НЕ получил (данные испорчены)",
        )

        reset_demo_balances(conn)
        print("\nБалансы возвращены в исходное состояние.")


if __name__ == "__main__":
    main()
