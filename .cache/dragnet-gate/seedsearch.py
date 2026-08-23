"""Seeds that witness BOTH byte-budget edges: a segment on it, and a cut one over."""
import os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig, _dragnet_forge as forge, _dragnet_engine as engine
SLOT = os.environ["SLOT"]
NEED_OVER = os.environ.get("OVER", "1") == "1"
BUDGET = engine.SEGMENT_BYTE_BUDGET
lo, hi = int(sys.argv[1]), int(sys.argv[2])
_seed0, spec = forge.PLANS[SLOT]

def tree_at(budget, work):
    engine.SEGMENT_BYTE_BUDGET = budget
    try:
        t = rig.stage_crashed(SLOT, work)
        engine.restitch(t)
        seg = os.path.join(t, "segments")
        sizes = [os.path.getsize(os.path.join(seg, n)) for n in sorted(os.listdir(seg))]
        d = rig.tree_digest(t)
        shutil.rmtree(t, ignore_errors=True)
        return sizes, d
    finally:
        engine.SEGMENT_BYTE_BUDGET = BUDGET

hits = 0
for seed in range(lo, hi):
    forge.PLANS[SLOT] = (seed, spec)
    rig._CACHE.clear()
    work = tempfile.mkdtemp(prefix="seed-")
    try:
        sizes, base = tree_at(BUDGET, work)
        if BUDGET not in sizes:
            continue
        if NEED_OVER:
            rig._CACHE.clear()
            _s2, over = tree_at(BUDGET + 1, work)
            if over == base:
                continue
        print("HIT seed=%d sizes=%s" % (seed, sizes), flush=True)
        hits += 1
        if hits >= 2:
            break
    except Exception:
        pass
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("done hits=%d" % hits)
