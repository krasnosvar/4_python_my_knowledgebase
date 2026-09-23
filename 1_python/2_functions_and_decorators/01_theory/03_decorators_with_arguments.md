# Декораторы с аргументами

Обычный декоратор принимает ровно один аргумент — оборачиваемую функцию. Если декоратору
нужны собственные параметры (`@retry(times=3)`), требуется ещё один уровень вложенности —
**фабрика декораторов**.

## Три уровня вложенности

```python
def retry(times):                      # уровень 1: фабрика — принимает аргументы декоратора
    def decorator(func):               # уровень 2: сам декоратор — принимает функцию
        def wrapper(*args, **kwargs):  # уровень 3: обёртка — принимает аргументы вызова
            last_exc = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
            raise last_exc
        return wrapper
    return decorator

@retry(times=3)
def flaky():
    ...
```

Разбор по шагам: `@retry(times=3)` сначала вызывает `retry(3)`, которая возвращает `decorator`.
Именно `decorator` затем применяется к `flaky` — так же, как в обычном декораторе без
аргументов. То есть `@retry(times=3)` эквивалентно `flaky = retry(3)(flaky)`.

Каждый уровень — это замыкание: `decorator` захватывает `times` из `retry`, а `wrapper`
захватывает `func` из `decorator`.

## Декораторы на основе класса

Вместо трёх вложенных функций декоратор с состоянием можно реализовать классом с методом
`__call__`, который делает экземпляр класса вызываемым (callable):

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def greet():
    ...

greet()
greet.calls  # 1
```

Такой подход удобен, когда декоратору нужно хранить состояние между вызовами (счётчики, кэш) —
состояние естественно живёт в атрибутах экземпляра, а не в замыкании.

Декоратор-фабрику тоже можно построить на классах: `__init__` принимает параметры декоратора,
а `__call__` — оборачиваемую функцию и возвращает готовую обёртку.

## Параметризованные декораторы из стандартной библиотеки

Два показательных примера из `functools`, устроенных именно как фабрики декораторов:

* **`functools.lru_cache(maxsize=...)`** — кэширует результаты вызовов по аргументам
  (мемоизация "из коробки"); `maxsize` — это параметр фабрики, точно как `times` у `retry`.
* **`functools.singledispatch`** — превращает обычную функцию в generic-функцию, выбирающую
  реализацию по типу первого аргумента; дополнительные реализации регистрируются через
  `@func.register(SomeType)`, что само по себе тоже декоратор.

```python
from functools import lru_cache, singledispatch

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@singledispatch
def render(value):
    raise NotImplementedError

@render.register(int)
def _(value):
    return f"int: {value}"
```
