"""Решение: 01_track_refcount_of_object"""
from __future__ import annotations

import sys


def clean_refcount(obj) -> int:
    return sys.getrefcount(obj) - 1


def main() -> None:
    checks_passed = 0
    total_checks = 4
    class Widget:
        pass

    w = Widget()
    base = clean_refcount(w)

    ref2 = w
    assert clean_refcount(w) == base + 1, "после ref2 = w refcount должен вырасти на 1"
    checks_passed += 1

    container = [w]
    assert clean_refcount(w) == base + 2, "после добавления в list refcount должен вырасти ещё на 1"
    checks_passed += 1

    del ref2
    assert clean_refcount(w) == base + 1, "после del ref2 refcount должен уменьшиться на 1"
    checks_passed += 1

    container.clear()
    assert clean_refcount(w) == base, "после container.clear() refcount должен вернуться к base"
    checks_passed += 1

    print(f"{checks_passed}/{total_checks} проверок пройдено")


if __name__ == "__main__":
    main()
