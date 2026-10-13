# Тема 4. ООП в Python (OOP)

Этот раздел посвящён объектно-ориентированному программированию в Python:
от того, что такое класс и объект, до магических методов, наследования и
MRO, миксинов, dataclasses, инкапсуляции через `@property`, структурной
типизации (`Protocol`) и принципов SOLID.

## Зачем этот раздел

Почти весь реальный Python-код — веб-фреймворки, ORM, тестовые библиотеки —
построен на классах: модель Django, схема Pydantic, клиент базы данных,
исключение — всё это классы. Без ООП такой код читается как набор магии.
После раздела вы сможете объявлять свои типы данных с поведением, понимать
чужие иерархии классов и решать, когда класс действительно нужен, а когда
хватит функции или dataclass.

Раздел начинается с нуля — [01_what_is_a_class.md](./01_theory/01_what_is_a_class.md)
не предполагает опыта ООП в других языках. В примерах используются
исключения (`raise ValueError(...)`) — они разобраны в
[1_python_fundamentals/06_exceptions](../1_python_fundamentals/06_exceptions/README.md).

## Структура раздела

* **[01_theory/](./01_theory/)** — теория (разбита по подтемам, читать по порядку):
  * [01_what_is_a_class.md](./01_theory/01_what_is_a_class.md) — с нуля: зачем нужны классы, класс и объект (экземпляр), атрибуты, методы, `self`, простой `__init__`.
  * [02_classes_and_magic_methods.md](./01_theory/02_classes_and_magic_methods.md) — `__init__`/`__new__`, `__repr__` против `__str__`, `__eq__` и его влияние на хешируемость, `__len__`, `__getitem__`/`__setitem__`, перегрузка операторов.
  * [03_inheritance_and_super.md](./01_theory/03_inheritance_and_super.md) — одиночное наследование, переопределение методов, что на самом деле делает `super()` и почему это не «просто вызов родителя».
  * [04_mro_and_mixins.md](./01_theory/04_mro_and_mixins.md) — множественное наследование, C3-линеаризация, `__mro__`, ромбовидное наследование (diamond problem), миксины.
  * [05_dataclasses.md](./01_theory/05_dataclasses.md) — `@dataclass`, `field(default_factory=...)`, `frozen=True`, `__post_init__`, `order=True`.
  * [06_property_and_encapsulation.md](./01_theory/06_property_and_encapsulation.md) — `@property`/`@x.setter`/`@x.deleter`, name mangling, отсутствие настоящей приватности в Python.
  * [07_duck_typing_and_protocols.md](./01_theory/07_duck_typing_and_protocols.md) — утиная типизация, `abc.ABC`/`@abstractmethod` (номинальная типизация) против `typing.Protocol` (структурная типизация).
  * [08_solid_in_python.md](./01_theory/08_solid_in_python.md) — принципы SOLID на идиоматичном Python с примерами «до/после».
* **[02_examples/](./02_examples/)** — практические примеры:
  * [01_cli_utilities.py](./02_examples/01_cli_utilities.py) — система команд CLI на `typing.Protocol` (утиная типизация обработчиков) и `@dataclass` для конфигурации.
  * [02_system_infrastructure.py](./02_examples/02_system_infrastructure.py) — миксины (`JSONSerializableMixin`, `LoggingMixin`) в сервисах здоровья системы, инспекция `__mro__`.
  * [03_product_backend.py](./02_examples/03_product_backend.py) — рефакторинг сервиса обработки заказов по SOLID (до/после) и value-объект `Money` с `__eq__`/`__repr__`/`__add__`.
* **[03_exercises/](./03_exercises/)** — интерактивные задачи для самопроверки с автопроверками `PASS`/`FAIL`:
  * `01_magic_methods_vector` — класс `Vector` с `__add__`, `__eq__`, `__repr__`, `__mul__`.
  * `02_inheritance_super` — иерархия `Animal`/`Dog`/`Cat` с корректным использованием `super().__init__()`.
  * `03_mro_diamond` — ромбовидное наследование и предсказание порядка разрешения методов.
  * `04_mixin` — переиспользуемый миксин для двух несвязанных классов.
  * `05_dataclass_refactor` — превращение рукописного класса в эквивалентный `@dataclass`.
  * `06_property_validation` — класс с валидацией значения через `@property`.
  * `07_protocol_duck_typing` — `typing.Protocol` и структурная совместимость без наследования.
  * `08_solid_srp_refactor` — рефакторинг «божественного класса» по принципу единственной ответственности.
* **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию по порядку от `01` до `08`, начиная с [01_what_is_a_class.md](./01_theory/01_what_is_a_class.md).
2. Запустите и изучите примеры из папки `02_examples/`:
   ```bash
   python 02_examples/02_system_infrastructure.py
   ```
3. Выполните задачи в `03_exercises/`. Запустите файл для самопроверки:
   ```bash
   python 03_exercises/06_property_validation.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.
