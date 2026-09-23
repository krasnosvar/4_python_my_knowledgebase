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

    all_ok = True
    for ok, description in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        print(f"[{status}] {description}")

    print("PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()
