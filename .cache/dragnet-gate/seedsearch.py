"""Find seeds whose packing lands a segment exactly on the byte budget."""
import os, shutil, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_forge as forge, _dragnet_engine as engine
spec = forge.PLANS[os.environ["SLOT"]][1]
BUDGET = engine.SEGMENT_BYTE_BUDGET
lo, hi = int(sys.argv[1]), int(sys.argv[2])
hits = 0
for seed in range(lo, hi):
    work = tempfile.mkdtemp(prefix="seed-")
    try:
        t = os.path.join(work, "d")
        forge.write_plan(t, forge.build_plan(seed, spec))
        engine.restitch(t)
        seg = os.path.join(t, "segments")
        sizes = [os.path.getsize(os.path.join(seg, n)) for n in sorted(os.listdir(seg))]
        if BUDGET in sizes:
            print("HIT seed=%d sizes=%s" % (seed, sizes), flush=True)
            hits += 1
            if hits >= 4:
                break
    except Exception:
        pass
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("done hits=%d" % hits)
