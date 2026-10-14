"""Задача: постройте ромбовидное наследование Child(Left, Right), оба из
которых наследуют Base, и убедитесь, что super() в Left и Right работает
кооперативно (по MRO), а не жёстко указывает на Base."""


class Base:
    def greet(self) -> str:
        return "Base"


class Left(Base):
    def greet(self) -> str:
        # TODO: верните "Left -> " + результат super().greet()
        raise NotImplementedError


class Right(Base):
    def greet(self) -> str:
        # TODO: верните "Right -> " + результат super().greet()
        raise NotImplementedError


# TODO: объявите Child(Left, Right) без собственного greet() —
# он должен унаследовать поведение по MRO.
class Child:
    pass


def main() -> None:
    expected_mro = ["Child", "Left", "Right", "Base", "object"]
    actual_mro = [cls.__name__ for cls in Child.__mro__]

    checks = [
        (actual_mro == expected_mro, f"MRO должен быть {expected_mro}, получено {actual_mro}"),
        (Child().greet() == "Left -> Right -> Base", "Child().greet() проходит через Left и Right один раз"),
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
