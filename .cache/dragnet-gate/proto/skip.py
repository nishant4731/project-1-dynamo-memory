"""Do band-skipping contacts make the (arrival, hops) frontier load-bearing?"""
import random, sys
T = "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security/task/tests"
sys.path.insert(0, T); sys.path.insert(0, "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate/proto")
import _dragnet_forge as forge
from hops import frontier, W

STEP, SPAN = forge.STEP, forge.SPAN

def edges_for(seed, spec, skips):
    rng = random.Random(seed)
    hosts = forge._hosts(spec["hosts"])
    raw = list(forge._contacts(rng, spec, hosts))
    edges = [{"fid": "f-%05d" % i, "src": s, "dst": d, "first": f, "last": l}
             for i, (s, d, f, l) in enumerate(raw)]
    # a contact that jumps a band: its source sits where a depth-d contact ended,
    # its destination where a depth-(d+2) contact begins, so it short-cuts a hop.
    by_dst = {}
    for e in edges:
        by_dst.setdefault(e["dst"], []).append(e)
    pool = sorted(edges, key=lambda e: (e["first"], e["fid"]))
    made = 0
    for anchor in pool:
        if made >= skips:
            break
        far = [e for e in pool if e["first"] > anchor["last"] + 2 * STEP]
        if not far:
            continue
        target = far[0]
        first = anchor["last"] + rng.randrange(1, W)
        edges.append({"fid": "s-%05d" % made, "src": anchor["dst"],
                      "dst": target["dst"], "first": first,
                      "last": first + rng.randrange(900, 40000)})
        made += 1
    edges.sort(key=lambda e: (e["first"], e["fid"]))
    return edges, made

def depth_sum(edges, pick):
    out = []
    for o in sorted({e["src"] for e in edges}):
        f = frontier(o, edges)
        if not f:
            continue
        arrival = {h: min(p) for h, p in f.items()}
        horizon = max(arrival.values())
        far = min(h for h in arrival if arrival[h] == horizon)
        out.append((o, len(arrival), horizon, far, sum(pick(s) for s in f.values())))
    return out

BEST = lambda seat: min(seat.values())
NAIVE = lambda seat: seat[min(seat)]

for skips in (0, 6, 12, 20):
    caught = 0
    made_live = 0
    for slot in ["dragnet-live"] + sorted(s for s in forge.PLANS if s.startswith("held-")):
        seed, spec = forge.PLANS[slot]
        n = 0 if slot == "dragnet-live" else skips
        e, made = edges_for(seed, spec, n)
        good, naive = depth_sum(e, BEST), depth_sum(e, NAIVE)
        bad = sum(1 for a, b in zip(good, naive) if a != b)
        if slot == "dragnet-live":
            made_live = bad
        elif bad:
            caught += 1
    print("skips=%-3d live-diff=%d  held-out caught by depth column: %d/13"
          % (skips, made_live, caught))
