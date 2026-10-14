# Пример 3. Отмена изменений: restore, amend, revert, reset

Повторяйте команды по порядку и сверяйте вывод (хеши у вас будут другими).
Теория:
[03_conflicts_and_hygiene.md → Отмена изменений](../01_theory/03_conflicts_and_hygiene.md#отмена-изменений-restore-reset-revert).

## 0. Подготовка: репозиторий с двумя коммитами

```bash
mkdir -p ~/git-practice/example-03
cd ~/git-practice/example-03
git init -b main

echo "print('start')" > main.py
git add main.py
git commit -m "chore: initial script"

echo "print('feature A')" >> main.py
git add main.py
git commit -m "feat: add feature A"

git log --oneline
```

```
8aa76be feat: add feature A
dc93b7f chore: initial script
```

`echo "текст" > файл` создаёт файл с этой строкой, `>>` — дописывает
строку в конец.

## 1. `git restore` — отменить незакоммиченную правку

```bash
echo "print('случайная строка')" >> main.py
git status --short
```

```
 M main.py
```

`M` — файл изменён, но правка ещё не в staging area.

```bash
git restore main.py
git status --short
cat main.py
```

```
print('start')
print('feature A')
```

`git status --short` ничего не вывел — изменений нет, файл снова как в
последнем коммите. ⚠️ Отменённая так правка не восстанавливается.

## 2. `git restore --staged` — убрать файл из staging area

```bash
echo "TEMP = 1" > scratch.py
git add scratch.py
git status --short
```

```
A  scratch.py
```

`A` — файл добавлен в staging area.

```bash
git restore --staged scratch.py
git status --short
```

```
?? scratch.py
```

`??` — untracked: файл остался на диске, но в коммит не попадёт.

```bash
rm scratch.py
```

## 3. `git commit --amend` — исправить последний коммит

Закоммитили с плохим сообщением:

```bash
echo "print('feature B')" >> main.py
git add main.py
git commit -m "add stuff"
```

Коммит ещё никуда не отправлен — значит, его можно переписать:

```bash
git commit --amend -m "feat: add feature B"
git log --oneline
```

```
9d0d847 feat: add feature B
8aa76be feat: add feature A
dc93b7f chore: initial script
```

Коммитов по-прежнему три: `--amend` **заменил** последний коммит новым (с
новым хешем), а не добавил ещё один.

## 4. `git revert` — отменить коммит, который уже видят другие

```bash
echo "DEBUG = True" >> main.py
git add main.py
git commit -m "chore: enable debug"
```

Представим, что этот коммит уже отправлен (`git push`) и коллеги его
скачали. Переписывать такую историю нельзя — отменяем **новым** коммитом:

```bash
git revert --no-edit HEAD
git log --oneline
cat main.py
```

```
12e6005 Revert "chore: enable debug"
24517d8 chore: enable debug
9d0d847 feat: add feature B
8aa76be feat: add feature A
dc93b7f chore: initial script
print('start')
print('feature A')
print('feature B')
```

Строки `DEBUG = True` в файле нет, но сам коммит `chore: enable debug`
остался в истории — revert её дополняет, а не переписывает. `HEAD` —
последний коммит; `--no-edit` — взять стандартное сообщение
`Revert "..."` без открытия редактора.

## 5. `git reset --soft` — отменить локальный коммит

```bash
echo "secret" > mistake.txt
git add mistake.txt
git commit -m "oops: wrong file"
```

Коммит только локальный — его можно убрать из истории:

```bash
git reset --soft HEAD~1
git log --oneline -n 2
git status --short
```

```
12e6005 Revert "chore: enable debug"
24517d8 chore: enable debug
A  mistake.txt
```

`HEAD~1` — «на один коммит назад». Коммита `oops` в истории больше нет, а
его изменения остались в staging area (`A`). Убираем и сам файл:

```bash
git restore --staged mistake.txt
rm mistake.txt
```

## Убрать за собой

```bash
cd ~
rm -rf ~/git-practice/example-03
```
