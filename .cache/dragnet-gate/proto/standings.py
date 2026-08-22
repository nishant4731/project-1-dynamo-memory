"""Is a 'moments stood' column strictly more sensitive than the reach columns?"""
import random, sys
T = "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security/task/tests"
sys.path.insert(0, T)
import _dragnet_forge as forge, _dragnet_engine as engine
W = engine.RELAY_WINDOW

def edges_for(seed, spec):
    rng = random.Random(seed)
    raw = forge._contacts(rng, spec, forge._hosts(spec["hosts"]))
    out = [{"fid": "f-%05d" % i, "src": s, "dst": d, "first": f, "last": l}
           for i, (s, d, f, l) in enumerate(raw)]
    out.sort(key=lambda e: (e["first"], e["fid"]))
    return out

def frontier(origin, edges, window, lo_incl=True, hi_incl=True, scalar=False):
    seat = {}
    for e in edges:
        if e["src"] == origin:
            ok = True
        else:
            held = seat.get(e["src"])
            ok = held is not None and any(
                ((a <= e["first"]) if lo_incl else (a < e["first"])) and
                ((e["first"] <= a + window) if hi_incl else (e["first"] < a + window))
                for a in held)
        if not ok:
            continue
        if scalar:
            t = e["last"]
            seat[e["dst"]] = {min(min(seat.get(e["dst"], {t})), t)}
        else:
            seat.setdefault(e["dst"], set()).add(e["last"])
    return seat

def rows(edges, **kw):
    out = []
    for o in sorted({e["src"] for e in edges}):
        f = frontier(o, edges, kw.pop("window", W), **kw) if kw else frontier(o, edges, W)
        if not f:
            continue
        arrival = {h: min(p) for h, p in f.items()}
        horizon = max(arrival.values())
        far = min(h for h in arrival if arrival[h] == horizon)
        standings = sum(len(p) for p in f.values())
        out.append((o, len(arrival), horizon, far, standings))
    return out

VARIANTS = {
  "scalar arrivals":        dict(scalar=True),
  "window +1":              dict(window=W + 1),
  "window -1":              dict(window=W - 1),
  "upper edge exclusive":   dict(hi_incl=False),
  "lower edge exclusive":   dict(lo_incl=False),
}

slots = ["dragnet-live"] + sorted(s for s in forge.PLANS if s.startswith("held-"))
print("%-24s %-26s %-26s" % ("variant", "caught by reach columns", "caught by + standings"))
for name, kw in VARIANTS.items():
    old_c = new_c = 0
    live_old = live_new = "blind"
    for slot in slots:
        seed, spec = forge.PLANS[slot]
        e = edges_for(seed, spec)
        good = rows(e)
        bad = rows(e, **dict(kw))
        old_diff = [r[:4] for r in good] != [r[:4] for r in bad]
        new_diff = good != bad
        if slot == "dragnet-live":
            live_old = "VISIBLE" if old_diff else "blind"
            live_new = "VISIBLE" if new_diff else "blind"
        else:
            old_c += old_diff; new_c += new_diff
    print("%-24s %2d/13 (live %-7s)     %2d/13 (live %-7s)"
          % (name, old_c, live_old, new_c, live_new))
