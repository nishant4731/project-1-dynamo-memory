"""QC's method: mutate the SUBMITTED SOLUTION one token at a time and grade it."""
import os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig

SOLUTION = open("/solution/dragnet_restitch.py").read()
GRADED = (rig.LIVE_ID,) + rig.HELD_OUT

def mutations(text):
    out = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        subs = []
        # comparison operators, both directions
        for a, b in (("<=", "<"), (">=", ">"), (" < ", " <= "), (" > ", " >= "),
                     ("==", "!="), (" is None", " is not None")):
            if a in line:
                subs.append((a, b))
        # min/max swaps
        for a, b in (("min(", "max("), ("max(", "min(")):
            if a in line:
                subs.append((a, b))
        # small integer constants
        for m in re.finditer(r"(?<![\w.])(\d+)(?![\w.])", line):
            v = int(m.group(1))
            if 0 <= v <= 100000:
                subs.append((m.group(0), str(v + 1)))
        for a, b in subs:
            new = lines[:]
            new[i] = line.replace(a, b, 1)
            body = "\n".join(new)
            if body != text:
                out.append(("L%d:%s->%s" % (i + 1, a.strip(), b.strip()), body))
    return out

def grade(text):
    work = tempfile.mkdtemp(prefix="qcs-")
    try:
        prog = os.path.join(work, "cand.py")
        open(prog, "w").write(text)
        shutil.copy(rig.HELPER, os.path.join(work, "dragnet_io.py"))
        digests = []
        for slot in GRADED:
            target = rig.stage_crashed(slot, work)
            try:
                r = subprocess.run([sys.executable, "-s", "-E", prog, target],
                                   capture_output=True, timeout=120)
                digests.append(rig.tree_digest(target) if r.returncode == 0 else None)
            except Exception:
                digests.append(None)
            shutil.rmtree(target, ignore_errors=True)
        return digests
    finally:
        shutil.rmtree(work, ignore_errors=True)

good = grade(SOLUTION)
muts = mutations(SOLUTION)
print("mutants: %d" % len(muts), flush=True)
survivors = []
for n, (name, body) in enumerate(muts):
    try:
        compile(body, "m", "exec")
    except SyntaxError:
        continue
    got = grade(body)
    if got == good:
        survivors.append(name)
        print("SURVIVOR %s" % name, flush=True)
    if n % 40 == 0:
        print("  ...%d/%d, %d survivors" % (n, len(muts), len(survivors)), flush=True)
print("\nsurvivors: %d of %d" % (len(survivors), len(muts)))
for s in survivors:
    print("  ", s)
