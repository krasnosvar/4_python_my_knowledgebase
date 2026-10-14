# Решение: упражнение 5. restore, reset и revert

Условие: [../03_exercises/05_restore_reset_revert.md](../03_exercises/05_restore_reset_revert.md).

## 1. restore — отменить незакоммиченную правку

```bash
cd ~/git-practice/ex05
git restore scratch.py
cat scratch.py
```

```
ORIGINAL = "keep me"
```

## 2. restore --staged — убрать файл из staging area

```bash
echo "TEMP = 1" > draft.py
git add draft.py
git status --short
```

```
A  draft.py
```

```bash
git restore --staged draft.py
git status --short
```

```
?? draft.py
```

## 3. revert — отменить опубликованный коммит

Находим хеш нужного коммита:

```bash
git log --oneline
```

```
8962ae4 chore: add scratch module
dfe2c6d feat: report v3 (bug: broke report output)
ede6de7 feat: report v2
66c6391 chore: initial report module
```

```bash
git revert --no-edit dfe2c6d     # подставьте свой хеш
cat report.py
```

```
[main a359bd8] Revert "feat: report v3 (bug: broke report output)"
 1 file changed, 1 insertion(+), 1 deletion(-)
def build_report():
    return "report v2"
```

## 4. reset — убрать локальный коммит

```bash
git add draft.py
git commit -m "wip: draft"
git reset HEAD~1
git status --short
```

```
[main 5c1e2a0] wip: draft
 1 file changed, 1 insertion(+)
 create mode 100644 draft.py
?? draft.py
```

## Почему так

| Ситуация | Инструмент | Что происходит с историей |
| :--- | :--- | :--- |
| Правка в файле ещё не закоммичена | `git restore <file>` | Не меняется |
| Файл случайно добавлен в staging area | `git restore --staged <file>` | Не меняется |
| Плохой коммит уже отправлен и виден другим | `git revert <hash>` | Дополняется новым коммитом |
| Плохой коммит только у вас локально | `git reset HEAD~1` | Коммит удаляется из ветки |

Хеш коммита надёжнее, чем `HEAD~N`: со смещением легко ошибиться на
единицу и откатить не тот коммит.

`git reset` без флага работает в режиме `--mixed`: убирает коммит и
снимает изменения со staging area, но оставляет файлы на диске. Поэтому
`draft.py` снова стал untracked.
