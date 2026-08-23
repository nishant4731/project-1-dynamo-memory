import os, shutil, subprocess, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig
SOL = open("/solution/dragnet_restitch.py").read()
GRADED = (rig.LIVE_ID,) + rig.HELD_OUT

def grade(text):
    work = tempfile.mkdtemp(prefix="c1-")
    try:
        prog = os.path.join(work, "cand.py"); open(prog, "w").write(text)
        shutil.copy(rig.HELPER, os.path.join(work, "dragnet_io.py"))
        out = []
        for slot in GRADED:
            t = rig.stage_crashed(slot, work)
            try:
                r = subprocess.run([sys.executable, "-s", "-E", prog, t],
                                   capture_output=True, timeout=180)
                out.append(rig.tree_digest(t) if r.returncode == 0 else "CRASH")
            except Exception:
                out.append("CRASH")
            shutil.rmtree(t, ignore_errors=True)
        return out
    finally:
        shutil.rmtree(work, ignore_errors=True)

CASES = [
 ("budget 3450 -> 3451", "SEGMENT_BYTE_BUDGET = 3450", "SEGMENT_BYTE_BUDGET = 3451"),
 ("capacity 13 -> 14", "SEGMENT_CAPACITY = 13", "SEGMENT_CAPACITY = 14"),
 ("label alphabet drops 2-9", r'LABEL_SHAPE = re.compile(r"\A[a-z][a-z0-9]*([/-][a-z0-9]+)*\Z")',
                              r'LABEL_SHAPE = re.compile(r"\A[a-z][a-z0-1]*([/-][a-z0-1]+)*\Z")'),
 ("bytes bound < -> <=", 'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
                          'if obj["bytes"] <= 1 or obj["pkts"] < 1 or obj["seq"] < 0:'),
 ("pkts bound < -> <=",  'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
                          'if obj["bytes"] < 1 or obj["pkts"] <= 1 or obj["seq"] < 0:'),
 ("seq bound < -> <=",   'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
                          'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] <= 0:'),
 ("amend seq bound",     'if not is_int(obj["seq"]) or obj["seq"] < 0:',
                          'if not is_int(obj["seq"]) or obj["seq"] <= 0:'),
 ("label limit 120->121", "LABEL_LIMIT = 120", "LABEL_LIMIT = 121"),
 ("port low 1 -> 2",     "PORT_LOW = 1", "PORT_LOW = 2"),
 ("port high -> 65534",  "PORT_HIGH = 65535", "PORT_HIGH = 65534"),
 ("refused stem keeps ext", '            stem = name.rsplit(".", 1)[0]',
                            '            stem = name.rsplit(".", 2)[0]'),
]
good = grade(SOL)
for name, old, new in CASES:
    if SOL.count(old) != 1:
        print("%-28s ANCHOR x%d" % (name, SOL.count(old))); continue
    got = grade(SOL.replace(old, new))
    killed = [s for s, a, b in zip(GRADED, good, got) if a != b]
    print("%-28s %s  (%d of %d dragnets)" %
          (name, "KILLED" if killed else "*** SURVIVES ***", len(killed), len(GRADED)))
