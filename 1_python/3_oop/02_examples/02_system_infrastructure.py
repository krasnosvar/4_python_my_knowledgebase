"""Миксины в сервисах инфраструктуры + инспекция MRO."""

import json
import time


class JSONSerializableMixin:
    """Добавляет одну возможность: сериализацию публичных полей в JSON."""

    def to_json(self) -> str:
        public_fields = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return json.dumps(public_fields, ensure_ascii=False)


class LoggingMixin:
    """Добавляет одну возможность: единообразное логирование событий."""

    def log(self, message: str) -> None:
        print(f"[{time.strftime('%H:%M:%S')}] {type(self).__name__}: {message}")


class BaseService:
    def __init__(self, name: str) -> None:
        self.name = name
        self.healthy = True

    def check_health(self) -> bool:
        return self.healthy


class DatabaseService(LoggingMixin, JSONSerializableMixin, BaseService):
    def __init__(self, name: str, host: str) -> None:
        super().__init__(name)
        self.host = host

    def check_health(self) -> bool:
        self.log(f"проверка соединения с {self.host}")
        return super().check_health()


if __name__ == "__main__":
    db = DatabaseService("primary-db", host="db.internal:5432")

    print("MRO:", [cls.__name__ for cls in DatabaseService.__mro__])

    print("health:", db.check_health())
    print("json:", db.to_json())

    # LoggingMixin стоит первым в списке родителей -> его log() и check_health()
    # (унаследованный от BaseService через MRO) видны раньше JSONSerializableMixin.
