"""Решение: SimpleRange."""

from __future__ import annotations


class SimpleRange:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step не может быть 0")
        self.start = start
        self.stop = stop
        self.step = step
        self._current = start

    def __iter__(self) -> "SimpleRange":
        return self

    def __next__(self) -> int:
        if self.step > 0 and self._current >= self.stop:
            raise StopIteration
        if self.step < 0 and self._current <= self.stop:
            raise StopIteration

        value = self._current
        self._current += self.step
        return value


def main() -> None:
    checks_passed = 0
    total_checks = 5

    forward = list(SimpleRange(0, 5))
    assert forward == [0, 1, 2, 3, 4], f"forward: {forward}"
    checks_passed += 1

    stepped = list(SimpleRange(0, 10, 2))
    assert stepped == [0, 2, 4, 6, 8], f"stepped: {stepped}"
    checks_passed += 1

    backward = list(SimpleRange(5, 0, -1))
    assert backward == [5, 4, 3, 2, 1], f"backward: {backward}"
    checks_passed += 1

    r = SimpleRange(0, 3)
    it1 = iter(r)
    assert next(it1) == 0
    checks_passed += 1
    assert next(it1) == 1
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
