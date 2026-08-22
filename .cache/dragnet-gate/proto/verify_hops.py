"""Brute-force check: the Pareto (arrival, hops) frontier vs trail enumeration."""
import random, sys
sys.path.insert(0, "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate/proto")
from hops import frontier, W

def brute(origin, edges, cap=8):
    """Least arrival and fewest contacts per host, over every trail."""
    best_t, best_h = {}, {}
    def walk(host, arrived, hops):
        if hops > cap:
            return
        for e in edges:
            if e["src"] != host:
                continue
            if arrived is not None and not (arrived <= e["first"] <= arrived + W):
                continue
            t, h = e["last"], hops + 1
            improved = False
            if e["dst"] not in best_t or t < best_t[e["dst"]]:
                best_t[e["dst"]] = t; improved = True
            if e["dst"] not in best_h or h < best_h[e["dst"]]:
                best_h[e["dst"]] = h; improved = True
            walk(e["dst"], t, h)
    walk(origin, None, 0)
    return best_t, best_h

bad = 0
for trial in range(300):
    rng = random.Random(9000 + trial)
    hosts = ["h-%03d" % n for n in range(rng.randint(3, 6))]
    edges = []
    for i in range(rng.randint(3, 11)):
        s, d = rng.sample(hosts, 2)
        f = rng.randrange(0, 1500000)
        edges.append({"fid": "f-%05d" % i, "src": s, "dst": d,
                      "first": f, "last": f + rng.randrange(1, 400000)})
    edges.sort(key=lambda e: (e["first"], e["fid"]))
    for h in hosts:
        bt, bh = brute(h, edges)
        fr = frontier(h, edges)
        got_t = {k: min(v) for k, v in fr.items()}
        got_h = {k: min(v.values()) for k, v in fr.items()}
        if got_t != bt:
            print("arrival mismatch", trial, h); bad += 1
        if got_h != bh:
            print("hops mismatch", trial, h, got_h, bh); bad += 1
print("mismatches:", bad, "over 300 random graphs")
