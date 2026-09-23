# SOLID в Python

SOLID — набор из пяти принципов проектирования ООП-кода. В Python они выражаются немного иначе, чем в статических языках вроде Java/Go: вместо интерфейсов часто используются `Protocol` (см. [06_duck_typing_and_protocols.md](./06_duck_typing_and_protocols.md)), а гибкость языка позволяет нарушать принципы «тихо», без ошибок компиляции — поэтому дисциплина важнее.

## S — Single Responsibility Principle (единственная ответственность)

Класс должен иметь одну причину для изменения.

```python
# До: один класс делает всё — валидацию, сохранение и уведомление
class OrderProcessor:
    def process(self, order: dict) -> None:
        if not order.get("items"):
            raise ValueError("пустой заказ")
        # запись в БД
        print(f"saved order {order['id']}")
        # отправка письма
        print(f"email sent for order {order['id']}")
```

```python
# После: три отдельных класса с одной ответственностью каждый
class OrderValidator:
    def validate(self, order: dict) -> None:
        if not order.get("items"):
            raise ValueError("пустой заказ")

class OrderRepository:
    def save(self, order: dict) -> None:
        print(f"saved order {order['id']}")

class OrderNotifier:
    def notify(self, order: dict) -> None:
        print(f"email sent for order {order['id']}")
```

## O — Open/Closed Principle (открыт для расширения, закрыт для изменения)

Новое поведение должно добавляться новым кодом, а не правкой существующего.

```python
# До: добавление скидки требует правки if/elif внутри функции
def apply_discount(price: float, kind: str) -> float:
    if kind == "seasonal":
        return price * 0.9
    elif kind == "vip":
        return price * 0.8
    # для нового вида скидки придётся снова редактировать эту функцию
```

```python
# После: новый вид скидки — это новый класс, существующий код не трогаем
from typing import Protocol

class DiscountStrategy(Protocol):
    def apply(self, price: float) -> float: ...

class SeasonalDiscount:
    def apply(self, price: float) -> float:
        return price * 0.9

class VipDiscount:
    def apply(self, price: float) -> float:
        return price * 0.8

def apply_discount(price: float, strategy: DiscountStrategy) -> float:
    return strategy.apply(price)
```

## L — Liskov Substitution Principle (подстановка Лисков)

Подкласс должен быть заменим вместо базового класса без нарушения корректности программы.

```python
# До: классическое нарушение LSP
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)

    # Переопределение ширины ломает независимость сторон,
    # на которую опирается любой код, работающий с Rectangle
    def set_width(self, width: float) -> None:
        self.width = self.height = width
```

Код, ожидающий, что у `Rectangle` можно менять `width` и `height` независимо, сломается на `Square` — значит, `Square` не должен наследоваться от `Rectangle`.

```python
# После: общий протокол вместо наследования "Square is-a Rectangle"
from typing import Protocol

class HasArea(Protocol):
    def area(self) -> float: ...

class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height

class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side ** 2
```

## I — Interface Segregation Principle (разделение интерфейсов)

Не заставляйте класс реализовывать методы, которые ему не нужны. В Python это особенно легко нарушить одним «толстым» `Protocol` или ABC.

```python
# До: один интерфейс на все случаи жизни
class Worker(Protocol):
    def work(self) -> None: ...
    def eat(self) -> None: ...

class Robot:
    def work(self) -> None:
        print("работает")

    def eat(self) -> None:
        raise NotImplementedError("роботы не едят")  # вынужденная заглушка
```

```python
# После: два маленьких протокола вместо одного большого
class Workable(Protocol):
    def work(self) -> None: ...

class Eatable(Protocol):
    def eat(self) -> None: ...

class Robot:
    def work(self) -> None:
        print("работает")

class Human:
    def work(self) -> None:
        print("работает")

    def eat(self) -> None:
        print("ест")
```

## D — Dependency Inversion Principle (инверсия зависимостей)

Модули верхнего уровня не должны зависеть от модулей нижнего уровня — оба должны зависеть от абстракций.

```python
# До: сервис жёстко завязан на конкретную реализацию БД
class PostgresRepository:
    def save(self, data: dict) -> None:
        print("saved to postgres")

class UserService:
    def __init__(self) -> None:
        self.repo = PostgresRepository()  # жёсткая связь, нельзя подменить в тестах

    def register(self, data: dict) -> None:
        self.repo.save(data)
```

```python
# После: зависимость внедряется через протокол (dependency injection)
from typing import Protocol

class Repository(Protocol):
    def save(self, data: dict) -> None: ...

class PostgresRepository:
    def save(self, data: dict) -> None:
        print("saved to postgres")

class InMemoryRepository:
    def save(self, data: dict) -> None:
        print("saved in memory (для тестов)")

class UserService:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo  # конкретная реализация подставляется снаружи

    def register(self, data: dict) -> None:
        self.repo.save(data)

# UserService(PostgresRepository())  # в проде
# UserService(InMemoryRepository())  # в тестах, без реальной БД
```

`Protocol` здесь играет ту же роль, что интерфейс в Go или Java, — но без явного `implements`/наследования: любой объект с методом `save(data)` подходит.
