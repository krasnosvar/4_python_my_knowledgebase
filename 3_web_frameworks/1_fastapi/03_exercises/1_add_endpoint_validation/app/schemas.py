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


class ItemUpdate(BaseModel):
    """Схема для частичного обновления (PATCH /items/{id}).

    Требования (см. задание в 03_exercises/1_add_endpoint_validation/README.md):
      - все поля опциональны — обновляются только те, что клиент реально прислал;
      - если передан price — он должен быть > 0;
      - если передан name — после strip() он не должен быть пустой строкой.
    """

    # TODO: объяви поля name, description, price как опциональные (str | None,
    # float | None), с теми же ограничениями (min_length/gt), что и в ItemCreate.
    name: str | None = None
    description: str | None = None
    price: float | None = None

    # TODO: добавь field_validator("name"), который бросает ValueError,
    # если непустая строка после strip() оказывается пустой (аналогично
    # ItemCreate.name_must_not_be_blank выше). Не забудь пропускать None.


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
