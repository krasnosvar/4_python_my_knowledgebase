#!/usr/bin/env bash
# Проверяет решение упражнения 04_amend_commit_safely.
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

check "коммитов ровно 2 (файл вошёл в существующий коммит, не создал новый)" \
  "[ \"\$(git rev-list --count HEAD)\" = \"2\" ]"

check "сообщение последнего коммита изменено (не 'fix bug')" \
  "[ \"\$(git log -1 --pretty=%s)\" != \"fix bug\" ]"

check "parser_test_notes.py отслеживается git'ом" \
  "git ls-files --error-unmatch parser_test_notes.py >/dev/null 2>&1"

check "parser_test_notes.py входит именно в последний коммит" \
  "git show --stat -1 --pretty=format: | grep -q parser_test_notes.py"

check "рабочая папка чистая (нет untracked/незакоммиченных файлов)" \
  "[ -z \"\$(git status --porcelain)\" ]"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
