#!/bin/bash
# Regenerate, in the only order that is self-consistent:
#   live dragnet -> image -> format sheet -> image -> pins
set -eu
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
R="/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security"

fresh () {   # a regen container built from the CURRENT repo bytes
  "$G/sync.sh" >/dev/null
  docker rm -f dragnet-regen >/dev/null 2>&1 || true
  docker run -d --name dragnet-regen --cpus 4 --memory 6g dragnet-restitch:local sleep 3600 >/dev/null
  docker cp "$G/task/tests" dragnet-regen:/tests >/dev/null
  docker cp "$G/regen.py" dragnet-regen:/regen.py >/dev/null
  docker exec dragnet-regen mkdir -p /out
}

echo "1/3 live dragnet"
fresh
docker exec dragnet-regen python3 /regen.py live >/dev/null
rm -rf "$G/newlive"; docker cp dragnet-regen:/out/dragnet "$G/newlive" >/dev/null
rm -rf "$R/task/environment/data/dragnet"
cp -a "$G/newlive" "$R/task/environment/data/dragnet"
find "$R/task/environment/data/dragnet" -type f -exec chmod 0644 {} +
find "$R/task/environment/data/dragnet" -type d -exec chmod 0755 {} +

echo "2/3 format sheet"
fresh
docker exec dragnet-regen python3 /regen.py sheet > "$G/sheet.json"
python3 - <<'PY'
import json
G = "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
d = json.load(open(G + "/sheet.json"))
p = "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security/task/environment/data/DRAGNET_CHARTER.md"
s = open(p).read()
head = s[:s.index("## 12. Format sheet")]
open(p, "w").write(head + """## 12. Format sheet

These fragments pin the conventions and nothing else. They come from a dragnet
you do not have; reproducing them proves nothing about a restitch.

One line of `segments/%(seg)s`, the second record in that segment:

    %(record)s

The two rows of `CONTACT.tsv` that name that segment first, which is where the
offset column starts again:

    %(c0)s
    %(c1)s

Two rows of `REACH.tsv`, following its header row:

    %(r0)s
    %(r1)s

Two rows of `PIVOT.tsv`, following its header row:

    %(p0)s
    %(p1)s

One row of a file under `refused/`:

    %(refused)s
""" % {"seg": d["segment_name"], "record": d["record"],
       "c0": d["contact"][0], "c1": d["contact"][1],
       "r0": d["reach"][0], "r1": d["reach"][1],
       "p0": d["pivot"][0], "p1": d["pivot"][1], "refused": d["refused"]})
PY

echo "3/3 pins"
fresh
docker exec dragnet-regen python3 /regen.py pins > "$G/pins.json"
python3 - <<'PY'
import json
G = "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
R = "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security"
d = json.load(open(G + "/pins.json"))
assert set(d) == {"charter", "crashed_live", "dragnets", "fleet", "helper"}, set(d)
json.dump(d, open(R + "/task/tests/reference_pins.json", "w"), indent=2, sort_keys=True)
open(R + "/task/tests/reference_pins.json", "a").write("\n")
print("pins:", len(d["dragnets"]))
PY
"$G/sync.sh" >/dev/null
echo "refreeze complete"
