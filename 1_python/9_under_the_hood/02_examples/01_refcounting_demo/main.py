"""
sys.getrefcount: как меняется счётчик ссылок при присваивании,
добавлении в контейнер, удалении.

Запуск: python main.py
"""
from __future__ import annotations

import sys


def main() -> None:
    class Widget:
        pass

    w = Widget()
    # getrefcount сам добавляет +1 временную ссылку на время своего вызова
    print(f"после создания:           {sys.getrefcount(w) - 1}")

    other_ref = w
    print(f"после other_ref = w:      {sys.getrefcount(w) - 1}")  # +1

    container = [w]
    print(f"после добавления в list:  {sys.getrefcount(w) - 1}")  # +1

    del other_ref
    print(f"после del other_ref:      {sys.getrefcount(w) - 1}")  # -1

    container.clear()
    print(f"после container.clear():  {sys.getrefcount(w) - 1}")  # -1

    print("\n--- немедленное уничтожение при refcount == 0 ---")

    class Loud:
        def __del__(self):
            print("Loud уничтожен немедленно (refcount дошёл до 0)")

    loud = Loud()
    print("перед del loud")
    del loud
    print("после del loud (сообщение выше уже выведено)")


if __name__ == "__main__":
    main()
