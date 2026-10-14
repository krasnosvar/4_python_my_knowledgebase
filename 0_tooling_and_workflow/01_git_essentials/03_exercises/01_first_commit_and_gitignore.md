# Упражнение 1. Первый коммит и .gitignore

Теория: [01_basic_workflow.md](../01_theory/01_basic_workflow.md).

## Подготовка

Создайте папку проекта — пока это **не** git-репозиторий:

```bash
mkdir -p ~/git-practice/ex01/__pycache__
cd ~/git-practice/ex01

cat > app.py <<'EOF'
def main():
    print("hello, git")


main()
EOF

echo "cached bytecode junk" > __pycache__/app.cpython-312.pyc
echo "DEBUG=1" > secret.log
```

В папке теперь:

- `app.py` — исходник, должен попасть в репозиторий;
- `secret.log` — лог, в репозиторий попадать не должен;
- `__pycache__/` — байткод-мусор, в репозиторий попадать не должен.

## Задание

1. Превратите папку в git-репозиторий с веткой `main`.
2. Посмотрите `git status` — Git предлагает добавить все три пункта.
3. Создайте `.gitignore`, который исключает `*.log` и `__pycache__/`.
4. Снова посмотрите `git status` — `secret.log` и `__pycache__/` должны
   исчезнуть из списка.
5. Одним коммитом закоммитьте **только** `app.py` и `.gitignore`, с
   осмысленным сообщением (например `chore: initial project setup`).

## Проверь себя

```bash
git log --oneline
```

Ровно одна строка — ваш коммит.

```bash
git ls-files
```

```
.gitignore
app.py
```

Только эти два файла отслеживаются Git'ом.

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

`secret.log` и `__pycache__/` на диске есть, но Git их не показывает —
`.gitignore` работает.

## Подсказки

- В `.gitignore` — один паттерн на строку; папки обычно пишут со `/` на
  конце.
- `.gitignore` не действует на файлы, которые уже отслеживаются. Здесь их
  ещё ни разу не коммитили, поэтому это не проблема.

Решение: [../04_exercises_answers/01_first_commit_and_gitignore.md](../04_exercises_answers/01_first_commit_and_gitignore.md).
