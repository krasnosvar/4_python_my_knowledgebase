# Решение: упражнение 3. Разрешение конфликта слияния

Условие: [../03_exercises/03_resolve_merge_conflict.md](../03_exercises/03_resolve_merge_conflict.md).

```bash
cd ~/git-practice/ex03
git merge feature/prod-settings
```

```
Auto-merging settings.py
CONFLICT (content): Merge conflict in settings.py
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
cat settings.py
```

```
<<<<<<< HEAD
DEBUG = True
MAX_CONNECTIONS = 50
=======
DEBUG = False
MAX_CONNECTIONS = 10
>>>>>>> feature/prod-settings
```

Обе строки попали в один конфликтный блок: правки в соседних строках Git
считает одним изменённым куском.

Открываем `settings.py` в редакторе и заменяем **весь** блок вместе с
маркерами на объединённый результат — `DEBUG` из входящей ветки,
`MAX_CONNECTIONS` из `main`:

```python
DEBUG = False
MAX_CONNECTIONS = 50
```

Завершаем merge:

```bash
git add settings.py
git commit -m "merge: resolve settings conflict"
git log --oneline --graph --all
```

```
*   224ae9e merge: resolve settings conflict
|\
| * d8cf124 feat: disable debug mode for production
* | a0cddf0 feat: raise max connections to 50
|/
* e8597de chore: initial settings
```

## Почему так

Разрешить конфликт — не «выбрать одну сторону», а собрать правильный
итоговый файл. Здесь нужны изменения обеих веток.

`git add` после правки означает «я разобрался с этим файлом». Git не
проверяет, удалены ли маркеры, — это ваша ответственность. Поэтому перед
коммитом стоит ещё раз выполнить `cat settings.py` или `git diff --staged`.
