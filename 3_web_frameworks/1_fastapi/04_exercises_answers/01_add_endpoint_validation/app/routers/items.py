import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Item
from ..schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


# def-роут: тело синхронное (обычная работа с SQLAlchemy Session), FastAPI
# сам исполнит его в threadpool — блокирующие вызовы к БД не остановят
# event loop. См. 01_theory/02_async_endpoints.md.
@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    item = Item(name=payload.name, description=payload.description, price=payload.price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return ItemRead.from_orm_item(item)


@router.get("", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)) -> list[ItemRead]:
    items = db.query(Item).order_by(Item.id).all()
    return [ItemRead.from_orm_item(item) for item in items]


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ItemRead.from_orm_item(item)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)) -> ItemRead:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return ItemRead.from_orm_item(item)


# async def-роут: реального async I/O здесь нет, только asyncio.sleep как
# заглушка "похода во внешний сервис" (например, курс валют перед показом
# цены). Это учебная демонстрация того, что await отдаёт event loop другим
# запросам на время ожидания — см. 01_theory/02_async_endpoints.md про то,
# когда async def даёт реальную выгоду (настоящий асинхронный I/O), а когда
# нет смысла его использовать.
@router.get("/{item_id}/with-external-check", response_model=ItemRead)
async def get_item_with_external_check(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    # имитация await-запроса к внешнему сервису (курсы валют, склад и т.п.)
    await asyncio.sleep(0.1)

    return ItemRead.from_orm_item(item)
