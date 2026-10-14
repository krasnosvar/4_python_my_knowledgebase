# Решение: упражнение 1. Первый коммит и .gitignore

Условие: [../03_exercises/01_first_commit_and_gitignore.md](../03_exercises/01_first_commit_and_gitignore.md).

```bash
cd ~/git-practice/ex01
git init -b main
git status
```

```
Untracked files:
	__pycache__/
	app.py
	secret.log
```

Git предлагает добавить всё, включая мусор. Создаём `.gitignore`:

```bash
printf '*.log\n__pycache__/\n' > .gitignore
git status
```

```
Untracked files:
	.gitignore
	app.py
```

`secret.log` и `__pycache__/` пропали из списка. Коммитим только нужное:

```bash
git add app.py .gitignore
git commit -m "chore: initial project setup"
```

```
[main (root-commit) fbffe91] chore: initial project setup
 2 files changed, 7 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 app.py
```

## Почему так

`.gitignore` создан **до** первого коммита, поэтому мусорные файлы ни разу
не попали под отслеживание. Если бы их уже закоммитили раньше,
`.gitignore` не помог бы — пришлось бы убрать их из индекса через
`git rm --cached` (см. теорию).

`git add .` здесь тоже сработал бы — `.gitignore` отфильтровал бы мусор.
Но явное перечисление файлов — хорошая привычка: в коммит не попадёт
ничего случайного.
