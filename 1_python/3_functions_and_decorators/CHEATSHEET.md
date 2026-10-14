# Функции и декораторы — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая ловушка.

## lambda и функции высшего порядка

Теория: [01_lambdas.md](./01_theory/01_lambdas.md), [03_first_class_functions_and_closures.md](./01_theory/03_first_class_functions_and_closures.md)

| Задача | Синтаксис |
| :--- | :--- |
| Сортировка по ключу | `sorted(words, key=len)` |
| Ключ «на лету» | `sorted(words, key=lambda w: w[-1])` |
| Составной ключ | `key=lambda p: (p["last_name"], p["first_name"])` |
| Фильтр / отображение (ленивые) | `list(filter(lambda x: x % 2 == 0, xs))` / `list(map(f, xs))` |
| Свернуть в одно значение | `functools.reduce(lambda acc, x: acc + x, [1, 2, 3])` → `6` |
| Функция как значение | `say = greet` (без скобок — не вызов) |
| Условие внутри lambda | `lambda x: "+" if x > 0 else "-"` |

- Тело lambda — одно выражение: без присваиваний, циклов, `try`, `with`.
- ⚠️ `f = lambda x: ...` — PEP 8 (E731) против: в traceback имя `<lambda>`, нет docstring. Нужно имя — пишите `def`.
- Чаще вместо `map`/`filter` пишут comprehension: `[x * 10 for x in xs]`.

## *args, **kwargs, / и *

Теория: [02_args_kwargs.md](./01_theory/02_args_kwargs.md)

| Синтаксис | Смысл |
| :--- | :--- |
| `def f(*args)` | лишние позиционные → `tuple` |
| `def f(**kwargs)` | лишние именованные → `dict` |
| `f(*seq, **mapping)` | распаковка при вызове |
| `def f(a, b, /, c, *, d)` | `a`, `b` — только позиционные; `c` — как угодно; `d` — только по имени |
| `def connect(host, port, *, timeout=30)` | таймаут нельзя передать случайно позиционно |
| `super().__init__(*args, **kwargs)` | пробросить всё родителю |

## Замыкания и nonlocal

Теория: [03_first_class_functions_and_closures.md](./01_theory/03_first_class_functions_and_closures.md)

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count      # без него: UnboundLocalError на count += 1
        count += 1
        return count
    return increment
```

| Задача | Синтаксис |
| :--- | :--- |
| Заглянуть в захваченное | `f.__closure__[0].cell_contents` |
| Зафиксировать значение в цикле | `lambda i=i: i` или фабрика `make_lambda(i)` |

- Замыкание захватывает **переменную (cell)**, а не значение.
- ⚠️ `[lambda: i for i in range(3)]` → все вернут `2` (позднее связывание).
- `nonlocal` нужен только для присваивания; читать внешнюю переменную можно и без него.

## Декораторы

Теория: [04_decorators_basics.md](./01_theory/04_decorators_basics.md), [05_decorators_with_arguments.md](./01_theory/05_decorators_with_arguments.md)

```python
from functools import wraps

def log_calls(func):                       # без аргументов
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("вызов", func.__name__)
        return func(*args, **kwargs)
    return wrapper

def retry(times):                          # с аргументами: фабрика → декоратор → обёртка
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator
```

| Запись | Эквивалент |
| :--- | :--- |
| `@dec` над `def f` | `f = dec(f)` |
| `@retry(times=3)` | `f = retry(3)(f)` |
| `@a` над `@b` над `def f` | `f = a(b(f))`: применяются снизу вверх, при вызове выполняются сверху вниз |
| Исходная функция под обёрткой | `f.__wrapped__` (есть благодаря `@wraps`) |
| Декоратор с состоянием | класс с `__init__(self, func)` и `__call__` |

| Готовый декоратор | Для чего |
| :--- | :--- |
| `@functools.lru_cache(maxsize=128)` | мемоизация по аргументам (аргументы должны быть хешируемыми) |
| `@functools.cache` (3.9+) | то же без ограничения размера |
| `@functools.singledispatch` + `@f.register(int)` | выбор реализации по типу первого аргумента |

- ⚠️ Без `@wraps` у обёртки `__name__ == "wrapper"`, `__doc__ is None` — ломаются логи, `help()`, `inspect.signature`.
- ⚠️ `def wrapper(x)` вместо `*args, **kwargs` — декоратор ломается на других сигнатурах.
- ⚠️ Забыли `return func(...)` в обёртке — декорированная функция возвращает `None`.

## Контекст-менеджеры

Теория: [06_context_managers.md](./01_theory/06_context_managers.md)

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("открыли")         # = __enter__
    try:
        yield "значение"     # попадёт в `as`
    finally:
        print("закрыли")     # = __exit__, выполнится и при исключении

with resource() as value:
    ...
```

| Задача | Синтаксис |
| :--- | :--- |
| Гарантированно закрыть файл | `with open("notes.txt") as f:` |
| Протокол класса | `__enter__(self)` → значение для `as`; `__exit__(self, exc_type, exc, tb)` |
| Подавить исключение из блока | `__exit__` вернул `True` (в генераторе — `except` без `raise`) |
| Пропустить ожидаемую ошибку | `with suppress(FileNotFoundError): os.remove(path)` |
| Заранее неизвестное число ресурсов | `with ExitStack() as stack: stack.enter_context(open(n))` |

- `__exit__` вызывается всегда; без исключения все три аргумента — `None`.
- ⚠️ `yield` без `try/finally` в `@contextmanager` — при исключении код «закрытия» не выполнится.
- ⚠️ `__exit__`, случайно вернувший truthy, молча глотает все исключения.
