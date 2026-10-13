"""
Собственный класс-итератор для пагинации "API", и yield from
для разворачивания вложенной структуры категорий/товаров.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class Product:
    id: int
    name: str


FAKE_DATABASE: list[Product] = [Product(id=i, name=f"item-{i}") for i in range(1, 24)]


class PagedApiIterator:
    """Итератор, отдающий элементы фиксированной базы данных постранично,
    как если бы каждая страница запрашивалась отдельным сетевым вызовом."""

    def __init__(self, page_size: int) -> None:
        self._page_size = page_size
        self._index = 0

    def __iter__(self) -> "PagedApiIterator":
        return self

    def __next__(self) -> Product:
        if self._index >= len(FAKE_DATABASE):
            raise StopIteration

        if self._index % self._page_size == 0:
            page_num = self._index // self._page_size + 1
            print(f"  [сетевой вызов] загрузка страницы {page_num}")

        product = FAKE_DATABASE[self._index]
        self._index += 1
        return product


@dataclass
class Category:
    name: str
    products: list[Product] = field(default_factory=list)
    subcategories: list["Category"] = field(default_factory=list)


def iter_all_products(category: Category) -> Iterator[Product]:
    """Рекурсивно разворачивает дерево категорий в плоский поток товаров."""
    yield from category.products
    for sub in category.subcategories:
        yield from iter_all_products(sub)


def build_catalog() -> Category:
    return Category(
        name="Электроника",
        products=[Product(1, "Наушники")],
        subcategories=[
            Category(
                name="Компьютеры",
                products=[Product(2, "Ноутбук"), Product(3, "Монитор")],
                subcategories=[
                    Category(name="Периферия", products=[Product(4, "Клавиатура")]),
                ],
            ),
            Category(name="Телефоны", products=[Product(5, "Смартфон")]),
        ],
    )


def main() -> None:
    print("Пагинация через собственный класс-итератор:")
    for product in PagedApiIterator(page_size=10):
        pass  # цикл выше уже напечатал сетевые вызовы; здесь просто проходим все страницы
    print(f"  всего получено товаров: {len(FAKE_DATABASE)}")

    print("\nРазворачивание вложенного каталога через yield from:")
    catalog = build_catalog()
    for product in iter_all_products(catalog):
        print(f"  - {product.name}")


if __name__ == "__main__":
    main()
