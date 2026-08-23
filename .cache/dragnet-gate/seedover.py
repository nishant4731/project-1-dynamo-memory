"""A held-out seed where raising the byte budget by one changes the restitch."""
import os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig, _dragnet_forge as forge, _dragnet_engine as engine
SLOT = os.environ["SLOT"]
BUDGET = engine.SEGMENT_BYTE_BUDGET
lo, hi = int(sys.argv[1]), int(sys.argv[2])
_s, spec = forge.PLANS[SLOT]

def tree_at(budget):
    engine.SEGMENT_BYTE_BUDGET = budget
    work = tempfile.mkdtemp(prefix="ov-")
    try:
        t = rig.stage_crashed(SLOT, work)
        engine.restitch(t)
        return rig.tree_digest(t)
    finally:
        engine.SEGMENT_BYTE_BUDGET = BUDGET
        shutil.rmtree(work, ignore_errors=True)

hits = 0
for seed in range(lo, hi):
    forge.PLANS[SLOT] = (seed, spec)
    try:
        rig._CACHE.clear(); base = tree_at(BUDGET)
        rig._CACHE.clear(); over = tree_at(BUDGET + 1)
        if base != over:
            print("HIT seed=%d" % seed, flush=True)
            hits += 1
            if hits >= 2:
                break
    except Exception:
        pass
print("done hits=%d" % hits)
