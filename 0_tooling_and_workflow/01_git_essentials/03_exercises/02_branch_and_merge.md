# Упражнение 2. Ветка и merge

Теория: [02_branching_merging.md](../01_theory/02_branching_merging.md).

## Подготовка

Репозиторий с одним коммитом:

```bash
mkdir -p ~/git-practice/ex02
cd ~/git-practice/ex02
git init -b main

cat > calculator.py <<'EOF'
def add(a, b):
    return a + b
EOF

git add calculator.py
git commit -m "feat: add calculator with add()"
```

## Задание

1. Создайте ветку `feature/subtract` и переключитесь на неё.
2. Допишите в конец `calculator.py` (в редакторе или через `cat >>`)
   функцию, отделив её двумя пустыми строками:
   ```python
   def subtract(a, b):
       return a - b
   ```
3. Закоммитьте изменение в ветке `feature/subtract`.
4. Вернитесь на `main` и слейте в неё `feature/subtract`.

## Проверь себя

```bash
git branch --show-current
```

```
main
```

```bash
git log --oneline --graph --all
```

```
* 23699c7 feat: add subtract()
* 0fc9325 feat: add calculator with add()
```

Хеши будут другими. Главное — история **линейная**, без `|\` и без
merge-коммита: это fast-forward. На `main` не было своих новых коммитов,
поэтому Git просто передвинул указатель вперёд.

```bash
cat calculator.py
```

В файле обе функции — `add` и `subtract`.

## Подсказки

- `git switch -c <имя>` создаёт ветку и сразу переключается на неё.
- Сообщение `git merge` со словом `Fast-forward` — признак, что всё
  сделано правильно.

Решение: [../04_exercises_answers/02_branch_and_merge.md](../04_exercises_answers/02_branch_and_merge.md).
