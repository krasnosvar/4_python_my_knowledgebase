# Массивы и строки: техники работы

`list` в Python — динамический массив (не связный список): элементы лежат
подряд в памяти, доступ по индексу — O(1). Строки — неизменяемые
последовательности символов с похожими операциями индексации, но без
возможности изменения на месте.

## Два указателя (two pointers)

Классический приём для задач на упорядоченные/симметричные структуры —
избежать вложенного цикла (O(n²)), пройдя массив за один проход двумя
указателями с разных концов или с разной скоростью:

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

O(n) времени, O(1) дополнительной памяти — вместо создания
развёрнутой копии (`s == s[::-1]`, тоже O(n), но с O(n) лишней памятью).

## Скользящее окно (sliding window)

Для задач "найти подотрезок с каким-то свойством" — окно `[left, right]`
расширяется вправо и сужается слева, избегая пересчёта с нуля на каждом шаге:

```python
def longest_unique_substring(s: str) -> int:
    seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1     # сдвигаем левую границу за повтор
        seen[char] = right
        best = max(best, right - left + 1)
    return best
```

O(n) вместо наивных O(n²)/O(n³) при переборе всех подотрезков.

## Префиксные суммы

Предвычисление накопленных сумм превращает "сумма подотрезка" из O(n) в
O(1) на запрос (за счёт O(n) предвычисления один раз):

```python
def build_prefix_sums(nums: list[int]) -> list[int]:
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return prefix

def range_sum(prefix: list[int], left: int, right: int) -> int:
    """Сумма nums[left:right] (правая граница не включена)."""
    return prefix[right] - prefix[left]
```

Полезно, когда нужно много запросов суммы по разным диапазонам одного и
того же массива — без префиксных сумм каждый запрос был бы O(n).

## Строки: специфика неизменяемости

```python
s = "hello"
# s[0] = "H"  # TypeError: строки неизменяемы

new_s = "H" + s[1:]  # каждое "изменение" создаёт новую строку
```

**Ловушка производительности**: конкатенация строк в цикле через `+=`
создаёт новую строку на каждой итерации — O(n²) суммарно для n конкатенаций:

```python
result = ""
for word in words:
    result += word + " "   # плохо: O(n²) при большом списке слов
```

Правильный способ — накопить части в списке и склеить один раз через
`str.join` (O(n)):

```python
result = " ".join(words)   # O(n)
```

## Сортировка как инструмент, а не самоцель

Многие задачи на массивы упрощаются предварительной сортировкой ценой
O(n log n), после чего решение становится линейным:

```python
def has_pair_with_sum(nums: list[int], target: int) -> bool:
    nums = sorted(nums)          # O(n log n)
    left, right = 0, len(nums) - 1
    while left < right:           # O(n) — два указателя после сортировки
        total = nums[left] + nums[right]
        if total == target:
            return True
        elif total < target:
            left += 1
        else:
            right -= 1
    return False
```

Итоговая сложность O(n log n) — хуже теоретического O(n) через
хеш-множество, но часто проще по коду и не требует лишней памяти под set.
