#!/usr/bin/env bash
# Проверяет решение упражнения 03_resolve_merge_conflict.
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

check "нет незавершённого merge (MERGE_HEAD отсутствует)" \
  "[ ! -f .git/MERGE_HEAD ]"

check "в settings.py нет конфликтных маркеров" \
  "! grep -qE '^(<<<<<<<|=======|>>>>>>>)' settings.py"

check "DEBUG = False" \
  "grep -qE '^DEBUG = False' settings.py"

check "MAX_CONNECTIONS = 50" \
  "grep -qE '^MAX_CONNECTIONS = 50' settings.py"

check "на main есть merge-коммит с двумя родителями" \
  "[ -n \"\$(git rev-list --merges main)\" ]"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
