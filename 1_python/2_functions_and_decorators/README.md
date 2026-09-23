# Тема 2. Функции и декораторы (Functions & Decorators)

Этот раздел посвящён функциям как объектам первого класса: замыканиям, декораторам (в том
числе параметризованным), протоколу `*args`/`**kwargs` и контекст-менеджерам. Отдельное
внимание уделено внутренним механизмам — что именно захватывает замыкание, почему декоратор
без `functools.wraps` ломает метаданные функции, и как `__exit__` может подавлять исключения.

## Структура раздела

* **[01_theory/](./01_theory/)** — теория (разбита по подтемам):
    * [01_first_class_functions_and_closures.md](./01_theory/01_first_class_functions_and_closures.md) — функции высшего порядка, что захватывает замыкание, `nonlocal`, ловушка позднего связывания в циклах.
    * [02_decorators_basics.md](./01_theory/02_decorators_basics.md) — десахаривание `@decorator`, зачем нужен `functools.wraps`, порядок применения/выполнения при стекировании декораторов.
    * [03_decorators_with_arguments.md](./01_theory/03_decorators_with_arguments.md) — декораторы-фабрики (три уровня вложенности), декораторы на основе класса (`__call__`), `functools.lru_cache` и `singledispatch`.
    * [04_args_kwargs.md](./01_theory/04_args_kwargs.md) — упаковка/распаковка `*args`/`**kwargs`, позиционные-только и именованные-только параметры (PEP 570), почему `**kwargs` обязателен для прозрачного декоратора.
    * [05_context_managers.md](./01_theory/05_context_managers.md) — протокол `__enter__`/`__exit__`, подавление исключений через возврат из `__exit__`, `contextlib.contextmanager`, `suppress`, `ExitStack`.
    * [06_lambdas.md](./01_theory/06_lambdas.md) — синтаксис и ограничения `lambda`, легитимные случаи применения, почему PEP 8 не рекомендует присваивать лямбду имени.
* **[02_examples/](./02_examples/)** — практические примеры:
    * [01_cli_utilities.py](./02_examples/01_cli_utilities.py) — реестр CLI-команд через декоратор `@command(name)` и контекст-менеджер для временной директории.
    * [02_system_infrastructure.py](./02_examples/02_system_infrastructure.py) — декоратор `retry` с backoff поверх нестабильной операции и контекст-менеджер на классе для управляемого "соединения".
    * [03_product_backend.py](./02_examples/03_product_backend.py) — ручная мемоизация через замыкание, логирующий декоратор с `functools.wraps` и `compose`-пайплайн функций.
* **[03_exercises/](./03_exercises/)** — интерактивные задачи для самопроверки с автопроверками `PASS`/`FAIL`:
    * `01_closure_counter` — замыкание-счётчик без утечки состояния.
    * `02_late_binding_bug` — исправление ловушки позднего связывания в цикле.
    * `03_simple_decorator` — декоратор `@timed`, сохраняющий метаданные функции.
    * `04_decorator_with_args` — декоратор-фабрика `@retry(times)`.
    * `05_args_kwargs_wrapper` — прозрачный декоратор `@log_calls` с произвольными аргументами.
    * `06_context_manager_class` — контекст-менеджер на классе с гарантированной очисткой.
    * `07_context_manager_generator` — тот же контекст-менеджер через `@contextlib.contextmanager`.
    * `08_lambda_sort_key` — сортировка записей по составному ключу через `lambda`.
* **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию по порядку, начиная с [01_first_class_functions_and_closures.md](./01_theory/01_first_class_functions_and_closures.md).
2. Запустите и изучите примеры из `02_examples/`:
   ```bash
   python 02_examples/02_system_infrastructure.py
   ```
3. Выполните задачи в `03_exercises/`. Запустите файл, чтобы увидеть встроенную самопроверку:
   ```bash
   python 03_exercises/03_simple_decorator.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.
