"""Задание 2: перевод денег с корректной обработкой транзакции.

Стенд: тот же docker-compose из ../02_examples, та же схема (таблица
accounts). Запускайте после `docker compose up -d` и применения schema.sql
из ../02_examples/.

Нужно дописать transfer_money так, чтобы:
- списание и зачисление происходили в одной транзакции;
- при недостатке средств поднималось InsufficientFundsError и НИ ОДНА
  строка не менялась;
- при сбое между списанием и зачислением (см. simulate_crash_after_debit)
  в базе не оставалось частичного состояния -- то есть после отлова
  исключения баланс отправителя должен быть таким же, как до вызова.

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

    TODO:
    1. Открыть транзакцию (в psycopg3 она открывается неявно первым
       запросом -- явный BEGIN не обязателен, но не забудьте про
       commit()/rollback()).
    2. Прочитать текущий баланс отправителя с блокировкой строки
       (SELECT ... FOR UPDATE), чтобы конкурентный перевод с того же
       счёта не мог прочитать несогласованное значение.
    3. Если баланс меньше amount -- откатить транзакцию и поднять
       InsufficientFundsError, не изменив ни одной строки.
    4. Списать amount у from_name и зачислить amount на to_name.
    5. Если simulate_crash_after_debit=True -- поднять RuntimeError
       ПОСЛЕ списания, но ДО зачисления (это имитация сбоя приложения).
       Убедитесь, что в этом случае вызывающий код (или сама функция)
       откатывает транзакцию, и списание тоже отменяется -- то есть
       partial state в базе оставаться не должно.
    6. Если всё прошло успешно -- закоммитить транзакцию.
    """
    # TODO: реализовать
    raise NotImplementedError


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
