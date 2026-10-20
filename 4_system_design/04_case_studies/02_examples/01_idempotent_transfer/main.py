"""
Пример 01: идемпотентный денежный перевод с двойной записью (double-entry).

Демонстрирует центральные решения из разбора "денежные переводы":
- идемпотентность через Idempotency-Key - повторный запрос с тем же
  ключом не проводит перевод повторно, а возвращает сохранённый результат;
- double-entry bookkeeping - каждый перевод создаёт пару записей в
  журнале движений (DEBIT/CREDIT), баланс - производная сумма записей;
- атомарная проверка достаточности средств перед списанием.

Запуск: python3 ./02_examples/01_idempotent_transfer/main.py
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class InsufficientFunds(Exception):
    pass


@dataclass
class LedgerEntry:
    transfer_id: str
    account_id: str
    direction: Direction
    amount_minor: int


@dataclass
class TransferResult:
    transfer_id: str
    status: str  # "completed" | "failed"
    reason: str | None = None


class Ledger:
    """Журнал движений (double-entry) + идемпотентность по ключу клиента."""

    def __init__(self) -> None:
        self.entries: list[LedgerEntry] = []
        self._idempotency_store: dict[str, TransferResult] = {}
        self._next_transfer_id = 1

    def balance_of(self, account_id: str) -> int:
        """Баланс - производное значение: сумма CREDIT минус сумма DEBIT
        по записям журнала данного счёта (источник истины - журнал)."""
        total = 0
        for entry in self.entries:
            if entry.account_id != account_id:
                continue
            if entry.direction is Direction.CREDIT:
                total += entry.amount_minor
            else:
                total -= entry.amount_minor
        return total

    def transfer(
        self,
        idempotency_key: str,
        from_account: str,
        to_account: str,
        amount_minor: int,
    ) -> TransferResult:
        # 1) Идемпотентность: если этот ключ уже обработан - вернуть
        # сохранённый результат, НЕ проводя перевод повторно.
        if idempotency_key in self._idempotency_store:
            return self._idempotency_store[idempotency_key]

        # 2) Проверка достаточности средств (в реальной системе - под
        # блокировкой строки счёта внутри ACID-транзакции).
        if self.balance_of(from_account) < amount_minor:
            result = TransferResult(
                transfer_id="",
                status="failed",
                reason="insufficient_funds",
            )
            self._idempotency_store[idempotency_key] = result
            return result

        # 3) Double-entry: одна операция - две записи в журнале.
        transfer_id = f"T{self._next_transfer_id}"
        self._next_transfer_id += 1
        debit_entry = LedgerEntry(
            transfer_id, from_account, Direction.DEBIT, amount_minor
        )
        credit_entry = LedgerEntry(
            transfer_id, to_account, Direction.CREDIT, amount_minor
        )
        self.entries.append(debit_entry)
        self.entries.append(credit_entry)

        result = TransferResult(transfer_id=transfer_id, status="completed")
        self._idempotency_store[idempotency_key] = result
        return result


def main() -> None:
    print("--- Пример: идемпотентный перевод с double-entry bookkeeping ---")

    ledger = Ledger()
    # Начальные балансы задаём как "депозит" - технически перевод "из ниоткуда".
    ledger.entries.append(
        LedgerEntry("T0", "account-A", Direction.CREDIT, 100_000)  # 1000.00
    )
    ledger.entries.append(
        LedgerEntry("T0", "account-B", Direction.CREDIT, 0)
    )

    print(
        f"Баланс A до перевода: {ledger.balance_of('account-A')} "
        f"(минорные единицы)"
    )
    print(
        f"Баланс B до перевода: {ledger.balance_of('account-B')} "
        f"(минорные единицы)"
    )

    key = "idem-key-abc-123"

    # Первый вызов: перевод 500.00 с A на B.
    r1 = ledger.transfer(key, "account-A", "account-B", amount_minor=50_000)
    print(f"\n1-й вызов transfer(): {r1}")

    # Клиент не получил ответ (сетевой сбой) и повторяет запрос с ТЕМ ЖЕ ключом.
    r2 = ledger.transfer(key, "account-A", "account-B", amount_minor=50_000)
    print(f"2-й вызов transfer() (ретрай, тот же ключ): {r2}")

    assert r1 == r2, (
        "повторный вызов с тем же ключом должен вернуть идентичный результат"
    )
    assert r1.status == "completed"

    balance_a = ledger.balance_of("account-A")
    balance_b = ledger.balance_of("account-B")
    print(f"\nБаланс A после: {balance_a} (минорные единицы)")
    print(f"Баланс B после: {balance_b} (минорные единицы)")

    assert balance_a == 50_000, (
        "перевод должен был списаться РОВНО ОДИН раз, а не дважды"
    )
    assert balance_b == 50_000, (
        "зачисление должно было произойти РОВНО ОДИН раз"
    )

    # Инвариант double-entry: сумма всех движений по журналу (без начального
    # депозита T0) равна нулю - что списано с одного, зачислено другому.
    transfer_entries = [
        e for e in ledger.entries if e.transfer_id == r1.transfer_id
    ]
    net = sum(
        e.amount_minor if e.direction is Direction.CREDIT else -e.amount_minor
        for e in transfer_entries
    )
    assert net == 0, (
        "double-entry инвариант нарушен: сумма движений перевода "
        "должна быть равна нулю"
    )

    # Попытка перевести больше, чем есть на счету - идемпотентный ключ другой,
    # так что это НОВАЯ операция, которая должна корректно отклониться.
    r3 = ledger.transfer(
        "idem-key-xyz-999", "account-A", "account-B", amount_minor=1_000_000
    )
    print(f"\nПопытка перевода сверх баланса: {r3}")
    assert r3.status == "failed"
    assert ledger.balance_of("account-A") == 50_000, (
        "баланс не должен измениться при отказе"
    )

    print(
        "\nВывод: повторный запрос с тем же Idempotency-Key не провёл перевод "
        "дважды, а инвариант double-entry (сумма движений = 0) выполняется "
        "для каждой успешной операции, давая встроенную возможность аудита."
    )


if __name__ == "__main__":
    main()
