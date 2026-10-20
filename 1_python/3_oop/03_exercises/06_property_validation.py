"""Задача: реализуйте класс BankAccount с @property balance, которое
запрещает установку отрицательного значения, и методами deposit/withdraw,
которые тоже не должны допускать уход баланса в минус."""


class BankAccount:
    def __init__(self, initial_balance: float = 0) -> None:
        self._balance = 0.0
        self.balance = initial_balance  # проходит через setter уже при создании

    @property
    def balance(self) -> float:
        # TODO: верните self._balance
        raise NotImplementedError

    @balance.setter
    def balance(self, value: float) -> None:
        # TODO: если value < 0 — поднимите ValueError("баланс не может быть отрицательным"),
        # иначе присвойте self._balance = value.
        raise NotImplementedError

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма пополнения должна быть положительной")
        self.balance = self.balance + amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма снятия должна быть положительной")
        self.balance = self.balance - amount  # setter сам не даст уйти в минус


def main() -> None:
    account = BankAccount(100)

    setter_rejected_negative = False
    try:
        account.balance = -50
    except ValueError:
        setter_rejected_negative = True

    withdraw_rejected_overdraft = False
    try:
        account.withdraw(1000)
    except ValueError:
        withdraw_rejected_overdraft = True

    account.deposit(50)

    checks = [
        (account.balance == 150, "deposit увеличивает баланс через property"),
        (setter_rejected_negative, "прямое присвоение отрицательного баланса запрещено"),
        (withdraw_rejected_overdraft, "withdraw не допускает уход в минус"),
        (account.balance == 150, "баланс не изменился после отклонённых операций"),
    ]

    checks_passed = 0
    total_checks = len(checks)
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if ok:
            checks_passed += 1
        print(f"[{status}] {description}")

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
