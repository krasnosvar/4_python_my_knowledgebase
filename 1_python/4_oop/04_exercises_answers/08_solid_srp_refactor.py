"""Решение: RegistrationService, разбитый на три SRP-коллаборатора."""


class RegistrationServiceBad:
    """Эталон "плохого" поведения для сравнения."""

    def register(self, email: str, password: str) -> str:
        if len(password) < 8:
            raise ValueError("пароль слишком короткий")
        hashed = f"hashed:{password[::-1]}"
        return f"Добро пожаловать, {email}! (пароль захеширован: {hashed})"


class PasswordValidator:
    def validate(self, password: str) -> None:
        if len(password) < 8:
            raise ValueError("пароль слишком короткий")


class PasswordHasher:
    def hash(self, password: str) -> str:
        return f"hashed:{password[::-1]}"


class WelcomeEmailSender:
    def send(self, email: str, hashed_password: str) -> str:
        return f"Добро пожаловать, {email}! (пароль захеширован: {hashed_password})"


class RegistrationService:
    def __init__(
        self,
        validator: PasswordValidator,
        hasher: PasswordHasher,
        sender: WelcomeEmailSender,
    ) -> None:
        self._validator = validator
        self._hasher = hasher
        self._sender = sender

    def register(self, email: str, password: str) -> str:
        self._validator.validate(password)
        hashed = self._hasher.hash(password)
        return self._sender.send(email, hashed)


def main() -> None:
    service = RegistrationService(PasswordValidator(), PasswordHasher(), WelcomeEmailSender())

    result = service.register("user@example.com", "supersecret")

    rejected_short_password = False
    try:
        service.register("user@example.com", "short")
    except ValueError:
        rejected_short_password = True

    reference = RegistrationServiceBad().register("user@example.com", "supersecret")

    checks = [
        (result == reference, "результат совпадает с эталонным (плохим) поведением"),
        (rejected_short_password, "короткий пароль отклоняется через PasswordValidator"),
        (hasattr(PasswordValidator(), "validate"), "есть отдельный класс-валидатор"),
        (hasattr(PasswordHasher(), "hash"), "есть отдельный класс-хешер"),
        (hasattr(WelcomeEmailSender(), "send"), "есть отдельный класс-отправитель"),
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
