"""
Пример: модули math и random, три способа импорта, __name__.

Запуск:
    python 02_examples/01_dice_and_geometry.py
"""

import math
import random as rnd
from math import sqrt


def roll_dice():
    """Бросок шестигранного кубика."""
    return rnd.randint(1, 6)


def circle_area(radius):
    """Площадь круга через константу math.pi."""
    return math.pi * radius ** 2


def distance(x1, y1, x2, y2):
    """Расстояние между двумя точками на плоскости."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def main():
    rnd.seed(7)
    print(f"Бросок 1: {roll_dice()}")
    print(f"Бросок 2: {roll_dice()}")
    print(f"Площадь круга радиуса 3: {circle_area(3):.2f}")
    print(f"Расстояние от (0, 0) до (3, 4): {distance(0, 0, 3, 4)}")
    print(f"__name__ этого файла: {__name__}")


if __name__ == "__main__":
    main()
