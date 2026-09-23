from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Для учебного примера используем sqlite: не нужно поднимать внешнюю БД,
# чтобы запустить приложение и миграции. В реальном async-сервисе на
# asyncpg/PostgreSQL вместо create_engine/sessionmaker использовался бы
# create_async_engine/async_sessionmaker из sqlalchemy.ext.asyncio — см.
# 01_theory/01_async_endpoints.md про то, когда async-драйвер БД реально нужен.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
