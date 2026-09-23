#!/usr/bin/env bash
# Проверяет решение упражнения 02_branch_and_merge.
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

check "текущая ветка — main" \
  "[ \"\$(git branch --show-current)\" = \"main\" ]"

check "calculator.py содержит subtract()" \
  "grep -q 'def subtract' calculator.py"

check "calculator.py содержит add() (не потерялось при мерже)" \
  "grep -q 'def add' calculator.py"

check "в истории main минимум 2 коммита" \
  "[ \"\$(git rev-list --count main)\" -ge 2 ]"

check "merge был fast-forward (нет merge-коммитов с двумя родителями)" \
  "[ -z \"\$(git rev-list --merges main)\" ]"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
