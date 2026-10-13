"""
Задача: реализовать класс SimpleRange, ведущий себя как урезанная версия
встроенного range() - с шагом, включая отрицательный, и корректной
остановкой через StopIteration.
"""

from __future__ import annotations


class SimpleRange:
    """Итератор по целым числам от start (включительно) до stop
    (не включая), с шагом step. step может быть отрицательным."""

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
        # TODO: вернуть self._current и сдвинуть его на self.step,
        # либо бросить StopIteration, если достигнута граница stop.
        # Учтите оба направления: step > 0 и step < 0.
        raise NotImplementedError


def main() -> None:
    forward = list(SimpleRange(0, 5))
    assert forward == [0, 1, 2, 3, 4], f"forward: {forward}"

    stepped = list(SimpleRange(0, 10, 2))
    assert stepped == [0, 2, 4, 6, 8], f"stepped: {stepped}"

    backward = list(SimpleRange(5, 0, -1))
    assert backward == [5, 4, 3, 2, 1], f"backward: {backward}"

    # каждый iter() на новом объекте должен работать независимо
    r = SimpleRange(0, 3)
    it1 = iter(r)
    assert next(it1) == 0
    assert next(it1) == 1

    print("PASS")


if __name__ == "__main__":
    main()
