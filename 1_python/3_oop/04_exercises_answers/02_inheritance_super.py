"""Решение: иерархия Animal -> Dog/Cat с использованием super().__init__()."""


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

    def describe(self) -> str:
        return f"{self.name} говорит: {self.speak()}"


class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)
        self.breed = breed

    def speak(self) -> str:
        return "Гав!"


class Cat(Animal):
    def __init__(self, name: str, indoor: bool) -> None:
        super().__init__(name)
        self.indoor = indoor

    def speak(self) -> str:
        return "Мяу!"


def main() -> None:
    dog = Dog("Бобик", breed="дворняга")
    cat = Cat("Мурка", indoor=True)

    checks = [
        (dog.name == "Бобик" and dog.breed == "дворняга", "Dog: имя и порода сохранены через super()"),
        (dog.speak() == "Гав!", "Dog.speak()"),
        (dog.describe() == "Бобик говорит: Гав!", "Dog.describe() использует переопределённый speak()"),
        (cat.name == "Мурка" and cat.indoor is True, "Cat: имя и indoor сохранены через super()"),
        (cat.speak() == "Мяу!", "Cat.speak()"),
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
