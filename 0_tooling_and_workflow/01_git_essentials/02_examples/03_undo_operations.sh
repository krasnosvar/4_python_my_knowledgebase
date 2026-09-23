#!/usr/bin/env bash
# Аннотированный проход по restore / reset / revert / commit --amend.
#
# Запуск:
#   bash 03_undo_operations.sh

set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir sandbox
cd sandbox

git init -q
git checkout -q -b main
git config user.name "KB Learner"
git config user.email "learner@example.com"

echo "=== Базовая история из трёх коммитов ==="
echo "print('start')" > main.py
git add main.py
git commit -m "chore: initial script"

echo "print('feature A')" >> main.py
git add main.py
git commit -m "feat: add feature A"

echo "DEBUG_PRINT = True  # забыли убрать" >> main.py
git add main.py
git commit -m "feat: add feature B (bug: leftover debug flag)"

git log --oneline

echo
echo "=== 1. git restore: отменить незакоммиченную правку ==="
echo "это изменение никогда не должно было тут оказаться" >> main.py
echo "--- до restore ---"; tail -n 2 main.py
git restore main.py
echo "--- после restore ---"; tail -n 2 main.py

echo
echo "=== 2. git restore --staged: убрать файл из staging area ==="
echo "TEMP = 1" > scratch.py
git add scratch.py
echo "staged перед restore:"; git status --short
git restore --staged scratch.py
echo "staged после restore --staged (файл всё ещё untracked на диске):"; git status --short
rm scratch.py

echo
echo "=== 3. git commit --amend: исправляем сообщение последнего коммита ==="
git commit --amend -m "fix: remove leftover debug flag from feature B"
git log --oneline

echo
echo "=== 4. git revert: безопасно отменить 'плохой' коммит, не трогая историю ==="
echo "Последний коммит (HEAD) всё ещё содержит забытый DEBUG_PRINT."
echo "Представим, что он уже запушен и виден коллегам — amend тут неуместен,"
echo "поэтому отменяем его новым коммитом через revert, а не переписываем историю:"
git revert --no-edit HEAD
echo
git log --oneline --graph
echo
echo "Обратите внимание: старые коммиты никуда не делись, просто добавился новый,"
echo "который отменяет изменения. Это то, что делает revert безопасным для истории,"
echo "которая уже могла быть запушена и подтянута кем-то ещё."

echo
echo "=== 5. git reset (только для ЛОКАЛЬНЫХ, ещё не запушенных коммитов) ==="
echo "console.log('oops, wrong repo')" > mistake.py
git add mistake.py
git commit -m "oops: wrong file in wrong repo"
echo "до reset:"; git log --oneline -n 3
git reset --soft HEAD~1   # откатываем коммит, изменения остаются в staging area
echo "после reset --soft (коммит исчез, изменения остались застейджены):"
git status --short
git restore --staged mistake.py
rm mistake.py
