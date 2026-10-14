# Python изнутри (CPython) — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). Значения ниже
сняты на CPython 3.14 (64 бит); там, где поведение зависит от версии, она
указана. ⚠️ — частая ошибка или опасная операция.

## Память и подсчёт ссылок

Подробнее: [01_memory_model_refcounting.md](./01_theory/01_memory_model_refcounting.md).

| Задача | Код | Заметка |
| :--- | :--- | :--- |
| Сколько ссылок на объект | `sys.getrefcount(obj)` | на 1 больше реального: аргумент вызова — тоже ссылка |
| Размер самого объекта | `sys.getsizeof(obj)` | `0` → 28, `[]` → 56, `[1, 2, 3]` → 88 байт; содержимое не учитывается |
| Увеличить refcount | присвоить, положить в контейнер, передать в функцию | — |
| Уменьшить refcount | `del x`, выход из области видимости, перезапись, удаление из контейнера | при 0 объект уничтожается **сразу** |
| Бессмертные объекты (3.12+, PEP 683) | `sys.getrefcount(None)` | огромное фиксированное число (3.14: `3221225472`) — счётчик не меняется |
| Слабая ссылка (не держит объект) | `r = weakref.ref(obj)`; `r()` | `r()` вернёт `None`, когда объект удалён |

```python
import sys, weakref

x = [1, 2, 3]
print(sys.getrefcount(x))       # 2: x + временная ссылка аргумента

class Node: pass
n = Node()
r = weakref.ref(n)
print(r() is n)                  # True
del n                            # refcount -> 0, объект уничтожен сразу
print(r())                       # None
```

## Сборщик мусора (`gc`)

Подробнее: [02_garbage_collector_generations.md](./01_theory/02_garbage_collector_generations.md).

| Задача | Код | Заметка |
| :--- | :--- | :--- |
| Пороги поколений | `gc.get_threshold()` | 3.12–3.13: `(700, 10, 10)`; 3.14: `(2000, 10, 10)` |
| Текущие счётчики | `gc.get_count()` | — |
| Собрать сейчас | `gc.collect()` | возвращает число найденных недостижимых объектов |
| Выключить / включить автосборку | `gc.disable()` / `gc.enable()` | refcounting продолжает работать |
| Отслеживается ли объект | `gc.is_tracked(obj)` | `[1, 2]` → True; `(1, 2)`, `"str"` → False |
| Статистика по поколениям | `gc.get_stats()` | `collections`, `collected`, `uncollectable` |
| Тюнинг порогов | `gc.set_threshold(...)` | редкая узкая оптимизация |

```python
import gc

class Node: pass
a, b = Node(), Node()
a.other, b.other = b, a          # цикл: refcount каждого никогда не станет 0
del a, b
print(gc.collect() >= 2)         # True — GC нашёл и удалил оба объекта
```

## Байткод и `dis`

Подробнее: [03_bytecode_and_dis.md](./01_theory/03_bytecode_and_dis.md).

| Задача | Код |
| :--- | :--- |
| Дизассемблировать функцию | `dis.dis(func)` |
| Сырые байты байткода | `func.__code__.co_code` |
| Локальные переменные / константы / число позиционных аргументов | `code.co_varnames` / `code.co_consts` / `code.co_argcount` |
| Таблица инструкций текущей версии | `dis.opmap` |
| Из терминала | `python3 -m dis script.py` |

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

Вывод на 3.14. На 3.13 вместо `..._BORROW` — `LOAD_FAST_LOAD_FAST`, на 3.12 —
два `LOAD_FAST` и колонка смещений; с 3.13 смещения скрыты, вернуть:
`dis.dis(add, show_offsets=True)`.

```text
  3           RESUME                   0

  4           LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE
```

| Факт | Версия |
| :--- | :--- |
| `.pyc` несовместимы между минорными версиями (`module.cpython-314.pyc`) | всегда |
| Specializing adaptive interpreter (PEP 659) — инструкции специализируются под типы | 3.11+ |
| `RESUME` в начале каждой функции | 3.11+ |

## Профилирование

