# Решение: 02_branch_and_merge

```bash
git switch -c feature/subtract

cat >> calculator.py <<'EOF'


def subtract(a: int, b: int) -> int:
    return a - b
EOF

git add calculator.py
git commit -m "feat: add subtract()"

git switch main
git merge feature/subtract    # fast-forward: main не имел своих новых коммитов
```

`git log --oneline --graph --all` после этого покажет линейную историю без
merge-коммита — это и есть fast-forward.
