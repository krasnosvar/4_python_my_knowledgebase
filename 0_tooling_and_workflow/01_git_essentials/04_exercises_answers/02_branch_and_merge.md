# Решение: упражнение 2. Ветка и merge

Условие: [../03_exercises/02_branch_and_merge.md](../03_exercises/02_branch_and_merge.md).

```bash
cd ~/git-practice/ex02
git switch -c feature/subtract

cat >> calculator.py <<'EOF'


def subtract(a, b):
    return a - b
EOF

git add calculator.py
git commit -m "feat: add subtract()"
```

```
Switched to a new branch 'feature/subtract'
[feature/subtract 23699c7] feat: add subtract()
 1 file changed, 4 insertions(+)
```

```bash
git switch main
git merge feature/subtract
```

```
Switched to branch 'main'
Updating 0fc9325..23699c7
Fast-forward
 calculator.py | 4 ++++
 1 file changed, 4 insertions(+)
```

## Почему так

С момента создания ветки на `main` не появилось новых коммитов, поэтому
Git сделал **fast-forward**: просто передвинул `main` на последний коммит
ветки. Merge-коммит не нужен, история осталась линейной.

После слияния ветку можно удалить: `git branch -d feature/subtract`.
