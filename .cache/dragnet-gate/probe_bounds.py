import json, os, sys, shutil, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig
want = {"bytes1": 0, "pkts1": 0, "seq0": 0, "digit_label": 0, "amend_seq0": 0}
for slot in (rig.LIVE_ID,) + rig.HELD_OUT:
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
                for line in open(p, errors="replace"):
                    try:
                        o = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(o, dict):
                        continue
                    if o.get("op") in ("amend", "retract"):
                        want["amend_seq0"] += o.get("seq") == 0
                        continue
                    want["bytes1"] += o.get("bytes") == 1
                    want["pkts1"] += o.get("pkts") == 1
                    want["seq0"] += o.get("seq") == 0
                    lab = o.get("label")
                    if isinstance(lab, str) and any(c in lab for c in "23456789"):
                        want["digit_label"] += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("sifted lines carrying each edge value, across the whole graded corpus:")
for k, v in want.items():
    print("  %-12s %d" % (k, v))
