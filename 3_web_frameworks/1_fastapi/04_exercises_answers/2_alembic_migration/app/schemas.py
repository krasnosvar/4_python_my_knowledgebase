from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .models import Item


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name не может состоять из одних пробелов")
        return value.strip()


class ItemMeta(BaseModel):
    """Вложенная схема (nested model) — попадает в ответ как под-объект."""

    created_at: datetime
    currency: str = "RUB"


class ItemRead(BaseModel):
    """Схема ответа API. from_attributes=True позволяет собрать её
    напрямую из ORM-объекта Item (item.id, item.name и т.д.), см.
    01_theory/02_pydantic.md."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: float
    meta: ItemMeta

    @classmethod
    def from_orm_item(cls, item: Item) -> "ItemRead":
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            meta=ItemMeta(created_at=item.created_at),
        )
