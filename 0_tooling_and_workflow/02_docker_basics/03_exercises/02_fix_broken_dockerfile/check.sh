#!/usr/bin/env bash
# Проверяет решение упражнения 02_fix_broken_dockerfile.
# Требует установленный и запущенный Docker.
set -uo pipefail
cd "$(dirname "$0")"

IMAGE="kb-exercise-02-fix-broken-dockerfile"
CONTAINER="kb-exercise-02-fix-broken-dockerfile-run"
HOST_PORT=15000

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

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1
  docker rmi "$IMAGE" >/dev/null 2>&1
}
trap cleanup EXIT

check "Dockerfile больше не ссылается на несуществующий app.py" \
  "! grep -q 'app\.py' Dockerfile"

check "EXPOSE указывает верный порт 5000" \
  "grep -qE '^EXPOSE 5000' Dockerfile"

if docker build -t "$IMAGE" . >/tmp/kb-ex02-build.log 2>&1; then
  echo "PASS: docker build завершился успешно"
  PASS=$((PASS + 1))
else
  echo "FAIL: docker build завершился с ошибкой (см. /tmp/kb-ex02-build.log)"
  FAIL=$((FAIL + 1))
  echo; echo "Итого: $PASS PASS, $FAIL FAIL"
  exit 1
fi

docker run --rm -d -p "${HOST_PORT}:5000" --name "$CONTAINER" "$IMAGE" >/dev/null 2>&1
sleep 2

RESPONSE=$(curl -s --max-time 3 "http://localhost:${HOST_PORT}/" || true)
check "контейнер отвечает на порту 5000 ожидаемым текстом" \
  "echo '$RESPONSE' | grep -q 'hello from broken-dockerfile exercise'"

echo
echo "Итого: $PASS PASS, $FAIL FAIL"
[ "$FAIL" -eq 0 ]
