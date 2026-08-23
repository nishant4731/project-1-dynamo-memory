import json, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig
SOL = open("/solution/dragnet_restitch.py").read()
OLD = 'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:'
NEW = 'if obj["bytes"] <= 1 or obj["pkts"] < 1 or obj["seq"] < 0:'
assert SOL.count(OLD) == 1
slot = "held-broad"
for tag, text in (("reference", SOL), ("mutant", SOL.replace(OLD, NEW))):
    work = tempfile.mkdtemp()
    try:
        prog = os.path.join(work, "c.py"); open(prog, "w").write(text)
        shutil.copy(rig.HELPER, os.path.join(work, "dragnet_io.py"))
        t = rig.stage_crashed(slot, work)
        r = subprocess.run([sys.executable, "-s", "-E", prog, t],
                           capture_output=True, timeout=180)
        rep = json.load(open(os.path.join(t, "restitch_report.json")))
        print("%-10s rc=%d  flows_settled=%s lines_refused=%s refused_malformed=%s"
              % (tag, r.returncode, rep["flows_settled"], rep["lines_refused"],
                 rep["refused_malformed"]))
        if r.returncode:
            print(r.stderr.decode()[-400:])
    finally:
        shutil.rmtree(work, ignore_errors=True)
# and where do the bytes==1 lines actually live?
work = tempfile.mkdtemp()
try:
    t = rig.stage_crashed(slot, work)
    for sub in ("segments", "inbox"):
        d = os.path.join(t, sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if not os.path.isfile(p):
                continue
            for n, line in enumerate(open(p, errors="replace"), 1):
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if isinstance(o, dict) and o.get("bytes") == 1 and "op" not in o:
                    print("bytes==1 at %s/%s:%d fid=%s pkts=%s" % (sub, name, n, o.get("fid"), o.get("pkts")))
finally:
    shutil.rmtree(work, ignore_errors=True)
