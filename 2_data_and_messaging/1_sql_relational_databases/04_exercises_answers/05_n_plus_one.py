"""Решение задания 05: найти и исправить проблему N+1.

load_authors_with_books_fixed использует selectinload: он выполняет ровно
2 запроса независимо от того, сколько книг у каждого автора -- сначала
SELECT авторов, затем один SELECT ... WHERE author_id IN (...) для всех
их книг разом, и SQLAlchemy сам склеивает результат по author_id в
Python. Это выгоднее, чем joinedload, именно в связи 1:N: joinedload
сделал бы это одним запросом через LEFT JOIN, но тогда каждая строка
автора дублировалась бы в результате JOIN на каждую его книгу (для
автора с 5 книгами -- 5 одинаковых строк author в сыром результате,
которые SQLAlchemy потом схлопывает через .unique() на стороне Python) --
при большом количестве книг на автора это лишний трафик из БД. selectinload
не размножает строки родителя вообще, поэтому предпочтительнее здесь.

Запуск: python 05_n_plus_one.py
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator, List, Tuple

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)

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
    """Антипатерн: N+1 запрос (оставлено как в задании -- для контраста)."""
    authors = session.scalars(select(Author)).all()
    result = []
    for author in authors:
        titles = [book.title for book in author.books]
        result.append((author.name, titles))
    return result


def load_authors_with_books_fixed(session: Session) -> List[Tuple[str, List[str]]]:
    """Исправление: selectinload -- ровно 2 запроса вместо 1+N."""
    stmt = select(Author).options(selectinload(Author.books))
    authors = session.scalars(stmt).all()
    return [(author.name, [book.title for book in author.books]) for author in authors]


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
