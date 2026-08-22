"""Does a fewest-contacts column diverge from the least-arrival walk?"""
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

def frontier(origin, edges):
    """Per host: every arrival time it is left standing at, and the fewest
    contacts any trail takes to leave it there at that time.

    There is no domination across times: with a relay window a later arrival is
    not a worse one, because it may still be standing when a contact opens that
    an earlier arrival has already let lapse.
    """
    front = {}
    for e in edges:
        cands = []
        if e["src"] == origin:
            cands.append(1)
        for when, hops in front.get(e["src"], {}).items():
            if when <= e["first"] <= when + W:
                cands.append(hops + 1)
        if not cands:
            continue
        seat = front.setdefault(e["dst"], {})
        best = min(cands)
        landed = e["last"]
        if landed not in seat or best < seat[landed]:
            seat[landed] = best
    return front


def rows_correct(edges):
    out = []
    for o in sorted({e["src"] for e in edges}):
        f = frontier(o, edges)
        if not f:
            continue
        arrival = {h: min(p) for h, p in f.items()}
        horizon = max(arrival.values())
        far = min(h for h in arrival if arrival[h] == horizon)
        depth = sum(min(seat.values()) for seat in f.values())
        out.append((o, len(arrival), horizon, far, depth))
    return out


def rows_variant(edges, pick):
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


PICKS = {
    "reach_on_the_least_arrival_trail": lambda seat: seat[min(seat)],
    "reach_on_the_greatest_arrival": lambda seat: seat[max(seat)],
    "reach_takes_the_most_contacts": lambda seat: max(seat.values()),
}

slots = ["dragnet-live"] + sorted(s for s in forge.PLANS if s.startswith("held-"))
tally = {}
for slot in slots:
    seed, spec = forge.PLANS[slot]
    e = edges_for(seed, spec)
    good = rows_correct(e)
    line = "%-18s rows=%3d" % (slot, len(good))
    for name, pick in PICKS.items():
        v = rows_variant(e, pick)
        bad = sum(1 for a, b in zip(good, v) if a != b)
        line += "  %s=%-3s" % (name.split("_")[1] if False else name[:14], bad)
        tally.setdefault(name, 0)
        if slot != "dragnet-live" and bad:
            tally[name] += 1
    print(line)
print()
for name, n in tally.items():
    print("%-40s held-out caught: %d/13" % (name, n))
