#!/usr/bin/env bash
# Готовит стартовое состояние для упражнения 02_branch_and_merge.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

cat > calculator.py <<'EOF'
def add(a: int, b: int) -> int:
    return a + b
EOF

git add calculator.py
git commit -q -m "feat: add calculator with add()"

echo "Sandbox готов: $(pwd)"
echo "git log:"
git log --oneline
