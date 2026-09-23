# Контекст-менеджеры и `with`

Оператор `with` гарантирует, что код освобождения ресурса выполнится **всегда** — даже если
тело блока завершилось исключением. Это структурный аналог `try/finally`, но декларативный
и переиспользуемый.

## Протокол `__enter__` / `__exit__`

```python
class Resource:
    def __enter__(self):
        print("Открываем ресурс")
        return self  # то, что попадёт в переменную после `as`

    def __exit__(self, exc_type, exc_value, traceback):
        print("Закрываем ресурс")
        return False  # не подавлять исключение

with Resource() as r:
    ...
```

Порядок вызовов:

1. `with` вызывает `Resource().__enter__()`, результат кладётся в `r`.
2. Выполняется тело блока `with`.
3. `__exit__(exc_type, exc_value, traceback)` вызывается **всегда** — если исключений не было,
   все три аргумента равны `None`; если исключение возникло, туда передаются его тип, значение
   и трейсбек.

## Что делает возвращаемое значение `__exit__`

Если `__exit__` вернёт значение, приводимое к **истине** (`True`), исключение, возникшее внутри
`with`-блока, будет **подавлено** — оно не полетит дальше. Если вернуть `False`/`None` (или
ничего не возвращать — тогда неявный `return None`), исключение продолжит распространяться
как обычно.

```python
def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is ValueError:
        print("Подавляем ValueError")
        return True  # исключение "проглочено"
    return False      # остальные исключения пробрасываются дальше
```

Это неочевидный, но важный момент: `__exit__` — единственное место, где Python позволяет
контекст-менеджеру решать судьбу исключения из блока.

## `contextlib.contextmanager`

Писать класс с двумя методами ради простого контекст-менеджера часто избыточно. Декоратор
`@contextlib.contextmanager` позволяет написать то же самое как обычный генератор с одним
`yield`:

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("Открываем ресурс")
    try:
        yield "значение для as"
    finally:
        print("Закрываем ресурс")

with resource() as value:
    ...
```

Код до `yield` — это `__enter__`, значение после `yield` — то, что попадёт в переменную после
`as`, а код после `yield` (в `finally`) — это `__exit__`. Именно `try/finally` вокруг `yield`
гарантирует выполнение освобождения ресурса даже при исключении в теле `with`: исключение
"впрыгивает" в точку `yield` внутри генератора (через `.throw()`), и `finally` отрабатывает как
обычно.

Чтобы подавить исключение в генераторном варианте, нужно обернуть `yield` в `try/except` и
не пробрасывать исключение дальше — поведение симметрично `return True` из `__exit__`.

## Полезные помощники `contextlib`

* **`contextlib.suppress(*exceptions)`** — компактная замена `try/except: pass` для ожидаемых
  и намеренно игнорируемых исключений:

  ```python
  from contextlib import suppress

  with suppress(FileNotFoundError):
      os.remove("some_file.tmp")
  ```

* **`contextlib.ExitStack`** — динамически управляет произвольным (заранее неизвестным)
  количеством контекст-менеджеров, гарантируя корректное закрытие всех открытых к моменту
  исключения, в порядке, обратном открытию:

  ```python
  from contextlib import ExitStack

  with ExitStack() as stack:
      files = [stack.enter_context(open(name)) for name in filenames]
      ...
  ```
