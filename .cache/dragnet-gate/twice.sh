#!/bin/bash
# the verifier must be re-runnable: three graded passes in one container
set -u
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
NAME="dragnet-twice-$$"
docker rm -f "$NAME" >/dev/null 2>&1
docker run -d --name "$NAME" --cpus 2 --memory 4g dragnet-restitch:local sleep 3600 >/dev/null
docker cp "$G/task/tests" "$NAME":/tests >/dev/null
docker cp "$G/task/solution" "$NAME":/solution >/dev/null
docker exec "$NAME" bash /solution/solve.sh >/dev/null 2>&1
for pass in 1 2 3; do
  START=$(date +%s)
  docker exec "$NAME" bash /tests/test.sh 2>&1 | grep -E "passed|failed" | tail -1
  echo "pass $pass reward $(docker exec "$NAME" cat /logs/verifier/reward.txt) wall $(( $(date +%s) - START ))s"
done
docker rm -f "$NAME" >/dev/null
