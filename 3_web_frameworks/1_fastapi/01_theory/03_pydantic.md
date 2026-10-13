# Pydantic: модели, валидация, вложенные схемы

FastAPI использует Pydantic-модели как основной способ описать форму данных:
что приходит в теле запроса, что уходит в ответе, какие поля обязательны,
какие ограничения на значения. Валидация происходит автоматически — если
данные не проходят схему, клиент получает `422 Unprocessable Entity` с
подробностями, а не падение где-то внутри бизнес-логики.

## Базовая модель

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    description: str | None = None
```

`Field` задаёт дополнительные ограничения и метаданные поверх обычной
Python-аннотации типа: границы значений, длину строк, значения по умолчанию.
Если в теле запроса `price` окажется отрицательным или `name` пустой строкой —
Pydantic вернёт ошибку валидации ещё до того, как код эндпоинта начнёт
выполняться.

## Вложенные схемы (nested models)

Модель может содержать другую модель — это прямое отражение вложенных
JSON-структур:

```python
from pydantic import BaseModel


class Address(BaseModel):
    city: str
    street: str


class UserCreate(BaseModel):
    name: str
    address: Address  # вложенная модель


# автоматически провалидирует и вложенный объект, и сам верхний уровень
user = UserCreate.model_validate(
    {
        "name": "Denis",
        "address": {"city": "Moscow", "street": "Lenina"},
    }
)
```

Список вложенных моделей — тоже штатный случай:

```python
class OrderCreate(BaseModel):
    items: list[ItemCreate]
```

## Кастомные валидаторы

Когда ограничений `Field` недостаточно (например, нужна проверка, зависящая от
нескольких полей сразу), используются валидаторы:

```python
from pydantic import BaseModel, field_validator, model_validator


class ItemCreate(BaseModel):
    name: str
    price: float
    discount_price: float | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name не может состоять из одних пробелов")
        return value.strip()

    @model_validator(mode="after")
    def discount_must_be_lower(self) -> "ItemCreate":
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price должен быть меньше price")
        return self
```

`field_validator` проверяет/нормализует одно поле, `model_validator(mode="after")`
проверяет модель целиком после того, как все поля уже провалидированы
по отдельности — удобно для правил вида "поле A должно быть меньше поля B".

## Pydantic v2 vs v1: что изменилось

FastAPI (актуальные версии) построен на Pydantic v2. Основные отличия от v1,
которые стоит знать, если встречается старый код или туториалы:

| v1 | v2 |
|---|---|
| `class Config:` внутри модели | `model_config = ConfigDict(...)` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj(data)` | `.model_validate(data)` |
| `orm_mode = True` | `from_attributes=True` (в `model_config`) |

```python
from pydantic import BaseModel, ConfigDict


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # было: orm_mode = True

    id: int
    name: str
    price: float
```

Ядро валидации в Pydantic v2 переписано на Rust (`pydantic-core`) — отсюда
заметный прирост производительности по сравнению с v1, где вся валидация шла
на чистом Python.

## Связь Pydantic-схем с ORM: `from_attributes=True`

Обычно в проекте есть SQLAlchemy-модель (хранится в БД) и отдельная
Pydantic-схема для ответа API — их не стоит смешивать, но нужно уметь
конвертировать одно в другое. `from_attributes=True` разрешает Pydantic читать
данные не только из dict, но и из произвольного объекта через атрибуты
(`obj.name`, `obj.price` и т.д.) — то есть напрямую из ORM-инстанса:

```python
from pydantic import BaseModel, ConfigDict


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float


# item_orm — это объект SQLAlchemy-модели Item, полученный из сессии БД
item_schema = ItemRead.model_validate(item_orm)
```

Без `from_attributes=True` пришлось бы вручную собирать dict из полей
ORM-объекта перед передачей в схему. С этим флагом Pydantic сам обращается к
атрибутам объекта — ровно то, что нужно на границе "ORM-модель → ответ API".

## Зачем всё это нужно

- Валидация происходит один раз, на границе входа в приложение — дальше по коду
  можно быть уверенным, что данные соответствуют заявленной форме.
- Схемы документируют контракт API: FastAPI генерирует OpenAPI/Swagger прямо
  из Pydantic-моделей, без ручного описания.
- Разделение "модель для API" и "модель для БД" позволяет менять одно, не
  трогая другое (например, скрыть внутреннее поле из ответа API).
