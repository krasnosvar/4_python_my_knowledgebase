#!/usr/bin/env bash
# Готовит стартовое состояние для упражнения 05_restore_reset_revert.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

cat > report.py <<'EOF'
def build_report() -> str:
    return "report v1"
EOF
git add report.py
git commit -q -m "chore: initial report module"

cat > report.py <<'EOF'
def build_report() -> str:
    return "report v2"
EOF
git add report.py
git commit -q -m "feat: report v2"

# "Плохой" коммит, который представляет собой уже запушенную/публичную историю
# (в реальности здесь был бы git push, в упражнении это условность).
cat > report.py <<'EOF'
def build_report() -> str:
    return "BROKEN"
EOF
git add report.py
git commit -q -m "feat: report v3 (bug: broke report output)"

# Незакоммиченная правка в другом файле — её нужно будет отменить через restore.
cat > scratch.py <<'EOF'
ORIGINAL = "keep me"
EOF
git add scratch.py
git commit -q -m "chore: add scratch module"
echo "ORIGINAL = \"keep me\"" > scratch.py
echo "ACCIDENTAL_LINE = True" >> scratch.py

echo "Sandbox готов: $(pwd)"
echo
git log --oneline
echo
echo "git status:"
git status --short
