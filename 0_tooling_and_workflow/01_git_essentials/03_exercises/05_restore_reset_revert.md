# Упражнение 5. restore, reset и revert

Теория: [03_conflicts_and_hygiene.md → Отмена изменений](../01_theory/03_conflicts_and_hygiene.md#отмена-изменений-restore-reset-revert).
Пошаговый пример: [02_examples/03_undo_operations.md](../02_examples/03_undo_operations.md).

## Подготовка

```bash
mkdir -p ~/git-practice/ex05
cd ~/git-practice/ex05
git init -b main

printf 'def build_report():\n    return "report v1"\n' > report.py
git add report.py
git commit -m "chore: initial report module"

printf 'def build_report():\n    return "report v2"\n' > report.py
git add report.py
git commit -m "feat: report v2"

printf 'def build_report():\n    return "BROKEN"\n' > report.py
git add report.py
git commit -m "feat: report v3 (bug: broke report output)"

echo 'ORIGINAL = "keep me"' > scratch.py
git add scratch.py
git commit -m "chore: add scratch module"

echo "ACCIDENTAL_LINE = True" >> scratch.py
```

Что получилось:

- 4 коммита на `main`. Коммит `feat: report v3 ...` сломал отчёт —
  считайте, что он **уже отправлен** и его видит команда;
- в `scratch.py` есть незакоммиченная лишняя строка
  `ACCIDENTAL_LINE = True`.

## Задание

1. **restore**: отмените незакоммиченную правку в `scratch.py` командой
   Git (не редактируя файл руками).
2. **restore --staged**: создайте файл `draft.py` с любым содержимым,
   добавьте его в staging area, затем уберите оттуда, не удаляя файл с
   диска.
3. **revert**: отмените эффект коммита `feat: report v3 ...`, **не
   удаляя** его из истории — он уже опубликован.
4. **reset**: закоммитьте `draft.py` коммитом `wip: draft`, затем
   передумайте и уберите этот коммит из истории командой `git reset` так,
   чтобы `draft.py` остался на диске. Этот коммит никуда не отправлялся —
   поэтому здесь `reset` допустим.

## Проверь себя

```bash
cat scratch.py
cat report.py
```

```
ORIGINAL = "keep me"
def build_report():
    return "report v2"
```

```bash
git log --oneline
```

```
a359bd8 Revert "feat: report v3 (bug: broke report output)"
8962ae4 chore: add scratch module
dfe2c6d feat: report v3 (bug: broke report output)
ede6de7 feat: report v2
66c6391 chore: initial report module
```

Пять коммитов: коммит `report v3` остался в истории, сверху — отменяющий
его revert-коммит, а коммита `wip: draft` нет.

```bash
git status --short
```

```
?? draft.py
```

`draft.py` на диске, но не отслеживается.

## Подсказки

- Чтобы сослаться на коммит, удобнее всего взять его хеш из
  `git log --oneline`.
- `git reset HEAD~1` убирает последний коммит, а его изменения оставляет в
  рабочей папке. Подробнее о режимах — в теории.

Решение: [../04_exercises_answers/05_restore_reset_revert.md](../04_exercises_answers/05_restore_reset_revert.md).
