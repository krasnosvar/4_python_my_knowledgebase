"""Решение: BankAccount с валидирующим @property balance."""


class BankAccount:
    def __init__(self, initial_balance: float = 0) -> None:
        self._balance = 0.0
        self.balance = initial_balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("баланс не может быть отрицательным")
        self._balance = value

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма пополнения должна быть положительной")
        self.balance = self.balance + amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма снятия должна быть положительной")
        self.balance = self.balance - amount


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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()
