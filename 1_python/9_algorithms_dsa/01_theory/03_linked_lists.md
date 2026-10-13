# Связные списки

**Связный список** — цепочка узлов, где каждый узел хранит значение и
ссылку на следующий узел. В отличие от `list` (динамического массива, где
элементы лежат подряд и доступны по индексу), до `k`-го элемента связного
списка можно дойти только пройдя по ссылкам от начала.

В Python нет встроенного типа связного списка (`list` — это динамический
массив) — но задачи на связные списки остаются полезным
упражнением на работу со ссылками и рекурсией, а сама
структура иногда нужна там, где важны O(1) вставка/удаление в середине
при наличии ссылки на узел (в реальном коде для этого чаще берут
`collections.deque`, но понимание устройства списка остаётся базой).

## Определение узла

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class ListNode:
    value: int
    next: Optional["ListNode"] = None
```

## Обход

```python
def to_list(head: ListNode | None) -> list[int]:
    result = []
    node = head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result
```

## Вставка и удаление

```python
def prepend(head: ListNode | None, value: int) -> ListNode:
    return ListNode(value, next=head)   # O(1) — новый узел становится головой

def delete_value(head: ListNode | None, value: int) -> ListNode | None:
    dummy = ListNode(0, next=head)      # фиктивный узел упрощает удаление головы
    prev, curr = dummy, head
    while curr is not None:
        if curr.value == value:
            prev.next = curr.next        # O(1) после нахождения узла
            break
        prev, curr = curr, curr.next
    return dummy.next
```

Приём **dummy node** (фиктивный узел перед головой) — стандартная техника,
убирающая частный случай "удаление/вставка в саму голову" из логики.

## Разворот списка (реверс)

Итеративный вариант, O(n) времени, O(1) памяти:

```python
def reverse(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next   # сохранить следующий узел до перезаписи ссылки
        curr.next = prev         # развернуть указатель
        prev = curr
        curr = next_node
    return prev
```

Ключевая ошибка новичков — забыть сохранить `curr.next` перед
перезаписью, из-за чего теряется остаток списка.

## Быстрый и медленный указатель (Floyd's cycle detection)

Определение середины списка и обнаружение цикла — оба используют два
указателя, движущихся с разной скоростью:

```python
def find_middle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow   # когда fast дошёл до конца, slow — в середине

def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:          # встретились — есть цикл
            return True
    return False
```

Если в списке цикл, `fast` (движется в 2 раза быстрее) неизбежно
"нагонит" `slow` изнутри цикла — O(n) времени, O(1) памяти, в отличие от
альтернативы через `set` посещённых узлов (O(n) памяти).

## Когда связный список реально уместен в Python

- Учебные задачи и понимание указателей/рекурсии — основная причина
  присутствия темы в этом разделе.
- LRU-кэш и подобные структуры с O(1) удалением произвольного узла —
  на практике `collections.OrderedDict`/`dict` (с 3.7+ сохраняющий порядок
  вставки) решают это без ручной реализации списка.
- Значимая вставка/удаление в начало без сдвига — `collections.deque`.

В подавляющем большинстве прикладного Python-кода `list` или `deque`
предпочтительнее самодельного связного списка — они быстрее за счёт
компактного представления в памяти и меньше кода.
