# Dependency Injection в FastAPI

FastAPI построен вокруг механизма зависимостей (`Depends`) — это способ
объявить "для выполнения этого эндпоинта сначала нужно получить вот это", без
ручного вызова кода в начале каждой функции.

## Базовый пример

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_query_param(q: str | None = None) -> str:
    return q or "default"


@app.get("/search")
def search(query: str = Depends(get_query_param)) -> dict:
    return {"query": query}
```

`Depends(get_query_param)` говорит FastAPI: перед вызовом `search` вызови
`get_query_param`, и результат подставь в параметр `query`. Зависимость может
сама принимать параметры запроса, заголовки, другие зависимости — FastAPI
разберёт всю цепочку.

## Цепочки зависимостей и кэширование в рамках запроса

Зависимости могут зависеть друг от друга:

```python
from fastapi import Depends


def get_token_header(x_token: str) -> str:
    return x_token


def get_current_user(token: str = Depends(get_token_header)) -> dict:
    # здесь можно было бы сходить в БД/кэш по token
    return {"token": token, "username": "denis"}


@app.get("/me")
def read_current_user(user: dict = Depends(get_current_user)) -> dict:
    return user
```

Важная деталь: если несколько зависимостей в рамках **одного и того же
запроса** ссылаются на одну и ту же функцию-зависимость, FastAPI вызовет её
только один раз и переиспользует результат для всех, кто на неё ссылается.
Это не глобальный кэш между запросами — он живёт строго в пределах обработки
одного запроса.

## Зависимости с `yield`: управление ресурсами

Самый частый практический случай — сессия БД, которую нужно открыть перед
обработкой запроса и гарантированно закрыть после, независимо от того,
успешно ли обработчик завершился или выбросил исключение:

```python
from collections.abc import Generator
from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  # сессия отдаётся обработчику эндпоинта
    finally:
        db.close()  # выполнится всегда — и при успехе, и при исключении
```

Код до `yield` выполняется перед вызовом эндпоинта, код после `yield`
(в `finally`) — после того, как ответ сформирован, вне зависимости от
исхода. Это то же самое, что `try/finally` вокруг вызова обработчика, но без
дублирования этой логики в каждом эндпоинте:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    item = db.get(Item, item_id)
    return {"id": item.id, "name": item.name}
```

## Типовые практические случаи

- **Сессия БД** (`get_db`, см. выше) — самый частый пример.
- **Текущий пользователь / авторизация** — зависимость проверяет токен и либо
  возвращает объект пользователя, либо кидает `HTTPException(401)`, которая
  остановит обработку запроса ещё до тела эндпоинта.
- **Пагинация** — общая зависимость `pagination_params(skip: int = 0, limit: int = 20)`,
  переиспользуемая в нескольких эндпоинтах списков.

```python
from fastapi import HTTPException, status


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return user
```

## Зачем нужен именно такой подход

- **Разделение ответственности.** Эндпоинт не занимается тем, как получить
  сессию БД или проверить токен — это вынесено в отдельные, переиспользуемые
  функции.
- **Тестируемость через override.** В тестах реальную зависимость (например,
  `get_db`, которая ходит в боевую БД) можно подменить на тестовую версию без
  изменения кода эндпоинтов:

```python
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_db


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
```

`dependency_overrides` — словарь "исходная зависимость → замена", который
FastAPI проверяет перед тем, как вызывать настоящую зависимость. Это позволяет
гонять тесты на in-memory/тестовой БД, не трогая код приложения.
