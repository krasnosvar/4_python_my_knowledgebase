# Решение: 01_first_commit_and_gitignore

```bash
git init -q
git checkout -q -b main            # явно называем ветку main
git config user.name "..."          # если ещё не настроено глобально
git config user.email "..."

cat > .gitignore <<'EOF'
*.log
__pycache__/
EOF

git add app.py .gitignore
git status                           # secret.log и __pycache__/ не предлагаются
git commit -m "chore: initial project setup"
```

Ключевой момент: `.gitignore` создаётся и коммитится **до** того, как
`secret.log`/`__pycache__/` вообще попадут под отслеживание — поэтому
`git rm --cached` тут не требуется (в отличие от ситуации, когда мусорные
файлы уже закоммичены раньше).
