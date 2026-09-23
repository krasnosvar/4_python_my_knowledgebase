#!/usr/bin/env bash
# Готовит стартовое состояние для упражнения 04_amend_commit_safely.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

cat > parser.py <<'EOF'
def parse_line(line: str) -> str:
    return line.strip()
EOF
git add parser.py
git commit -q -m "chore: initial parser"

# "Плохой" последний коммит: невнятное сообщение и забытый файл.
cat > parser.py <<'EOF'
def parse_line(line: str) -> str:
    if not line:
        raise ValueError("empty line")
    return line.strip()
EOF
git add parser.py
git commit -q -m "fix bug"

cat > parser_test_notes.py <<'EOF'
# заметки: parse_line теперь бросает ValueError на пустой строке
EOF
# Файл создан, но забыт: он НЕ добавлен в staging и не закоммичен.

echo "Sandbox готов: $(pwd)"
echo
git log --oneline
echo
echo "Обратите внимание: parser_test_notes.py создан, но не отслеживается git'ом:"
git status --short
