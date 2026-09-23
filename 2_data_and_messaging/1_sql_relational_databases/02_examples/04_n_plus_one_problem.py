"""Проблема N+1 в ORM и её решение через eager loading.

Показывает:
1. Антипаттерн: цикл по авторам с ленивым обращением к author.books --
   на каждой итерации ORM шлёт отдельный SELECT (N+1 запрос вместо одного).
2. Счётчик запросов через событие SQLAlchemy before_cursor_execute, чтобы
   разница была измеримой, а не "на глаз".
3. Исправление через selectinload (доп. запрос вида IN (...)) и joinedload
   (один запрос через LEFT JOIN) -- у каждого свой компромисс, см. теорию.

Запуск: python 04_n_plus_one_problem.py
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, List

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
)

from db_config import SQLALCHEMY_URL


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


def demo_n_plus_one(engine: Engine) -> None:
    """Антипаттерн: N+1 запросов вместо одного-двух."""
    with count_queries(engine) as counter, Session(engine) as session:
        authors = session.scalars(select(Author)).all()  # 1 запрос
        total_books = 0
        for author in authors:
            # Ленивая загрузка по умолчанию: каждое обращение к .books --
            # это отдельный SELECT ... WHERE author_id = :id прямо здесь.
            total_books += len(author.books)

        print(f"[N+1]           авторов={len(authors)}, книг={total_books}, "
              f"запросов к БД={counter.count} (ожидаем 1 + N)")


def demo_selectinload(engine: Engine) -> None:
    """Исправление: selectinload -- отдельный запрос вида IN (...)."""
    with count_queries(engine) as counter, Session(engine) as session:
        stmt = select(Author).options(selectinload(Author.books))
        authors = session.scalars(stmt).all()
        total_books = sum(len(author.books) for author in authors)

        print(f"[selectinload]  авторов={len(authors)}, книг={total_books}, "
              f"запросов к БД={counter.count} (ожидаем 2: авторы + книги одним IN)")


def demo_joinedload(engine: Engine) -> None:
    """Исправление: joinedload -- один запрос через LEFT JOIN."""
    with count_queries(engine) as counter, Session(engine) as session:
        stmt = select(Author).options(joinedload(Author.books))
        authors = session.scalars(stmt).unique().all()
        total_books = sum(len(author.books) for author in authors)

        print(f"[joinedload]    авторов={len(authors)}, книг={total_books}, "
              f"запросов к БД={counter.count} (ожидаем 1)")


def main() -> None:
    engine = create_engine(SQLALCHEMY_URL, echo=False)

    demo_n_plus_one(engine)
    demo_selectinload(engine)
    demo_joinedload(engine)


if __name__ == "__main__":
    main()
