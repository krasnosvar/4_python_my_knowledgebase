"""
Задача: построить ленивый пайплайн из генераторных стадий и доказать
самопроверкой, что лишние элементы действительно не вычисляются, пока
их явно не потребовали.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import islice

# Счётчик количества элементов, реально прошедших через "дорогую" стадию.
# Используется только для самопроверки лени пайплайна.
processed_counter = {"count": 0}


def source(n: int) -> Iterator[int]:
    yield from range(n)


def expensive_filter(numbers: Iterable[int]) -> Iterator[int]:
    """Пропускает только чётные числа. Помечает каждый обработанный элемент
    в processed_counter - чтобы можно было проверить, сколько элементов
    реально "прошло" через стадию."""
    for n in numbers:
        processed_counter["count"] += 1
        if n % 2 == 0:
            yield n


def double(numbers: Iterable[int]) -> Iterator[int]:
    for n in numbers:
        yield n * 2


def build_pipeline(n: int) -> Iterator[int]:
    """Должна вернуть ленивый пайплайн: source -> expensive_filter -> double,
    не материализуя список ни на одном из промежуточных шагов."""
    # TODO: соберите пайплайн из source(n), expensive_filter, double
    # и верните итоговый итератор (без list(...) внутри).
    raise NotImplementedError


def main() -> None:
    processed_counter["count"] = 0

    pipeline = build_pipeline(1_000_000)
    first_three = list(islice(pipeline, 3))

    assert first_three == [0, 4, 8], f"first_three: {first_three}"

    # если пайплайн действительно ленив, для получения первых трёх
    # результатов (0, 2, 4 - которые чётные) не должно быть обработано
    # больше нескольких десятков элементов исходного диапазона, а не все 1_000_000
    processed = processed_counter["count"]
    assert processed < 100, (
        f"пайплайн не ленив: expensive_filter обработал {processed} элементов "
        "вместо нескольких - похоже, где-то материализуется список"
    )

    print(f"Обработано элементов до получения первых трёх результатов: {processed}")
    print("PASS")


if __name__ == "__main__":
    main()
