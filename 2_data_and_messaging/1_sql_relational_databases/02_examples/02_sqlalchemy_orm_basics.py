"""Базовые CRUD-операции через SQLAlchemy 2.0 (declarative models + Session).

Показывает:
- декларативные модели в стиле SQLAlchemy 2.0 (DeclarativeBase, Mapped,
  mapped_column);
- связь один-ко-многим Author -> Book через relationship();
- Create / Read / Update / Delete через Session.

Запуск: python 02_sqlalchemy_orm_basics.py
Перед запуском: docker compose up -d, затем применить schema.sql.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from db_config import SQLALCHEMY_URL


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    books: Mapped[List["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r})"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    title: Mapped[str] = mapped_column(String(255))
    published_year: Mapped[Optional[int]]

    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r})"


def demo_create(session: Session) -> int:
    """Create: добавляем нового автора с двумя книгами одной транзакцией."""
    author = Author(name="Михаил Булгаков")
    author.books.append(Book(title="Мастер и Маргарита", published_year=1967))
    author.books.append(Book(title="Собачье сердце", published_year=1925))
    session.add(author)
    session.commit()
    print(f"Создан: {author}, книг: {len(author.books)}")
    return author.id


def demo_read(session: Session) -> None:
    """Read: выборка всех авторов и точечный поиск книги по названию."""
    authors = session.scalars(select(Author).order_by(Author.name)).all()
    print("\nВсе авторы:")
    for author in authors:
        print(f"  {author}")

    book = session.scalar(select(Book).where(Book.title == "Мастер и Маргарита"))
    print(f"\nНайдена книга: {book}")


def demo_update(session: Session, author_id: int) -> None:
    """Update: точечное изменение имени автора."""
    author = session.get(Author, author_id)
    if author is None:
        return
    author.name = f"{author.name} (уточнено)"
    session.commit()
    print(f"\nОбновлён автор: {author}")


def demo_delete(session: Session, author_id: int) -> None:
    """Delete: удаление автора вместе с книгами (каскад задан и в ORM, и в БД)."""
    author = session.get(Author, author_id)
    if author is None:
        return
    session.delete(author)
    session.commit()
    print(f"\nУдалён автор id={author_id} вместе с книгами")


def main() -> None:
    engine = create_engine(SQLALCHEMY_URL, echo=False)

    with Session(engine) as session:
        author_id = demo_create(session)
        demo_read(session)
        demo_update(session, author_id)
        demo_delete(session, author_id)


if __name__ == "__main__":
    main()
