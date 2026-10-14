# ООП в Python — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.

## Класс за 10 секунд

```python
class Account:
    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner            # атрибут экземпляра
        self.balance = balance

    def deposit(self, amount: float) -> None:   # метод: первым идёт self
        self.balance += amount

a = Account("Аня", 100)               # Python вызовет __init__(a, "Аня", 100)
a.deposit(50)                         # == Account.deposit(a, 50)
print(a.balance)                      # 150
```

Основы: [01_what_is_a_class.md](./01_theory/01_what_is_a_class.md).

## Магические методы

Подробно: [02_classes_and_magic_methods.md](./01_theory/02_classes_and_magic_methods.md).

| Нужно | Метод | Когда вызывает Python |
| :--- | :--- | :--- |
| Создать объект (редко) | `__new__(cls, ...)` | до `__init__`; синглтоны, наследники `int`/`str`/`tuple` |
| Заполнить объект | `__init__(self, ...)` | сразу после `__new__`, обязан вернуть `None` |
| Отладочное представление | `__repr__` | консоль, `repr()`, печать внутри `list`/`dict`, fallback для `str()` |
| Представление для пользователя | `__str__` | `print()`, `str()`, f-строка без `!r` |
| Сравнение по значению | `__eq__` | `==` (без него `==` работает как `is`) |
| Ключ `dict` / элемент `set` | `__hash__` | `hash()`; обязан быть согласован с `__eq__` |
| Длина и truthiness | `__len__` | `len()`, `if obj:` (если нет `__bool__`) |
| Доступ по индексу/ключу | `__getitem__` / `__setitem__` | `obj[k]`, `obj[k] = v`; `__getitem__` даёт и `for` без `__iter__` |
| Операторы | `__add__`, `__sub__`, `__mul__`, `__lt__`, `__contains__` | `+`, `-`, `*`, `<`, `in` |

```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Point(x={self.x!r}, y={self.y!r})"     # !r — repr() значения

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:                          # те же поля, что в __eq__
        return hash((self.x, self.y))

print({Point(1, 2), Point(1, 2)})                       # {Point(x=1, y=2)}
```

## Наследование, `super()`, MRO

Подробно: [03_inheritance_and_super.md](./01_theory/03_inheritance_and_super.md),
[04_mro_and_mixins.md](./01_theory/04_mro_and_mixins.md).

| Задача | Синтаксис |
| :--- | :--- |
| Унаследовать | `class Dog(Animal):` |
| Переопределить метод | объявить метод с тем же именем в подклассе |
| Расширить метод родителя | `result = super().speak()` + своя логика |
| Инициализировать базовую часть | `super().__init__(name)` — всегда, даже при одиночном наследовании |
| Посмотреть порядок поиска методов | `Cls.__mro__` или `Cls.mro()` |
| Примешать возможность | `class User(JSONMixin, Base):` — миксин **перед** основной базой |

```python
class Base:
    def greet(self) -> str: return "Base"
class Left(Base):
    def greet(self) -> str: return "Left -> " + super().greet()
class Right(Base):
    def greet(self) -> str: return "Right -> " + super().greet()
class Child(Left, Right): pass

print([c.__name__ for c in Child.__mro__])  # ['Child', 'Left', 'Right', 'Base', 'object']
print(Child().greet())                      # Left -> Right -> Base
```

`super()` — следующий класс **по MRO** экземпляра, а не «родитель»: в `Left`
он ведёт в `Right`.

## `@dataclass`

Подробно: [05_dataclasses.md](./01_theory/05_dataclasses.md).

| Параметр / приём | Что даёт |
| :--- | :--- |
| `@dataclass` | `__init__`, `__repr__`, `__eq__` по полям; `__hash__ = None` (нехешируем) |
| `@dataclass(frozen=True)` | присваивание → `FrozenInstanceError`; генерируется `__hash__` |
| `@dataclass(order=True)` | `<`, `<=`, `>`, `>=` как сравнение кортежа полей; работает `sorted()` |
| `field(default_factory=list)` | свой новый список для каждого экземпляра |
| `field(init=False)` | поле не принимается в `__init__` (вычисляется в `__post_init__`) |
| `def __post_init__(self)` | валидация и производные поля после генерированного `__init__` |

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)

print(sorted([Version(2), Version(1, 5)]))   # [Version(major=1, minor=5, tags=()), Version(major=2, minor=0, tags=())]
print(hash(Version(1)) == hash(Version(1)))  # True
```

## Инкапсуляция и `@property`

Подробно: [06_property_and_encapsulation.md](./01_theory/06_property_and_encapsulation.md).

| Запись | Смысл |
| :--- | :--- |
| `self.name` | обычный публичный атрибут — по умолчанию в Python |
| `self._name` | «внутреннее», только соглашение, интерпретатор не проверяет |
| `self.__name` | name mangling → `_ClassName__name`; защита от конфликта имён в подклассах, не безопасность |
| `@property` | чтение `obj.x` через метод (вычисляемое / только для чтения) |
| `@x.setter` | валидация при `obj.x = v` |
| `@x.deleter` | перехват `del obj.x` |

Когда `@property`: валидация при записи, вычисляемое из других полей значение,
поле стало вычисляемым, а API `obj.x` нужно сохранить. Иначе — обычный атрибут.

## ABC или Protocol

Подробно: [07_duck_typing_and_protocols.md](./01_theory/07_duck_typing_and_protocols.md).

| | `abc.ABC` + `@abstractmethod` | `typing.Protocol` |
| :--- | :--- | :--- |
| Совместимость | номинальная (явное наследование) | структурная (совпадение по форме) |
| Проверка | в рантайме: `TypeError` при создании экземпляра без реализации | статически (mypy/pyright); в рантайме — нет |
| Брать, когда | своя иерархия, контракт нужно навязать | чужие/сторонние классы, слабая связанность |

## SOLID одной строкой

Подробно: [08_solid_in_python.md](./01_theory/08_solid_in_python.md).

| Принцип | Правило | Типичный приём в Python |
| :--- | :--- | :--- |
| S — единственная ответственность | одна причина для изменения класса | разделить валидацию / хранение / уведомления |
| O — открыт/закрыт | новое поведение — новым кодом | стратегия через `Protocol` вместо `if/elif` |
| L — подстановка Лисков | подкласс заменяет базу без поломок | `Square` не наследует `Rectangle` с независимыми сторонами |
| I — разделение интерфейсов | не заставлять реализовывать ненужное | несколько маленьких `Protocol` вместо одного «толстого» |
| D — инверсия зависимостей | зависеть от абстракции | передавать репозиторий в `__init__` (DI), подменять в тестах |

## Ловушки

- ⚠️ Определили `__eq__` без `__hash__` → объект нехешируем (`TypeError: unhashable type`).
- ⚠️ `__hash__` по изменяемым полям → объект «теряется» в `set`/`dict` после изменения.
- ⚠️ Нет `__repr__` → в логах `<__main__.Point object at 0x...>`.
- ⚠️ Забыли `super().__init__()` → `AttributeError` на атрибутах базы.
- ⚠️ `items: list = []` в dataclass → `ValueError` при определении класса; нужен `field(default_factory=list)`.
- ⚠️ Обычный dataclass нехешируем; для ключа `dict` — `frozen=True`.
- ⚠️ `__add__`, который меняет операнд или делает побочный эффект, — источник трудноуловимых багов.
- ⚠️ Геттеры/сеттеры «на всякий случай» — не идиоматично; `@property` вводят по необходимости.
- ⚠️ Наследование ради «is-a из жизни» (квадрат — прямоугольник) может нарушить LSP.
