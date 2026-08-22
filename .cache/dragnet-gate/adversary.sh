#!/bin/bash
set -u
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
case_run () {
  local label="$1"; local script="$2"
  local NAME="dragnet-adv-$$-$RANDOM"
  docker rm -f "$NAME" >/dev/null 2>&1
  docker run -d --name "$NAME" --cpus 2 --memory 4g dragnet-restitch:local sleep 1800 >/dev/null
  docker cp "$G/task/tests" "$NAME":/tests >/dev/null
  docker cp "$G/task/solution" "$NAME":/solution >/dev/null
  docker exec "$NAME" bash -c "$script" >/dev/null 2>&1
  docker exec "$NAME" bash /tests/test.sh >/dev/null 2>&1
  local r; r=$(docker exec "$NAME" cat /logs/verifier/reward.txt 2>/dev/null)
  local n; n=$(docker exec "$NAME" sh -c 'tail -3 /logs/verifier/test-stdout.txt 2>/dev/null | grep -oE "[0-9]+ failed|[0-9]+ passed" | tr "\n" " "')
  printf '%-60s -> reward %s  (%s)\n' "$label" "${r:-?}" "${n:-?}"
  docker rm -f "$NAME" >/dev/null
}
case_run "stub program that does nothing" 'echo "def restitch(p): pass" > /app/dragnet_restitch.py'
case_run "correct tool, reward file pre-written to 1" '
  mkdir -p /logs/verifier && echo 1 > /logs/verifier/reward.txt && chmod 0444 /logs/verifier/reward.txt
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py'
case_run "correct tool but the live dragnet never restitched" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py'
case_run "live dragnet replaced by a symlink to a correct copy" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  cp -a /app/data/dragnet /app/real && python3 /app/dragnet_restitch.py /app/real
  rm -rf /app/data/dragnet && ln -s /app/real /app/data/dragnet'
case_run "scratch directory left behind in the live dragnet" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet && mkdir -p /app/data/dragnet/scratch'
case_run "charter edited during the run" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet && echo x >> /app/data/DRAGNET_CHARTER.md'
case_run "tool that peeks at the sealed overlay" '
  printf "import os\ndef restitch(t):\n    open(\"/tests/test_outputs.py\").read()\n" > /app/dragnet_restitch.py'
case_run "report pretty-printed instead of canonical" '
  sed "s/separators=(\",\", \":\")/separators=(\", \", \": \")/" /solution/dragnet_restitch.py > /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet'
case_run "supplied plumbing edited by the agent" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  chmod 0644 /app/dragnet_io.py && echo "# tweak" >> /app/dragnet_io.py
  python3 /app/dragnet_restitch.py /app/data/dragnet'
case_run "restore the spare and stop, never restitching" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  rm -rf /app/data/dragnet && tar -C /app/data -xf /app/data/dragnet.spare.tar'
case_run "restitch, then restore the spare over the result" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet
  rm -rf /app/data/dragnet && tar -C /app/data -xf /app/data/dragnet.spare.tar'
case_run "correct restitch but the spare unpacked inside the dragnet" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet
  mkdir -p /app/data/dragnet/backup && tar -C /app/data/dragnet/backup -xf /app/data/dragnet.spare.tar'
echo "--- these two MUST be reward 1 ---"
case_run "correct restitch, spare deleted afterwards" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet && rm -f /app/data/dragnet.spare.tar'
case_run "correct restitch after two restore-and-redo cycles" '
  cp /solution/dragnet_restitch.py /app/dragnet_restitch.py
  for i in 1 2; do python3 /app/dragnet_restitch.py /app/data/dragnet
    rm -rf /app/data/dragnet && tar -C /app/data -xf /app/data/dragnet.spare.tar; done
  python3 /app/dragnet_restitch.py /app/data/dragnet'
case_run "tool that imports the plumbing with a bare import" '
  printf "import dragnet_io\n" > /tmp/head.py
  sed "s/^import dragnet_io$//" /solution/dragnet_restitch.py >> /tmp/head.py
  cp /tmp/head.py /app/dragnet_restitch.py
  python3 /app/dragnet_restitch.py /app/data/dragnet'
