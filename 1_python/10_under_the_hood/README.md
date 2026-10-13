# Тема 10. Python изнутри (Under The Hood)

Как устроен CPython изнутри: модель памяти и подсчёт ссылок, generational
garbage collector, байткод и `dis`, профилирование (`cProfile`, `timeit`,
`tracemalloc`), краткое сравнение с альтернативными реализациями (PyPy и
другие).

## Зачем этот раздел

В предыдущих разделах не раз встречалось «подробно — в
`10_under_the_hood`»: почему существует GIL, откуда берутся утечки памяти,
почему одна строка кода быстрее другой. Здесь эти «почему» получают ответ.
Практическая польза двойная: вы сможете **находить** реальные проблемы
производительности и памяти инструментами (`cProfile`, `tracemalloc`)
вместо гадания, и **объяснять** поведение Python, которое иначе выглядит
магией (циклические ссылки, `is` против `==`, медленные глобальные
переменные). Раздел завершающий: он опирается на всё пройденное выше.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_memory_model_refcounting.md](./01_theory/01_memory_model_refcounting.md)
    — куча, объекты, подсчёт ссылок.
  - [02_garbage_collector_generations.md](./01_theory/02_garbage_collector_generations.md)
    — где refcounting не справляется (циклы) и как помогает GC поколений.
  - [03_bytecode_and_dis.md](./01_theory/03_bytecode_and_dis.md) — как код
    вообще исполняется интерпретатором.
  - [04_profiling_cprofile_timeit_tracemalloc.md](./01_theory/04_profiling_cprofile_timeit_tracemalloc.md)
    — практические инструменты диагностики производительности и памяти.
  - [05_alternative_implementations.md](./01_theory/05_alternative_implementations.md)
    — что меняется, если уйти от CPython.
- **[02_examples/](./02_examples/)** — 6 runnable-примеров.
- **[03_exercises/](./03_exercises/)** — 6 упражнений с `TODO`.
- **[04_exercises_answers/](./04_exercises_answers/)** — готовые решения.

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
