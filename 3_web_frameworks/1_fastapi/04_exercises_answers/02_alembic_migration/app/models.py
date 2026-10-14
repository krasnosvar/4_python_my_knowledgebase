from datetime import datetime, timezone

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    # Добавлено миграцией 0002_add_in_stock_column.py к уже существующей
    # таблице items (см. server_default в этой миграции).
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
