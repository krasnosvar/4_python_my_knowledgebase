# Тема 01. Git — что нужно знать для работы

## Зачем этот раздел

Git нужен с первого дня: в нём хранится код любого проекта, через него
вы получаете чужие изменения и отдаёте свои. Это не полный курс по Git, а
минимум, без которого тяжело работать в команде: базовый workflow,
ветвление и слияние, разрешение конфликтов и безопасная отмена изменений.

После раздела вы сможете создать репозиторий, делать атомарные коммиты,
работать в ветках, разрешить конфликт слияния и отменить ошибку, не
сломав историю коллегам.

**Пререквизиты:** терминал и команда `cd`. Знать Python не нужно.

**Уже знаете Git?** Сразу открывайте [CHEATSHEET.md](./CHEATSHEET.md) —
таблица «задача → команда».

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_basic_workflow.md](./01_theory/01_basic_workflow.md) — установка и
    первая настройка, три области Git,
    `init`/`clone`/`add`/`commit`/`push`/`pull`, `.gitignore`.
  - [02_branching_merging.md](./01_theory/02_branching_merging.md) — ветки,
    fast-forward vs three-way merge, rebase и когда его не стоит использовать.
  - [03_conflicts_and_hygiene.md](./01_theory/03_conflicts_and_hygiene.md) —
    разрешение конфликтов, commit hygiene, `restore`/`reset`/`revert`/`amend`.
- **[02_examples/](./02_examples/)** — пошаговые разборы: команда → её
  вывод → пояснение. Повторяйте команды у себя в терминале.
  - [01_basic_workflow.md](./02_examples/01_basic_workflow.md) — init →
    commit → ветка → fast-forward merge.
  - [02_conflict_walkthrough.md](./02_examples/02_conflict_walkthrough.md) —
    как возникает и решается конфликт слияния.
  - [03_undo_operations.md](./02_examples/03_undo_operations.md) —
    `restore`, `restore --staged`, `amend`, `revert`, `reset --soft`.
- **[03_exercises/](./03_exercises/)** — 5 упражнений: подготовка → задание
  → «Проверь себя».
- **[04_exercises_answers/](./04_exercises_answers/)** — решения с выводом
  команд и объяснением «почему так».
- **[CHEATSHEET.md](./CHEATSHEET.md)** — шпаргалка по всем командам раздела.

## Как проходить тему

1. Прочитать теорию по порядку — `01_theory/01` → `02` → `03`.
2. Повторить руками примеры из `02_examples/`, сверяя вывод.
3. Выполнить упражнения из `03_exercises/` — каждое заканчивается блоком
   «Проверь себя».
4. Сверить решение с `04_exercises_answers/`.

## Когда двигаться дальше

Когда без подсказок получается: закоммитить только нужные файлы, слить
ветку, разрешить конфликт и выбрать между `restore`, `reset` и `revert`.
Дальше — [02_docker_basics](../02_docker_basics/) или сразу
[1_python](../../1_python/), если Docker хотите отложить.
