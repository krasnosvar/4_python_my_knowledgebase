"""Задание 3: найти и исправить проблему N+1.

Стенд: тот же docker-compose из ../02_examples, та же схема (таблицы
authors/books). Запускайте после `docker compose up -d` и применения
schema.sql из ../02_examples/.

load_authors_with_books ниже -- рабочий код, который тем не менее содержит
классическую проблему N+1: он делает 1 запрос на список авторов и ещё по
одному запросу НА КАЖДОГО автора, чтобы получить его книги.

Запуск: python task_3_n_plus_one.py
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, List, Tuple

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

import os

SQLALCHEMY_URL = (
    f"postgresql+psycopg://{os.getenv('PG_USER', 'kb_user')}:"
    f"{os.getenv('PG_PASSWORD', 'kb_password')}@"
    f"{os.getenv('PG_HOST', 'localhost')}:{os.getenv('PG_PORT', '5432')}/"
    f"{os.getenv('PG_DB', 'kb_shop')}"
)


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    title: Mapped[str] = mapped_column(String(255))

    author: Mapped["Author"] = relationship(back_populates="books")


class QueryCounter:
    """Считает количество запросов, реально отправленных в БД."""

    def __init__(self) -> None:
        self.count = 0

    def __call__(self, conn, cursor, statement, parameters, context, executemany) -> None:
        self.count += 1


@contextmanager
def count_queries(engine: Engine) -> Iterator[QueryCounter]:
    counter = QueryCounter()
    event.listen(engine, "before_cursor_execute", counter)
    try:
        yield counter
    finally:
        event.remove(engine, "before_cursor_execute", counter)


def load_authors_with_books(session: Session) -> List[Tuple[str, List[str]]]:
    """АНТИПАТТЕРН: N+1 запрос. Оставлено как есть -- это код, который надо
    научиться диагностировать, а не образец для подражания."""
    authors = session.scalars(select(Author)).all()  # 1 запрос
    result = []
    for author in authors:
        titles = [book.title for book in author.books]  # +1 запрос на автора
        result.append((author.name, titles))
    return result


def load_authors_with_books_fixed(session: Session) -> List[Tuple[str, List[str]]]:
    """TODO: перепишите эту функцию так, чтобы она возвращала тот же
    результат, что и load_authors_with_books, но за фиксированное
    небольшое число запросов вместо 1+N.

    Используйте selectinload или joinedload (см. импорт ниже -- добавьте
    нужный). Обоснуйте комментарием, какой вариант выбрали и почему
    (подсказка: у каждого автора в этих сид-данных обычно 1-3 книги --
    подумайте, как это влияет на выбор между joinedload и selectinload
    при бОльшем количестве книг на автора).
    """
    # TODO: реализовать, например:
    # from sqlalchemy.orm import selectinload
    # stmt = select(Author).options(selectinload(Author.books))
    # authors = session.scalars(stmt).all()
    # ...
    raise NotImplementedError


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_URL, echo=False)

    print("=== До исправления (N+1) ===")
    with count_queries(engine) as counter, Session(engine) as session:
        data = load_authors_with_books(session)
        print(f"Авторов: {len(data)}, запросов к БД: {counter.count}")
        assert counter.count > len(data), "Ожидался N+1: запросов должно быть больше, чем авторов"

    print("\n=== После исправления ===")
    with count_queries(engine) as counter, Session(engine) as session:
        data_fixed = load_authors_with_books_fixed(session)
        print(f"Авторов: {len(data_fixed)}, запросов к БД: {counter.count}")
        assert counter.count <= 2, f"Ожидалось не более 2 запросов, получили {counter.count}"

    assert sorted(data) == sorted(data_fixed), "Результат должен совпадать с исходной версией"
    print("\nOK: результат совпадает, количество запросов заметно меньше")
