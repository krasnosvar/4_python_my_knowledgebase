# Базовый workflow: init, clone, add, commit, push, pull

Git — это не система diff'ов, а система снэпшотов. Каждый коммит — это полный
слепок состояния файлов (с дедупликацией через content-addressable storage по
SHA), а не список изменений относительно предыдущей версии. Это объясняет,
почему переключение веток и большинство операций в Git такие быстрые.

## Три области Git

- **Working directory** — файлы на диске, с которыми вы реально работаете.
- **Staging area (index)** — «черновик» следующего коммита. Сюда попадает то,
  что вы явно добавили через `git add`.
- **Repository (`.git`)** — история коммитов.

```
working directory --(git add)--> staging area --(git commit)--> repository
```

⚠️ Главная ловушка новичков: **`git commit` сохраняет не файлы на диске, а
содержимое staging area**. Если вы поправили файл после `git add`, но не
добавили правку повторно — она не попадёт в коммит.

## Базовые команды

```bash
git init                 # создать новый репозиторий в текущей папке
git clone <url>           # склонировать существующий репозиторий

git status                 # что изменено / что застейджено
git add <file>             # добавить файл в staging area
git add -p                 # добавить изменения выборочно, по кускам (hunk)
git commit -m "message"    # закоммитить содержимое staging area
git log --oneline --graph  # компактная история с ветками
```

`git diff` и `git diff --staged` — разные команды:

| Команда | Что показывает |
| :--- | :--- |
| `git diff` | Working directory vs staging area (что ещё не добавлено) |
| `git diff --staged` (он же `--cached`) | Staging area vs последний коммит (что попадёт в коммит) |

## Remote: push, pull, fetch

```bash
git remote add origin <url>
git push -u origin main    # -u привязывает локальную ветку к remote-ветке
git push                    # дальше достаточно просто `git push`

git fetch                   # скачать изменения, НЕ трогая рабочие файлы
git pull                     # fetch + merge (или rebase, см. ниже) текущей ветки
```

`git pull` под капотом — это `git fetch` + слияние. Именно поэтому `git pull`
иногда приводит к конфликтам: вы на самом деле мержите чужие изменения в свою
ветку. Поведение слияния настраивается через `pull.rebase`:

```bash
git config pull.rebase false   # merge (поведение по умолчанию)
git config pull.rebase true    # rebase вместо merge (см. 02_branching_merging.md)
```

## .gitignore

`.gitignore` описывает паттерны файлов, которые Git не должен *начинать*
отслеживать:

```gitignore
# Python
__pycache__/
*.pyc
.venv/
venv/

# окружение и секреты
.env

# IDE
.idea/
.vscode/

# артефакты
dist/
*.egg-info/
```

⚠️ Частая ловушка: **`.gitignore` не действует на файлы, которые уже
отслеживаются**. Если файл случайно закоммитили раньше, добавление его в
`.gitignore` ничего не изменит — Git продолжит видеть его изменения. Нужно
явно убрать файл из индекса:

```bash
git rm --cached path/to/file       # убрать из репозитория, оставить на диске
git rm -r --cached __pycache__/    # то же самое для директории
git commit -m "chore: stop tracking generated files"
```

## Полезные вспомогательные команды

```bash
git show <commit>          # содержимое конкретного коммита
git blame <file>            # кто и в каком коммите менял каждую строку
git log --follow <file>     # история файла, включая переименования
git stash                   # временно отложить незакоммиченные изменения
git stash pop                # вернуть отложенные изменения обратно
```

`git stash` полезен, когда нужно быстро переключиться на другую ветку
(например, чтобы исправить баг в проде), а текущие изменения ещё не готовы
к коммиту.
