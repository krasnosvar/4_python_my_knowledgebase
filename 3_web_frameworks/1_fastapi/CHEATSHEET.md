# FastAPI — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая
ошибка, которая ломает сервис или данные. Проверено на FastAPI 0.141,
Pydantic 2.13.

## HTTP: методы и статус-коды

Подробно: [01_http_and_first_app.md](./01_theory/01_http_and_first_app.md).

| Метод | Смысл |
| :--- | :--- |
| `GET` | прочитать, ничего не меняя |
| `POST` | создать |
| `PUT` / `PATCH` | заменить целиком / изменить часть полей |
| `DELETE` | удалить |

| Код | Когда |
| :--- | :--- |
| `200` / `201` | успех / ресурс создан (ответ на `POST`) |
| `202` | принято, обработка позже (фоновая задача) |
| `400` | запрос некорректен |
| `401` / `403` | «кто ты?» / «знаю, кто ты, но нельзя» |
| `404` / `422` | нет ресурса / данные не прошли валидацию (FastAPI отдаёт сам) |
| `500` | необработанная ошибка в коде сервера |

## Запуск

| Задача | Команда |
| :--- | :--- |
| Установить | `pip install fastapi uvicorn` |
| Dev-сервер с автоперезапуском | `uvicorn main:app --reload` (`main.py`, объект `app`) |
| Интерактивная документация | `http://127.0.0.1:8000/docs` |

## Откуда берётся параметр

| Объявление | Источник | Пример запроса |
| :--- | :--- | :--- |
| `item_id: int` + `{item_id}` в пути | path | `/items/42` |
| `q: str \| None = None` (нет в пути) | query, необязательный | `/items?q=test` |
| `limit: int = Query(20, le=100)` | query с ограничениями | `/items?limit=50` |
| `item: ItemCreate` (Pydantic-модель) | JSON-тело | `POST` с `{"name": ...}` |
| `x_token: str = Header()` | заголовок `X-Token` (`_` → `-`) | `X-Token: abc` |
| `user = Depends(get_user)` | результат зависимости | — |

```python
from fastapi import FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI()

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict:
    return {"item_id": item_id, "q": q}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, x_token: str = Header()) -> dict:
    if x_token != "secret":
        raise HTTPException(status_code=403, detail="Forbidden")
    return item.model_dump()
```

## `async def` или `def`

Подробно: [02_async_endpoints.md](./01_theory/02_async_endpoints.md).

| Внутри эндпоинта | Объявлять | Почему |
| :--- | :--- | :--- |
| `await` над async-библиотекой (`httpx.AsyncClient`, `asyncpg`) | `async def` | event loop свободен во время ожидания |
| Синхронная библиотека (`requests`, `psycopg2`), `time.sleep` | `def` | FastAPI сам уводит вызов в threadpool |
| Нужен `async def`, но есть блокирующий кусок | `async def` + `await run_in_threadpool(fn, arg)` | снять блокировку с event loop |
| Сомневаетесь | `def` | блокировка изолирована в потоке, а не в loop |

- ⚠️ `time.sleep` / `requests.get` / синхронный драйвер БД внутри `async def` блокирует **все** запросы приложения.
- ⚠️ async не ускоряет CPU-bound работу — её в процессы или в Celery.

## Pydantic v2

Подробно: [03_pydantic.md](./01_theory/03_pydantic.md).

| Задача | Pydantic v2 | Было в v1 |
| :--- | :--- | :--- |
| Ограничения поля | `Field(min_length=1, gt=0)` | то же |
| Dict → модель (валидация) | `Model.model_validate(data)` | `.parse_obj()` |
| Модель → dict / JSON | `.model_dump()` / `.model_dump_json()` | `.dict()` / `.json()` |
| Проверка одного поля | `@field_validator("name")` + `@classmethod` | `@validator` |
| Проверка нескольких полей | `@model_validator(mode="after")`, вернуть `self` | `@root_validator` |
| Настройки модели | `model_config = ConfigDict(...)` | `class Config:` |
| Читать из ORM-объекта | `ConfigDict(from_attributes=True)` | `orm_mode = True` |
| Вложенная схема / список | `address: Address`, `items: list[ItemCreate]` | то же |

```python
from pydantic import BaseModel, ValidationError, field_validator, model_validator

class Price(BaseModel):
    name: str
    price: float
    discount_price: float | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name пустой")
        return value.strip()

    @model_validator(mode="after")
    def discount_lower(self) -> "Price":
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price должен быть меньше price")
        return self

print(Price.model_validate({"name": " Чайник ", "price": 10}).model_dump())
# {'name': 'Чайник', 'price': 10.0, 'discount_price': None}
try:
    Price(name="x", price=10, discount_price=20)
except ValidationError as exc:
    print(exc.error_count())  # 1
```

## Зависимости (`Depends`)

Подробно: [04_dependency_injection.md](./01_theory/04_dependency_injection.md).

| Задача | Как |
| :--- | :--- |
| Подставить результат функции | `param: T = Depends(fn)` |
| Цепочка | зависимость сама принимает `Depends(other)` |
| Одна зависимость в нескольких местах запроса | вызывается **один раз** на запрос (кэш только в рамках запроса) |
| Ресурс с гарантированным закрытием | `yield` в зависимости, закрытие в `finally` |
| Остановить запрос до эндпоинта | `raise HTTPException(status_code=401/403)` в зависимости |
| Подменить в тестах | `app.dependency_overrides[get_db] = fake_get_db` |

```python
from collections.abc import Generator
from fastapi import Depends

def get_db() -> Generator[dict, None, None]:
    db = {"open": True}        # SessionLocal() в реальном коде
    try:
        yield db               # до yield — перед эндпоинтом
    finally:
        db["open"] = False     # после — всегда, даже при исключении

@app.get("/health")
def health(db: dict = Depends(get_db)) -> dict:
    return {"db_open": db["open"]}
```

## Alembic

Подробно: [05_alembic.md](./01_theory/05_alembic.md).

| Задача | Команда |
| :--- | :--- |
| Создать каркас | `alembic init alembic` (затем в `env.py`: `target_metadata = Base.metadata`) |
| Сгенерировать миграцию из моделей | `alembic revision --autogenerate -m "create items table"` |
| Накатить всё / одну | `alembic upgrade head` / `alembic upgrade +1` |
| Откатить одну / всё ⚠️ | `alembic downgrade -1` / `alembic downgrade base` |
| Что применено / вся цепочка | `alembic current` / `alembic history` |

- ⚠️ Переименование колонки autogenerate видит как `drop_column` + `add_column` — потеря данных; замените на `op.alter_column(..., new_column_name=...)`.
- ⚠️ Данные не мигрируются сами — `op.execute("UPDATE ...")` вручную.
- ⚠️ Autogenerate — черновик: читайте файл целиком, особенно `downgrade()`.
