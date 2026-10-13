"""Решение: ComparableMixin, примешанный к двум несвязанным классам."""

from functools import total_ordering


class ComparableMixin:
    """Классы-потребители обязаны реализовать _sort_key() -> сравнимое значение."""

    def _sort_key(self):
        raise NotImplementedError("классы-потребители должны переопределить _sort_key()")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComparableMixin):
            return NotImplemented
        return self._sort_key() == other._sort_key()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ComparableMixin):
            return NotImplemented
        return self._sort_key() < other._sort_key()


@total_ordering
class Employee(ComparableMixin):
    def __init__(self, name: str, salary: int) -> None:
        self.name = name
        self.salary = salary

    def _sort_key(self):
        return self.salary


@total_ordering
class Product(ComparableMixin):
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
