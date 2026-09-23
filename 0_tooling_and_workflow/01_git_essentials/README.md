# Тема 01. Git — что нужно знать для работы

Это не полный курс по Git, а тот минимум механики и привычек, без которого
тяжело работать в команде: базовый workflow, ветвление и слияние, разрешение
конфликтов и безопасная отмена изменений.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_basic_workflow.md](./01_theory/01_basic_workflow.md) — три области Git,
    `init`/`clone`/`add`/`commit`/`push`/`pull`, `.gitignore`.
  - [02_branching_merging.md](./01_theory/02_branching_merging.md) — ветки,
    fast-forward vs three-way merge, rebase и когда его не стоит использовать.
  - [03_conflicts_and_hygiene.md](./01_theory/03_conflicts_and_hygiene.md) —
    разрешение конфликтов, commit hygiene, `restore`/`reset`/`revert`/`amend`.
- **[02_examples/](./02_examples/)** — самостоятельные bash-скрипты,
  создающие временный репозиторий в `./sandbox` и проходящие сценарий целиком
  с комментариями:
  - `01_basic_workflow.sh` — init → commit → branch → fast-forward merge.
  - `02_conflict_walkthrough.sh` — как возникает и решается конфликт слияния.
  - `03_undo_operations.sh` — `restore`, `restore --staged`, `amend`,
    `revert`, `reset --soft`.
- **[03_exercises/](./03_exercises/)** — 5 практических сценариев с
  автопроверкой `PASS`/`FAIL` через `check.sh`.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения
  и скрипты `solve.sh`, прогоняющие сценарий целиком.

## Как проходить тему

1. Прочитать теорию по порядку — `01_theory/01` → `02` → `03`.
2. Запустить и разобрать примеры:
   ```bash
   bash 02_examples/01_basic_workflow.sh
   bash 02_examples/02_conflict_walkthrough.sh
   bash 02_examples/03_undo_operations.sh
   ```
3. Выполнить упражнения из `03_exercises/` — для каждого: `setup.sh` →
   решить руками в `sandbox/` → `check.sh` до состояния `PASS` по всем
   пунктам.
4. Сверить решение с `04_exercises_answers/`.
