# Упражнение 4. Безопасный amend последнего коммита

Теория: [03_conflicts_and_hygiene.md → `git commit --amend`](../01_theory/03_conflicts_and_hygiene.md#git-commit---amend--исправление-последнего-коммита).

## Подготовка

```bash
mkdir -p ~/git-practice/ex04
cd ~/git-practice/ex04
git init -b main

cat > parser.py <<'EOF'
def parse_line(line):
    return line.strip()
EOF
git add parser.py
git commit -m "chore: initial parser"

cat > parser.py <<'EOF'
def parse_line(line):
    if not line:
        raise ValueError("empty line")
    return line.strip()
EOF
git add parser.py
git commit -m "fix bug"

echo "# заметки: parse_line теперь бросает ValueError на пустой строке" > parser_notes.md
```

Что получилось:

- последний коммит называется `fix bug` — сообщение не объясняет, что
  изменилось;
- файл `parser_notes.md` должен был войти в тот же коммит, но его забыли
  добавить.

Коммит существует **только локально** и никуда не отправлен — значит, его
безопасно переписать.

## Задание

1. Добавьте `parser_notes.md` в staging area.
2. Одной командой `git commit --amend` включите его в последний коммит
   **и** замените сообщение на осмысленное, например
   `fix: raise ValueError on empty line in parse_line()`.

## Проверь себя

```bash
git log --oneline
```

```
7852657 fix: raise ValueError on empty line in parse_line()
a3a3ba2 chore: initial parser
```

Коммитов по-прежнему **два**, а не три: файл вошёл в существующий коммит.
Сообщения `fix bug` больше нет.

```bash
git show --stat HEAD
```

В конце вывода — оба файла:

```
 parser.py       | 2 ++
 parser_notes.md | 1 +
 2 files changed, 3 insertions(+)
```

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

## Подсказки

- `git commit --amend -m "..."` задаёт новое сообщение сразу. Без `-m`
  откроется редактор.
- Если бы коммит уже был отправлен и его видели коллеги, amend делать не
  стоило бы — тогда правильный инструмент `git revert` (упражнение 5).

Решение: [../04_exercises_answers/04_amend_commit_safely.md](../04_exercises_answers/04_amend_commit_safely.md).
