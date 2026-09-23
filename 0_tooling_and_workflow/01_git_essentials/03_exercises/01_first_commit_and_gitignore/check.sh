#!/usr/bin/env bash
# Проверяет решение упражнения 01_first_commit_and_gitignore.
# Запуск: bash check.sh (из папки упражнения, ПОСЛЕ bash setup.sh и работы в sandbox/)
set -uo pipefail
cd "$(dirname "$0")/sandbox" 2>/dev/null || {
  echo "FAIL: папка sandbox не найдена. Сначала выполните: bash setup.sh"
  exit 1
}

PASS=0
FAIL=0

check() {
  local desc="$1"
  local cond="$2"
  if eval "$cond"; then
    echo "PASS: $desc"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $desc"
    FAIL=$((FAIL + 1))
  fi
}

check "sandbox — git-репозиторий" \
  "git rev-parse --is-inside-work-tree >/dev/null 2>&1"

check ".gitignore существует и игнорирует *.log" \
  "[ -f .gitignore ] && grep -qE '(^|/)\*\.log' .gitignore"

check ".gitignore игнорирует __pycache__/" \
  "[ -f .gitignore ] && grep -q '__pycache__' .gitignore"

check "secret.log НЕ отслеживается git'ом" \
  "! git ls-files --error-unmatch secret.log >/dev/null 2>&1"

check "__pycache__/ НЕ отслеживается git'ом" \
  "[ -z \"\$(git ls-files __pycache__)\" ]"

check "app.py отслеживается git'ом" \
  "git ls-files --error-unmatch app.py >/dev/null 2>&1"

check ".gitignore отслеживается git'ом" \
  "git ls-files --error-unmatch .gitignore >/dev/null 2>&1"

check "есть ровно один коммит" \
  "[ \"\$(git rev-list --count HEAD 2>/dev/null)\" = \"1\" ]"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
