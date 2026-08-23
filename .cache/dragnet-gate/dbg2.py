import json, os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig, _dragnet_engine as engine
slot = "sweep-a"
work = tempfile.mkdtemp()
try:
    t = rig.stage_crashed(slot, work)
    raw = {}
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
                if isinstance(o, dict) and str(o.get("fid", "")).startswith("f-5"):
                    raw[o["fid"]] = (sub, name, n, o.get("bytes"), o.get("pkts"),
                                     o.get("seq"), o.get("op"), o.get("label"))
    print("planted witnesses found in the crashed store:")
    for k in sorted(raw):
        print("  ", k, raw[k])
    engine.restitch(t)
    rep = json.load(open(os.path.join(t, "restitch_report.json")))
    print("refused_duplicate_id", rep["refused_duplicate_id"], "malformed", rep["refused_malformed"])
    ref = os.path.join(t, "refused")
    if os.path.isdir(ref):
        for name in sorted(os.listdir(ref)):
            for line in open(os.path.join(ref, name)):
                row = json.loads(line)
                if "f-5" in row["text"]:
                    print("  REFUSED", row["cause"], row["source"], row["text"][:90])
    seg = os.path.join(t, "segments")
    kept = [json.loads(l)["fid"] for n in sorted(os.listdir(seg))
            for l in open(os.path.join(seg, n))]
    print("witnesses settled:", sorted(f for f in kept if f.startswith("f-5")))
finally:
    shutil.rmtree(work, ignore_errors=True)
