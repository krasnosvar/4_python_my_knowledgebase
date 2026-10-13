"""Решение: ромбовидное наследование Child(Left, Right), кооперативный super()."""


class Base:
    def greet(self) -> str:
        return "Base"


class Left(Base):
    def greet(self) -> str:
        return "Left -> " + super().greet()


class Right(Base):
    def greet(self) -> str:
        return "Right -> " + super().greet()


class Child(Left, Right):
    pass


def main() -> None:
    expected_mro = ["Child", "Left", "Right", "Base", "object"]
    actual_mro = [cls.__name__ for cls in Child.__mro__]

    checks = [
        (actual_mro == expected_mro, f"MRO должен быть {expected_mro}, получено {actual_mro}"),
        (Child().greet() == "Left -> Right -> Base", "Child().greet() проходит через Left и Right один раз"),
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
