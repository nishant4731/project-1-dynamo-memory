"""Re-search every measure-zero byte-budget witness and print the seeds to pin.

Any change to the corpus moves every record, so these have to be found again
rather than kept.  Each slot carries a different edge of the same bound.
"""
import os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig, _dragnet_forge as forge, _dragnet_engine as engine
BUDGET = engine.SEGMENT_BYTE_BUDGET

def measure(slot, budget):
    engine.SEGMENT_BYTE_BUDGET = budget
    work = tempfile.mkdtemp(prefix="rs-")
    try:
        t = rig.stage_crashed(slot, work)
        engine.restitch(t)
        seg = os.path.join(t, "segments")
        sizes = [os.path.getsize(os.path.join(seg, n)) for n in sorted(os.listdir(seg))]
        return sizes, rig.tree_digest(t)
    finally:
        engine.SEGMENT_BYTE_BUDGET = BUDGET
        shutil.rmtree(work, ignore_errors=True)

def holds(slot, want):
    rig._CACHE.clear()
    sizes, base = measure(slot, BUDGET)
    if want == "first" and not (sizes and sizes[0] == BUDGET):
        return False
    if want == "later" and BUDGET not in sizes[1:]:
        return False
    if want in ("any", "both") and BUDGET not in sizes:
        return False
    if want in ("over", "both"):
        rig._CACHE.clear()
        _s, over = measure(slot, BUDGET + 1)
        if over == base:
            return False
    return True

WANTED = [("sweep-g", "both")]

for slot, want in WANTED:
    seed0, spec = forge.PLANS[slot]
    found = None
    for seed in range(seed0, seed0 + 120000):
        forge.PLANS[slot] = (seed, spec)
        try:
            if holds(slot, want):
                found = seed
                break
        except Exception:
            pass
    forge.PLANS[slot] = (found if found else seed0, spec)
    print("%s %s %s" % (slot, want, found if found else "NONE"), flush=True)
