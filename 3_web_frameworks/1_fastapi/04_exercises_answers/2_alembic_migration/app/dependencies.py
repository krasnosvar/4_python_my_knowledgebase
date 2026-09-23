from collections.abc import Generator

from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield-зависимость: открывает сессию перед запросом и гарантированно
    закрывает её после — даже если обработчик эндпоинта выбросит исключение.
    См. 01_theory/03_dependency_injection.md."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
