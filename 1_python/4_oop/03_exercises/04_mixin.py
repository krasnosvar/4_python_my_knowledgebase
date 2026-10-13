"""Задача: реализуйте ComparableMixin — миксин, который добавляет __lt__,
__le__, __gt__, __ge__ на основе одного метода _sort_key(), который должны
предоставить классы-потребители. Примешайте его к двум несвязанным классам."""

from functools import total_ordering


class ComparableMixin:
    """Классы-потребители обязаны реализовать _sort_key() -> сравнимое значение."""

    def _sort_key(self):
        raise NotImplementedError("классы-потребители должны переопределить _sort_key()")

    # TODO: реализуйте __eq__ и __lt__ через self._sort_key() и other._sort_key().
    # Остальные операторы сравнения можно получить декоратором functools.total_ordering
    # (уже импортирован) — примените его к классам-потребителям ниже.
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        raise NotImplementedError


# TODO: примешайте ComparableMixin и добавьте @total_ordering к обоим классам.
class Employee:
    def __init__(self, name: str, salary: int) -> None:
        self.name = name
        self.salary = salary

    def _sort_key(self):
        return self.salary


class Product:
    def __init__(self, title: str, price: float) -> None:
        self.title = title
        self.price = price

    def _sort_key(self):
        return self.price


def main() -> None:
    alice = Employee("Alice", 90000)
    bob = Employee("Bob", 70000)
    cheap = Product("Ручка", 10.0)
    expensive = Product("Ноутбук", 900.0)

    checks = [
        (bob < alice, "Employee: сравнение по зарплате (<)"),
        (alice > bob, "Employee: сравнение по зарплате (>) через total_ordering"),
        (alice >= alice, "Employee: >= через total_ordering"),
        (cheap < expensive, "Product: сравнение по цене (<) — тот же миксин, другой класс"),
        (sorted([alice, bob], key=lambda e: e._sort_key())[0].name == "Bob", "сортировка сотрудников"),
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