Подробнее: [04_profiling_cprofile_timeit_tracemalloc.md](./01_theory/04_profiling_cprofile_timeit_tracemalloc.md).

| Вопрос | Инструмент | Команда |
| :--- | :--- | :--- |
| Какая функция съедает время во всей программе | `cProfile` | `python3 -m cProfile -s cumulative script.py` |
| Сохранить профиль в файл и разобрать | `cProfile` + `pstats` | `python3 -m cProfile -o out.prof script.py` |
| Что быстрее — вариант A или B одной строки | `timeit` | `python3 -m timeit -s "data = list(range(1000))" "sum(data)"` |
| Где выделяется память, которая не освобождается | `tracemalloc` | снапшоты до/после + `compare_to` |
| Время одного интервала в работающем коде | `time.perf_counter()` | — |

| Колонка `cProfile` | Значение | Сортировка находит |
| :--- | :--- | :--- |
| `ncalls` | сколько раз вызвана | — |
| `tottime` | время внутри функции без вложенных вызовов | функции, медленные сами по себе |
| `cumtime` | время вместе с вложенными вызовами | «точки входа», где копится время |

```python
import cProfile, pstats, timeit, tracemalloc

def work():
    return sum(i * i for i in range(100_000))

cProfile.run("work()", "out.prof")
pstats.Stats("out.prof").sort_stats("cumulative").print_stats(3)

print(timeit.timeit("sum(range(1000))", number=1000))

tracemalloc.start()
before = tracemalloc.take_snapshot()
leak = [str(i) for i in range(50_000)]
after = tracemalloc.take_snapshot()
for stat in after.compare_to(before, "lineno")[:3]:
    print(stat)                  # файл:строка с наибольшим приростом памяти
```

## Альтернативные реализации

Подробнее: [05_alternative_implementations.md](./01_theory/05_alternative_implementations.md).

| Реализация | Суть | Когда рассмотреть | Ограничение |
| :--- | :--- | :--- | :--- |
| CPython | эталон, байткод + интерпретатор, GIL | по умолчанию; веб-бэкенд, C-расширения | GIL мешает CPU-параллелизму потоков |
| CPython free-threaded (PEP 703) | сборка без GIL (`python3.14t`) | CPU-bound потоки | 3.13 — эксперимент, 3.14 — официально (PEP 779), но опционально; однопоток медленнее, C-расширения должны поддерживать режим |
| Субинтерпретаторы (PEP 734) | `concurrent.interpreters`, свой GIL у каждого | параллелизм в обычной сборке | 3.14+; данные — явно через очереди |
| PyPy | JIT-компиляция | CPU-bound чистый Python | хуже совместимость с C-расширениями; свой GIL |
| Jython / IronPython | Python на JVM / .NET | интеграция с Java / .NET | отстают по версиям языка, нет C-расширений |
| GraalPy | GraalVM + Truffle JIT | встраивание в JVM-системы, полиглот | моложе, реже в проде |
| MicroPython | урезанный рантайм | микроконтроллеры (ESP32 и т.п.) | урезанная stdlib, не для серверов |

Проверить, включён ли GIL: `sys._is_gil_enabled()` (3.13+);
free-threaded ли сборка: `sysconfig.get_config_var("Py_GIL_DISABLED")`.

## Типичные ошибки

- ⚠️ Ждать, что `del obj` освободит память, когда на объект ещё есть ссылки.
- ⚠️ Полагаться на момент вызова `__del__` — в PyPy он позже; ресурсы закрывайте через `with`.
- ⚠️ Сложная логика в `__del__` у объектов в циклах — порядок вызова не гарантирован (3.4+, PEP 442).
- ⚠️ `gc.disable()` в долгоживущем сервисе — циклические структуры будут копиться.
- ⚠️ «Утечка» обычно — забытая сильная ссылка (глобальный кэш, список подписчиков, замыкание), а не сбой GC.
- ⚠️ Оптимизировать «на глаз» до профилирования — узкое место часто не там.
- ⚠️ `timeit` отключает GC на время замера — в проде цифры могут быть хуже.
- ⚠️ Сравнивать вывод `dis` между версиями Python — набор инструкций не стабилен.
