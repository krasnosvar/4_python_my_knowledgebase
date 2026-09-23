# Dataclasses

`@dataclass` (модуль `dataclasses`, с Python 3.7) генерирует шаблонный код класса-контейнера данных на основе аннотаций полей.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

Это автоматически генерирует:

* `__init__(self, x, y)`;
* `__repr__` вида `Point(x=1, y=2)`;
* `__eq__`, сравнивающий по значениям всех полей (а не по идентичности, как в обычном классе).

Без `@dataclass` пришлось бы писать все три метода вручную — dataclass убирает этот шаблонный код, оставляя фокус на данных.

## Изменяемые значения по умолчанию: `field(default_factory=...)`

В обычной функции/методе изменяемое значение по умолчанию (`def f(items=[])`) — классическая ловушка: список создаётся **один раз** при определении функции и переиспользуется между вызовами (подробнее — в теме [1_basics](../../1_basics/README.md)). В dataclass эта проблема встречается ещё чаще, потому что поля выглядят как декларативные аннотации:

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)  # правильно
    # items: list[str] = []                          # SyntaxError на уровне dataclass!
```

Dataclass **явно запрещает** изменяемые литералы (`[]`, `{}`, `set()`) в качестве значения по умолчанию — попытка написать `items: list = []` вызовет `ValueError` при определении класса. Вместо этого используется `field(default_factory=list)`: фабрика вызывается заново **для каждого экземпляра**, так что экземпляры не делят один и тот же список.

## `frozen=True` — неизменяемость и автоматический `__hash__`

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

`frozen=True` делает попытку присвоить атрибут (`p.x = 5`) исключением (`FrozenInstanceError`). Как следствие, dataclass автоматически генерирует и `__hash__`, согласованный с автосгенерированным `__eq__` — потому что неизменяемый объект с сравнением по значению безопасно использовать как ключ словаря или элемент множества (см. связь `__eq__`/`__hash__` в [01_classes_and_magic_methods.md](./01_classes_and_magic_methods.md)).

Обычный (не frozen) dataclass с автосгенерированным `__eq__`, наоборот, получает `__hash__ = None` — он **нехешируем** по тем же причинам, что и любой класс с ручным `__eq__`.

## `__post_init__` — производные и валидируемые поля

`__init__` генерируется автоматически, но иногда нужна дополнительная логика после присвоения полей — например, вычислить производное значение или провалидировать вход. Для этого dataclass вызывает `__post_init__`, если он определён:

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # не принимается в __init__, вычисляется сама

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("стороны должны быть положительными")
        self.area = self.width * self.height
```

## `order=True` — сравнение по порядку

```python
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int
```

`order=True` дополнительно генерирует `__lt__`, `__le__`, `__gt__`, `__ge__`, сравнивающие поля как кортеж по порядку объявления (`(major, minor, patch)`) — что делает экземпляры сортируемыми через `sorted()` без ручной реализации `__lt__`.

## Когда dataclass не подходит

Dataclass — это класс с данными и минимальной логикой. Если у класса сложное поведение, множество вычисляемых методов и данные — второстепенны, обычный класс (или `@property` — см. [05_property_and_encapsulation.md](./05_property_and_encapsulation.md)) может быть яснее.
