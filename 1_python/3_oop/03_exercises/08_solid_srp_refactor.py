"""Задача: класс RegistrationService ниже нарушает принцип единственной
ответственности (SRP) — валидация, хеширование пароля и "отправка" письма
свалены в один метод. Разбейте это на три отдельных коллаборатора
(PasswordValidator, PasswordHasher, WelcomeEmailSender) и соберите их
через RegistrationService, который только координирует вызовы (DIP)."""


class RegistrationServiceBad:
    """Не трогайте — эталон "плохого" поведения для сравнения."""

    def register(self, email: str, password: str) -> str:
        if len(password) < 8:
            raise ValueError("пароль слишком короткий")
        hashed = f"hashed:{password[::-1]}"
        return f"Добро пожаловать, {email}! (пароль захеширован: {hashed})"


# TODO: реализуйте три маленьких класса с одной ответственностью каждый.

class PasswordValidator:
    def validate(self, password: str) -> None:
        raise NotImplementedError  # должно поднимать ValueError при len(password) < 8


class PasswordHasher:
    def hash(self, password: str) -> str:
        raise NotImplementedError  # верните f"hashed:{password[::-1]}"


class WelcomeEmailSender:
    def send(self, email: str, hashed_password: str) -> str:
        raise NotImplementedError  # верните f"Добро пожаловать, {email}! (пароль захеширован: {hashed_password})"


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
        # TODO: скоординируйте вызовы validator.validate, hasher.hash, sender.send
        # и верните результат sender.send(...).
        raise NotImplementedError


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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()
