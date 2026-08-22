#!/bin/bash
# manual Harbor fallback: oracle (solve then verify) or nop (verify only)
set -u
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
MODE="$1"
NAME="dragnet-$MODE-$$"
docker rm -f "$NAME" >/dev/null 2>&1
docker run -d --name "$NAME" --cpus 2 --memory 4g dragnet-restitch:local sleep 3600 >/dev/null
docker cp "$G/task/tests" "$NAME":/tests >/dev/null
docker cp "$G/task/solution" "$NAME":/solution >/dev/null
if [ "$MODE" = "oracle" ]; then
  docker exec "$NAME" bash /solution/solve.sh
  echo "--- solve exit $? ---"
fi
START=$(date +%s)
docker exec "$NAME" bash /tests/test.sh 2>&1 | tail -45
echo "--- verifier wall $(( $(date +%s) - START ))s ---"
echo -n "reward: "; docker exec "$NAME" cat /logs/verifier/reward.txt
docker rm -f "$NAME" >/dev/null
