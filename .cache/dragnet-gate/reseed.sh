#!/bin/bash
# Re-pin the byte-budget witnesses, then refreeze.  Run after ANY corpus change.
set -eu
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
R="/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security"
"$G/sync.sh" >/dev/null
docker rm -f dragnet-reseed >/dev/null 2>&1 || true
docker run -d --name dragnet-reseed --cpus 6 --memory 8g dragnet-restitch:local sleep 7200 >/dev/null
docker cp "$G/task/tests" dragnet-reseed:/tests >/dev/null
docker cp "$G/reseed.py" dragnet-reseed:/rs.py >/dev/null
docker exec dragnet-reseed python3 /rs.py | tee "$G/reseed.out"
python3 - <<'PY'
import re
G = "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
p = "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security/task/tests/_dragnet_forge.py"
s = open(p).read()
for line in open(G + "/reseed.out"):
    parts = line.split()
    if len(parts) != 3 or parts[2] == "NONE":
        continue
    slot, _want, seed = parts
    pat = re.compile(r'("%s": \()(\d+)(, shape\()' % re.escape(slot))
    s, n = pat.subn(lambda m: m.group(1) + seed + m.group(3), s, count=1)
    print("pinned %-16s -> %s" % (slot, seed) if n else "MISS %s" % slot)
open(p, "w").write(s)
PY
"$G/refreeze.sh"
docker rm -f dragnet-reseed >/dev/null 2>&1 || true
