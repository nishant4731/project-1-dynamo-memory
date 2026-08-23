"""A held-out seed whose FIRST segment lands exactly on the byte budget."""
import os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig, _dragnet_forge as forge, _dragnet_engine as engine
SLOT = os.environ["SLOT"]
BUDGET = engine.SEGMENT_BYTE_BUDGET
lo, hi = int(sys.argv[1]), int(sys.argv[2])
_s, spec = forge.PLANS[SLOT]
hits = 0
for seed in range(lo, hi):
    forge.PLANS[SLOT] = (seed, spec)
    rig._CACHE.clear()
    work = tempfile.mkdtemp(prefix="sf-")
    try:
        t = rig.stage_crashed(SLOT, work)
        engine.restitch(t)
        seg = os.path.join(t, "segments")
        names = sorted(os.listdir(seg))
        sizes = [os.path.getsize(os.path.join(seg, n)) for n in names]
        if BUDGET in sizes[1:]:
            print("HIT seed=%d sizes=%s" % (seed, sizes), flush=True)
            hits += 1
            if hits >= 2:
                break
    except Exception:
        pass
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("done hits=%d" % hits)
