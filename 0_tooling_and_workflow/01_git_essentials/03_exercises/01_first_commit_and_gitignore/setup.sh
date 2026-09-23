#!/usr/bin/env bash
# Готовит стартовое состояние для упражнения 01_first_commit_and_gitignore.
# Создаёт ./sandbox — обычную (пока НЕ git) папку с файлами проекта.
set -euo pipefail
cd "$(dirname "$0")"

rm -rf sandbox
mkdir -p sandbox/__pycache__
cd sandbox

cat > app.py <<'EOF'
def main() -> None:
    print("hello, git")


if __name__ == "__main__":
    main()
EOF

# "Мусорные" файлы, которые не должны попасть в репозиторий
echo "some cached bytecode junk" > __pycache__/app.cpython-312.pyc
echo "DEBUG=1" > secret.log

echo "Sandbox готов: $(pwd)"
echo "Это ПОКА НЕ git-репозиторий — это часть задания."
