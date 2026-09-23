# Python Under The Hood

Как устроен CPython изнутри: модель памяти и подсчёт ссылок, generational
garbage collector, байткод и `dis`, профилирование (`cProfile`, `timeit`,
`tracemalloc`), краткое сравнение с альтернативными реализациями (PyPy и
другие).

## Структура

- `01_theory/` — пять тем: refcounting и модель памяти; generational GC;
  байткод и `dis`; профилирование; альтернативные реализации Python.
- `02_examples/` — 6 runnable-примеров.
- `03_exercises/` — 6 упражнений с `TODO`.
- `04_exercises_answers/` — готовые решения.

## Как проходить

1. `01_memory_model_refcounting.md` → `02_garbage_collector_generations.md`
   — фундамент: почему Python управляет памятью именно так, и где
   refcounting не справляется сам.
2. `03_bytecode_and_dis.md` — как код вообще исполняется интерпретатором.
3. `04_profiling_...md` — практические инструменты диагностики
   производительности и памяти, применимые к любому коду из предыдущих
   разделов базы.
4. `05_alternative_implementations.md` — контекст: что меняется, если
   уйти от CPython.

## Запуск примеров и упражнений

```bash
python 02_examples/02_gc_generations_demo/main.py
python 03_exercises/01_track_refcount_of_object/main.py
```
