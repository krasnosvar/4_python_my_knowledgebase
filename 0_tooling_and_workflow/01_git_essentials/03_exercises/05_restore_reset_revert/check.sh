#!/usr/bin/env bash
# Проверяет решение упражнения 05_restore_reset_revert.
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

check "scratch.py больше не содержит ACCIDENTAL_LINE" \
  "! grep -q ACCIDENTAL_LINE scratch.py"

check "scratch.py содержит исходную строку ORIGINAL" \
  "grep -q 'ORIGINAL = \"keep me\"' scratch.py"

check "draft.py существует на диске, но НЕ отслеживается git'ом (untracked)" \
  "[ -f draft.py ] && ! git ls-files --error-unmatch draft.py >/dev/null 2>&1"

check "report.py снова возвращает 'report v2' (эффект бага отменён)" \
  "grep -q 'report v2' report.py"

check "коммит про report v3 всё ещё есть в истории (история не переписана)" \
  "git log --oneline --all | grep -q 'report v3'"

check "в истории появился новый revert-коммит (минимум 5 коммитов)" \
  "[ \"\$(git rev-list --count HEAD)\" -ge 5 ]"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
