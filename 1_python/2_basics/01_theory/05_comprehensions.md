# List/dict/set comprehensions

Comprehension — компактный синтаксис для построения коллекции из другой
последовательности, часто заменяющий явный цикл с
`append`/`.add()`/присваиванием по ключу.

## Синтаксис

```python
squares = [x ** 2 for x in range(10)]                      # list comprehension
name_lengths = {name: len(name) for name in names}         # dict comprehension
unique_lengths = {len(word) for word in words}              # set comprehension
gen = (x ** 2 for x in range(10))                           # generator expression (см. модуль 5)
```

Общая форма: `[выражение for переменная in источник if условие]`. Условие `if`
— необязательный фильтр.

## Почему comprehension часто быстрее и читаемее ручного цикла

```python
# Ручной цикл
result = []
for x in range(1000):
    if x % 2 == 0:
        result.append(x * 2)

# Comprehension
result = [x * 2 for x in range(1000) if x % 2 == 0]
```

Comprehension обычно быстрее эквивалентного цикла с `append`:

- тело comprehension выполняется в собственном оптимизированном фрейме, где
  обращение к переменной цикла — это быстрый доступ к локальной переменной;
- в ручном цикле `result.append(x)` на каждой итерации требует поиска атрибута
  `append` у объекта `result` (атрибутный доступ дороже, чем прямая операция
  накопления в comprehension) — на практике выигрыш обычно 20-50%, но не
  порядки.

Comprehension также читаемее, когда операция действительно укладывается в одно
выражение: она сразу сообщает «это преобразование/фильтрация коллекции», тогда
как явный цикл требует прочитать все строки, чтобы понять то же самое.

## Вложенные comprehensions

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]     # [1, 2, 3, 4, 5, 6]
# эквивалентно:
# for row in matrix:
#     for x in row:
#         flat.append(x)

transposed = [[row[i] for row in matrix] for i in range(2)]
```

Порядок `for` в comprehension совпадает с порядком вложенных циклов при ручной
записи — это частая путаница у новичков.

## Walrus-оператор `:=` внутри comprehension

Позволяет вычислить выражение один раз и переиспользовать его результат, не
вызывая функцию дважды:

```python
# Без walrus — функция вызывается дважды на элемент
results = [expensive(x) for x in data if expensive(x) > 0]

# С walrus — функция вызывается один раз
results = [y for x in data if (y := expensive(x)) > 0]
```

## Когда comprehension — плохая идея

Если внутри выражения появляются вложенные `if/else`, несколько уровней
вложенности циклов или побочные эффекты (логирование, мутация внешнего
состояния), comprehension превращается в трудночитаемую «простыню». В этом
случае — обычный цикл с понятными именами и промежуточными переменными почти
всегда предпочтительнее: читаемость важнее лаконичности.

```python
# Плохо — трудно понять с первого взгляда
result = [f(x) if cond1(x) else (g(x) if cond2(x) else None) for x in data if valid(x)]

# Лучше — обычный цикл
result = []
for x in data:
    if not valid(x):
        continue
    if cond1(x):
        result.append(f(x))
    elif cond2(x):
        result.append(g(x))
    else:
        result.append(None)
```
