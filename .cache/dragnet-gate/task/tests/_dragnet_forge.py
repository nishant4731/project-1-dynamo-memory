"""Build crashed dragnets.

Every graded dragnet -- the one the image ships, the ones the submitted program
has never seen, the sweep set and the one derived from the submission's own
digest -- comes out of this builder, so a store is a seed plus a shape rather
than a checked-in blob.  The builder plants one line per rejection clause, so
each clause of the charter is exercised by a line that is well formed in every
other respect.
"""

import hashlib
import json
import os
import random

import _dragnet_engine as engine

SITES = ("kestrel", "marlow", "pendine", "quarry", "torrent", "vellum")
LABEL_STEMS = ("smb", "ldap", "winrm", "rdp", "http", "dns", "kerberos",
               "ssh", "rpc", "mssql", "wmi", "nfs", "syslog", "ftp")
LABEL_PARTS = ("named-pipe", "psexec", "service-write", "proxy-connect",
               "tunnel-established", "bind-simple", "axfr", "tgs-rep",
               "pssession", "shell-run", "dcom-activation", "webdav-put",
               "epmapper", "tds-login", "share-enumerate", "ticket-renew",
               "session-setup", "keepalive")


def _exact_label(width):
    """Return a well-shaped service attribution path of exactly ``width`` bytes."""
    text = "smb"
    while len(text) + 14 <= width:
        text += "/session-setup"
    if len(text) < width:
        text += "/" + "a" * (width - len(text) - 1)
    return text


def _plant_ties(flows):
    """Make the tie-breaks the charter states actually decide something."""
    groups = {}
    for flow in flows:
        mark = (flow["src"], flow["dst"], flow["sport"], flow["dport"],
                flow["first"])
        groups.setdefault(mark, []).append(flow)
    # a co-observation group whose members share the greatest seq, so the
    # keeper is settled by the lowest fid rather than by the sequence
    for crowd in groups.values():
        if len(crowd) > 1:
            top = max(item["seq"] for item in crowd)
            for item in crowd:
                item["seq"] = top
                item.update(_sealed(item))
            break
    # two flows that are not co-observations but open on the same millisecond,
    # so the settling order is decided by the fid rather than by the instant
    singles = [crowd[0] for crowd in groups.values() if len(crowd) == 1]
    if len(singles) > 1:
        one, two = singles[0], singles[1]
        two["first"] = one["first"]
        if two["last"] <= two["first"]:
            two["last"] = two["first"] + 1
        two.update(_sealed(two))
    return flows


def _plant_bounds(flows):
    """Sit one accepted flow on each inclusive bound the charter states."""
    room = [flow for flow in flows if flow["state"] == "closed"]
    if len(room) < 7:
        return flows
    for flow, key, value in ((room[0], "sport", PORT_LOW),
                             (room[1], "dport", PORT_HIGH),
                             (room[2], "bytes", 1),
                             (room[3], "pkts", 1),
                             (room[4], "seq", 0),
                             (room[5], "label", _exact_label(LABEL_LIMIT))):
        flow[key] = value
        flow.update(_sealed(flow))
    room[6]["last"] = room[6]["first"] + 1
    room[6].update(_sealed(room[6]))
    return flows


def _restate(state):
    """Return a state other than the one a flow already carries."""
    return "reset" if state == "closed" else "closed"


def _label(rng):
    """Return one service attribution path; these vary a lot in length."""
    parts = [rng.choice(LABEL_STEMS)]
    for _ in range(rng.randrange(0, 8)):
        parts.append(rng.choice(LABEL_PARTS))
    return "/".join(parts)


PORT_LOW = 1
PORT_HIGH = 65535
LABEL_LIMIT = 120

STEP = 400000
SPAN = 60000
DUR_LOW = 900
DUR_HIGH = 40000

# one planted line per rejection clause; each is well formed but for one thing
SEGMENT_FAULTS = (
    "cut", "garbage", "notobject", "missing", "extrakey", "boolint", "floatint",
    "badfid", "badhost", "badstate", "badport", "zeropkts", "flat", "backwards",
    "badsum", "negseq", "stranger", "edited", "twin", "badlabel", "longlabel",
    "stranger_edited", "portzero", "porttop", "zerobytes", "overlabel",
    "shortsum", "upsum", "shortfid", "letterhost", "trailinglabel",
)
INBOX_FAULTS = (
    "cut", "garbage", "missing", "extrakey", "boolint", "floatint", "badfid",
    "badstate", "badport", "flat", "badsum", "stranger", "edited", "twin",
    "badlabel",
    "stranger_edited", "portzero", "zerobytes", "overlabel", "shortsum",
    "shortfid",
    "badop", "noop", "amend_missing", "amend_bad_state", "amend_float",
    "amend_extra", "retract_extra", "retract_missing",
)


def _text(record):
    """Render a record the way the collector wrote it, with the sum in place."""
    body = {name: record[name] for name in engine.RECORD_FIELDS}
    body["seq"] = record["seq"]
    body["sum"] = record["sum"]
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


def _sealed(record):
    """Return the record with a sum that matches its own payload."""
    record = dict(record)
    record["sum"] = engine.flow_sum(record)
    return record


def _hosts(count):
    return ["h-%03d" % (n + 1) for n in range(count)]


def _fleet(count):
    return ["tap-%02d" % (n + 1) for n in range(count)]


# ---------------------------------------------------------------- the contacts
def _layer_split(rng, hosts, layers):
    """Split the hosts into ordered layers, keeping every layer non-empty."""
    pool = list(hosts)
    rng.shuffle(pool)
    split = [[] for _ in range(layers)]
    for index, host in enumerate(pool):
        split[index % layers].append(host)
    for group in split:
        group.sort()
    return split


def _window(rng, spec, depth):
    """Return a contact window inside the band that belongs to one depth."""
    first = depth * STEP + rng.randrange(0, spec.get("span", SPAN))
    return first, first + rng.randrange(spec.get("dur_low", DUR_LOW),
                                        spec.get("dur_high", DUR_HIGH))


def _contacts(rng, spec, hosts):
    """Return the closed contacts, as (src, dst, first, last) in build order."""
    layers = _layer_split(rng, hosts, spec["layers"])
    edges = []
    ends = {}
    for depth in range(1, len(layers)):
        for host in layers[depth]:
            parents = rng.sample(
                layers[depth - 1],
                min(len(layers[depth - 1]), rng.randint(1, spec["parents"])),
            )
            for parent in parents:
                first, last = _window(rng, spec, depth)
                edges.append([parent, host, first, last])
                ends.setdefault(host, []).append(last)
    for _ in range(spec.get("touch", 0)):
        if len(edges) < 2:
            break
        anchor = rng.choice(edges)
        followers = [edge for edge in edges if edge[0] == anchor[1]]
        if not followers:
            continue
        follower = rng.choice(followers)
        follower[2] = anchor[3]
        follower[3] = follower[2] + rng.randrange(
            spec.get("dur_low", DUR_LOW), spec.get("dur_high", DUR_HIGH))
    twinned = spec.get("twin_end", 0)
    if twinned > 1 and len(edges) > twinned:
        latest = sorted(edges, key=lambda edge: (-edge[3], edge[0]))[:twinned]
        settled = latest[0][3]
        for edge in latest:
            edge[3] = settled
            if edge[2] >= settled:
                edge[2] = settled - rng.randrange(1, 400)
    for _ in range(spec.get("stall", 0)):
        if len(edges) < 2:
            break
        anchor = rng.choice(edges)
        followers = [edge for edge in edges if edge[0] == anchor[1]]
        if not followers:
            continue
        follower = rng.choice(followers)
        follower[2] = anchor[2] + max(1, (anchor[3] - anchor[2]) // 2)
        follower[3] = follower[2] + rng.randrange(
            spec.get("dur_low", DUR_LOW), spec.get("dur_high", DUR_HIGH))
    # Both edges of the relay window, alternating: a hand-off that opens exactly
    # a window after its predecessor closed, which a trail may take, and one that
    # opens a single unit later, which it may not.  Neither can be found by
    # chance -- the window is one point in a range of a million.
    wanted = spec.get("window_edge", 0)
    if wanted:
        touched = set()
        placed = 0
        for anchor in sorted(edges, key=lambda edge: (edge[2], edge[0], edge[1])):
            if id(anchor) in touched:
                continue
            followers = [edge for edge in edges
                         if edge[0] == anchor[1] and id(edge) not in touched
                         and edge is not anchor]
            if not followers:
                continue
            follower = followers[0]
            offset = engine.RELAY_WINDOW + (placed % 2)
            follower[2] = anchor[3] + offset
            follower[3] = follower[2] + rng.randrange(
                spec.get("dur_low", DUR_LOW), spec.get("dur_high", DUR_HIGH))
            touched.add(id(anchor))
            touched.add(id(follower))
            placed += 1
            if placed >= wanted:
                break
    return [tuple(edge) for edge in edges]


def _flows(rng, spec):
    """Return every settled-to-be flow of one dragnet, in collector order."""
    hosts = _hosts(spec["hosts"])
    fleet = _fleet(spec["sensors"])
    edges = _contacts(rng, spec, hosts)
    flows = []
    counter = [0]

    def make(src, dst, first, last, state):
        counter[0] += 1
        return _sealed({
            "fid": "f-%05d" % counter[0],
            "src": src,
            "dst": dst,
            "sport": rng.randrange(1024, 65536),
            "dport": rng.choice((22, 80, 135, 389, 443, 445, 3389, 5985, 8080)),
            "first": first,
            "last": last,
            "bytes": rng.randrange(1, 9500000),
            "pkts": rng.randrange(1, 700000),
            "sensor": rng.choice(fleet),
            "label": _label(rng),
            "state": state,
            "seq": 0,
        })

    for src, dst, first, last in edges:
        flows.append(make(src, dst, first, last, "closed"))
    for _ in range(spec["noise"]):
        src, dst = rng.sample(hosts, 2)
        depth = rng.randrange(0, spec["layers"])
        first, last = _window(rng, spec, depth)
        flows.append(make(src, dst, first, last, rng.choice(("reset", "timeout"))))

    retries = []
    for flow in rng.sample(flows, min(spec.get("retries", 0), len(flows))):
        if flow["state"] != "closed":
            continue
        again = dict(flow)
        counter[0] += 1
        again["fid"] = "f-%05d" % counter[0]
        again["first"] = flow["last"] + rng.randrange(60, 9000)
        again["last"] = again["first"] + rng.randrange(
            spec.get("dur_low", DUR_LOW), spec.get("dur_high", DUR_HIGH))
        again["sensor"] = rng.choice(fleet)
        retries.append(_sealed(again))
    flows.extend(retries)

    twins = []
    for flow in rng.sample(flows, min(spec["merges"], len(flows))):
        crowd = rng.randint(1, 2)
        for _ in range(crowd):
            other = dict(flow)
            counter[0] += 1
            other["fid"] = "f-%05d" % counter[0]
            other["sensor"] = rng.choice(fleet)
            if spec["merge_agree"]:
                other["bytes"] = flow["bytes"]
                other["pkts"] = flow["pkts"]
            else:
                other["last"] = flow["last"] + rng.randrange(1, 5000)
                other["bytes"] = flow["bytes"] + rng.randrange(1, 40000)
                other["pkts"] = flow["pkts"] + rng.randrange(1, 300)
            twins.append(_sealed(other))
    flows.extend(twins)

    order = list(range(len(flows)))
    rng.shuffle(order)
    for rank, index in enumerate(order, 1):
        flows[index]["seq"] = rank
        flows[index] = _sealed(flows[index])
    if spec.get("bounds"):
        flows = _plant_bounds(flows)
        flows = _plant_ties(flows)
    return flows


# ------------------------------------------------------------------- the faults
def _fault_line(rng, kind, base, fleet, seen):
    """Return the text of one planted line, wrong in exactly one respect."""
    record = dict(base)
    if kind == "cut":
        return _text(_sealed(record))[: rng.randrange(20, 40)]
    if kind == "garbage":
        return "collector: short write at offset 40961"
    if kind == "notobject":
        return json.dumps([record["fid"], record["src"], record["dst"]])
    if kind == "missing":
        body = json.loads(_text(_sealed(record)))
        del body["pkts"]
        return json.dumps(body, sort_keys=True, separators=(",", ":"))
    if kind == "extrakey":
        body = json.loads(_text(_sealed(record)))
        body["vlan"] = 412
        return json.dumps(body, sort_keys=True, separators=(",", ":"))
    if kind == "boolint":
        record = _sealed(record)
        body = json.loads(_text(record))
        body["pkts"] = True
        return json.dumps(body, sort_keys=True, separators=(",", ":"))
    if kind == "floatint":
        record = _sealed(record)
        body = json.loads(_text(record))
        text = json.dumps(body, sort_keys=True, separators=(",", ":"))
        return text.replace('"bytes":%d' % body["bytes"],
                            '"bytes":%d.0' % body["bytes"], 1)
    if kind == "badfid":
        record["fid"] = "f-%04dz" % rng.randrange(1000, 9999)
        return _text(_sealed(record))
    if kind == "badhost":
        record["dst"] = "h-%d" % rng.randrange(10, 99)
        return _text(_sealed(record))
    if kind == "badstate":
        record["state"] = "half-open"
        return _text(_sealed(record))
    if kind == "badlabel":
        record["label"] = "SMB/Named_Pipe"
        return _text(_sealed(record))
    if kind == "longlabel":
        record["label"] = "smb/" + "named-pipe-service-write/" * 5 + "close"
        return _text(_sealed(record))
    if kind == "badport":
        record["dport"] = 65536 + rng.randrange(0, 4000)
        return _text(_sealed(record))
    if kind == "zeropkts":
        record["pkts"] = 0
        return _text(_sealed(record))
    if kind == "flat":
        record["last"] = record["first"]
        return _text(_sealed(record))
    if kind == "backwards":
        record["last"] = record["first"] - rng.randrange(1, 500)
        return _text(_sealed(record))
    if kind == "badsum":
        record = _sealed(record)
        record["sum"] = "Z" + record["sum"][1:]
        return _text(record)
    if kind == "negseq":
        record["seq"] = -1
        return _text(_sealed(record))
    if kind == "portzero":
        record["sport"] = PORT_LOW - 1
        return _text(_sealed(record))
    if kind == "porttop":
        record["dport"] = PORT_HIGH + 1
        return _text(_sealed(record))
    if kind == "zerobytes":
        record["bytes"] = 0
        return _text(_sealed(record))
    if kind == "overlabel":
        record["label"] = _exact_label(LABEL_LIMIT + 1)
        return _text(_sealed(record))
    if kind == "trailinglabel":
        record["label"] = "smb/named-pipe/"
        return _text(_sealed(record))
    if kind == "shortsum":
        record = _sealed(record)
        record["sum"] = record["sum"][:-1]
        return _text(record)
    if kind == "upsum":
        record = _sealed(record)
        record["sum"] = record["sum"][:-1] + record["sum"][-1].upper()
        return _text(record)
    if kind == "shortfid":
        record["fid"] = "f-0123"
        return _text(_sealed(record))
    if kind == "letterhost":
        record["src"] = "h-a04"
        return _text(_sealed(record))
    if kind == "stranger":
        record["sensor"] = "tap-%02d" % (len(fleet) + rng.randrange(3, 9))
        return _text(_sealed(record))
    if kind == "edited":
        record = _sealed(record)
        record["bytes"] = record["bytes"] + 4096
        return _text(record)
    if kind == "stranger_edited":
        record["sensor"] = "tap-%02d" % (len(fleet) + rng.randrange(3, 9))
        record = _sealed(record)
        record["pkts"] = record["pkts"] + 11
        return _text(record)
    if kind == "twin":
        record["fid"] = rng.choice(sorted(seen))
        record["dport"] = 4444
        return _text(_sealed(record))
    raise ValueError("no such fault: %s" % kind)


def _inbox_fault(rng, kind, base, fleet, seen):
    """Return the text of one planted inbox line, wrong in exactly one respect."""
    if kind in ("badop", "noop"):
        body = json.loads(_text(_sealed(dict(base))))
        body["op"] = "revise" if kind == "badop" else None
        return json.dumps(body, sort_keys=True, separators=(",", ":"))
    if kind == "amend_missing":
        return json.dumps({"op": "amend", "seq": rng.randrange(1, 400),
                           "fid": rng.choice(sorted(seen)), "bytes": 8192,
                           "pkts": 44, "last": base["last"] + 900},
                          sort_keys=True, separators=(",", ":"))
    if kind == "amend_bad_state":
        return json.dumps({"op": "amend", "seq": rng.randrange(1, 400),
                           "fid": rng.choice(sorted(seen)), "bytes": 8192,
                           "pkts": 44, "state": "closing",
                           "last": base["last"] + 900},
                          sort_keys=True, separators=(",", ":"))
    if kind == "amend_float":
        text = json.dumps({"op": "amend", "seq": rng.randrange(1, 400),
                           "fid": rng.choice(sorted(seen)), "bytes": 8192,
                           "pkts": 44, "state": "closed",
                           "last": base["last"] + 900},
                          sort_keys=True, separators=(",", ":"))
        return text.replace('"bytes":8192', '"bytes":8192.0', 1)
    if kind == "amend_extra":
        return json.dumps({"op": "amend", "seq": rng.randrange(1, 400),
                           "fid": rng.choice(sorted(seen)), "bytes": 8192,
                           "pkts": 44, "state": "closed", "sensor": "tap-01",
                           "last": base["last"] + 900},
                          sort_keys=True, separators=(",", ":"))
    if kind == "retract_extra":
        return json.dumps({"op": "retract", "seq": rng.randrange(1, 400),
                           "fid": rng.choice(sorted(seen)), "why": "operator"},
                          sort_keys=True, separators=(",", ":"))
    if kind == "retract_missing":
        return json.dumps({"op": "retract", "seq": rng.randrange(1, 400)},
                          sort_keys=True, separators=(",", ":"))
    line = _fault_line(rng, kind, base, fleet, seen)
    if kind in ("cut", "garbage"):
        return line
    try:
        body = json.loads(line)
    except ValueError:
        return line
    if not isinstance(body, dict):
        return line
    body["op"] = "admit"
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


# ------------------------------------------------------------------- the plans
def build_plan(seed, spec):
    """Return the complete file plan of one crashed dragnet."""
    rng = random.Random(seed)
    fleet = _fleet(spec["sensors"])
    flows = _flows(rng, spec)
    rng.shuffle(flows)

    held_back = spec["admits"]
    admits = flows[:held_back]
    resident = flows[held_back:]
    seen = {flow["fid"] for flow in resident}

    segment_lines = [_text(flow) for flow in resident]
    for offset, kind in enumerate(spec["segment_faults"]):
        base = dict(resident[(offset * 7 + 3) % len(resident)])
        base["fid"] = "f-9%04d" % (offset + 1)
        base["seq"] = 0
        spot = min(len(segment_lines), (offset * 5 + 2) % (len(segment_lines) + 1))
        segment_lines.insert(spot, _fault_line(rng, kind, base, fleet, seen))

    segments = {}
    if spec["segments"] < 1:
        segment_lines = []
    per_file = max(1, (len(segment_lines) + max(1, spec["segments"]) - 1)
                   // max(1, spec["segments"]))
    for number in range(max(0, spec["segments"])):
        chunk = segment_lines[number * per_file:(number + 1) * per_file]
        if chunk or number == 0:
            segments["%04d.jsonl" % (number + 1)] = chunk
    if spec["segments"] >= 1 and segment_lines[spec["segments"] * per_file:]:
        last = "%04d.jsonl" % spec["segments"]
        segments[last] = segments.get(last, []) + segment_lines[spec["segments"] * per_file:]

    # --- the operations the collector had accepted but not folded
    operations = []
    seq_pool = list(range(500, 500 + 4 * (len(admits) + spec["amends"]
                                          + spec["retracts"] + 12)))
    rng.shuffle(seq_pool)
    pool = iter(seq_pool)
    resident_ids = sorted(seen)

    for flow in admits:
        flow = dict(flow)
        flow["seq"] = next(pool)
        body = json.loads(_text(_sealed(flow)))
        body["op"] = "admit"
        operations.append((flow["seq"], json.dumps(
            body, sort_keys=True, separators=(",", ":"))))

    contended = []
    for flow in admits[:spec["contend"]]:
        seq = max(item[0] for item in operations
                  if json.loads(item[1])["fid"] == flow["fid"]) + 1
        contended.append((seq, json.dumps(
            {"op": "amend", "seq": seq, "fid": flow["fid"],
             "bytes": flow["bytes"] + 51200, "pkts": flow["pkts"] + 61,
             "state": flow["state"], "last": flow["last"] + 7700},
            sort_keys=True, separators=(",", ":"))))

    for index in range(spec["amends"]):
        fid = resident_ids[(index * 11 + 5) % len(resident_ids)]
        target = [flow for flow in resident if flow["fid"] == fid][0]
        seq = next(pool)
        quiet = spec["quiet_amends"] > index
        operations.append((seq, json.dumps(
            {"op": "amend", "seq": seq, "fid": fid,
             "bytes": target["bytes"] if quiet else target["bytes"] + 3300,
             "pkts": target["pkts"] if quiet else target["pkts"] + 17,
             "state": (_restate(target["state"])
                       if index < spec.get("restate", 0) else target["state"]),
             "last": target["last"] if quiet else target["last"] + 2600},
            sort_keys=True, separators=(",", ":"))))

    taken_away = []
    for index in range(spec["retracts"]):
        fid = resident_ids[(index * 17 + 9) % len(resident_ids)]
        seq = next(pool)
        taken_away.append((fid, seq))
        operations.append((seq, json.dumps(
            {"op": "retract", "seq": seq, "fid": fid},
            sort_keys=True, separators=(",", ":"))))

    # an amend that arrives after the retract it chases is an orphan, because
    # the flow it names is no longer among them by the time it applies
    for index in range(min(spec.get("late_amends", 0), len(taken_away))):
        fid, retired = taken_away[index]
        operations.append((retired + 1, json.dumps(
            {"op": "amend", "seq": retired + 1, "fid": fid, "bytes": 6400,
             "pkts": 29, "state": "closed", "last": 3600000 + index},
            sort_keys=True, separators=(",", ":"))))

    for index in range(spec["orphan_amends"]):
        seq = next(pool)
        operations.append((seq, json.dumps(
            {"op": "amend", "seq": seq, "fid": "f-8%04d" % (index + 1),
             "bytes": 4096, "pkts": 31, "state": "closed", "last": 900000 + index},
            sort_keys=True, separators=(",", ":"))))

    for index in range(spec["orphan_retracts"]):
        seq = next(pool)
        operations.append((seq, json.dumps(
            {"op": "retract", "seq": seq, "fid": "f-7%04d" % (index + 1)},
            sort_keys=True, separators=(",", ":"))))

    if spec.get("bounds"):
        fid = resident_ids[(29) % len(resident_ids)]
        target = [flow for flow in resident if flow["fid"] == fid][0]
        seq = next(pool)
        operations.append((seq, json.dumps(
            {"op": "amend", "seq": seq, "fid": fid, "bytes": 990, "pkts": 7,
             "state": target["state"], "last": target["first"] + 1},
            sort_keys=True, separators=(",", ":"))))

    for index in range(spec["incoherent"]):
        fid = resident_ids[(index * 23 + 13) % len(resident_ids)]
        target = [flow for flow in resident if flow["fid"] == fid][0]
        seq = next(pool)
        operations.append((seq, json.dumps(
            {"op": "amend", "seq": seq, "fid": fid, "bytes": 700, "pkts": 3,
             "state": "reset",
             "last": target["first"] - 40 * index},
            sort_keys=True, separators=(",", ":"))))

    rng.shuffle(operations)
    inbox_lines = [text for _seq, text in operations]

    for offset, kind in enumerate(spec["inbox_faults"]):
        base = dict(resident[(offset * 13 + 6) % len(resident)])
        base["fid"] = "f-6%04d" % (offset + 1)
        base["seq"] = next(pool)
        spot = min(len(inbox_lines), (offset * 3 + 1) % (len(inbox_lines) + 1))
        inbox_lines.insert(spot, _inbox_fault(rng, kind, base, fleet, seen))

    nested_inbox = {}
    if spec.get("bounds") and spec["inbox_files"]:
        nested_inbox["stalled/0009.ndjson"] = "collector spill, never folded\n"

    inbox = {}
    files = max(1, spec["inbox_files"])
    per_inbox = max(1, (len(inbox_lines) + files - 1) // files)
    for number in range(files):
        chunk = inbox_lines[number * per_inbox:(number + 1) * per_inbox]
        if chunk or number == 0:
            inbox["%04d.ndjson" % (number + 1)] = chunk
    spill = inbox_lines[files * per_inbox:]
    if spill:
        last = "%04d.ndjson" % files
        inbox[last] = inbox.get(last, []) + spill

    if spec.get("seq_tie", 0) and len(inbox) > 1:
        names = sorted(inbox)
        fid = resident_ids[3 % len(resident_ids)]
        target = [flow for flow in resident if flow["fid"] == fid][0]
        shared = next(pool)
        early = json.dumps(
            {"op": "amend", "seq": shared, "fid": fid, "bytes": 111000,
             "pkts": 71, "state": target["state"],
             "last": target["last"] + 11000},
            sort_keys=True, separators=(",", ":"))
        later = json.dumps(
            {"op": "amend", "seq": shared, "fid": fid, "bytes": 222000,
             "pkts": 92, "state": target["state"],
             "last": target["last"] + 22000},
            sort_keys=True, separators=(",", ":"))
        inbox[names[0]] = inbox[names[0]] + [early]
        inbox[names[1]] = [later] + inbox[names[1]]

    # the contending pair goes to the FIRST inbox file, ahead of its own admit
    if contended:
        head = sorted(inbox)[0]
        inbox[head] = [text for _seq, text in contended] + inbox[head]

    scratch = {}
    for number in range(spec["scratch"]):
        scratch["part-%03d.tmp" % (number + 1)] = (
            "collector scratch %d\n" % number) * (number + 2)
    # the collector spilled into subdirectories as well, so what a restitch
    # consumes is a tree rather than a flat directory
    if spec.get("bounds") and spec["scratch"]:
        scratch["spill/part-%03d.tmp" % (spec["scratch"] + 1)] = "spilled\n"
        scratch["spill/deeper/part-%03d.tmp" % (spec["scratch"] + 2)] = "deeper\n"

    fleet_rows = ["\t".join(engine.FLEET_COLUMNS)]
    for index, sensor in enumerate(fleet):
        fleet_rows.append("%s\t%s" % (sensor, SITES[index % len(SITES)]))

    return {
        "FLEET.tsv": "\n".join(fleet_rows) + "\n",
        "segments": segments,
        "inbox": inbox,
        "nested_inbox": nested_inbox,
        "scratch": scratch,
    }


def write_plan(target, plan):
    """Materialise one crashed dragnet on disk."""
    os.makedirs(target)
    with open(os.path.join(target, "FLEET.tsv"), "w") as handle:
        handle.write(plan["FLEET.tsv"])
    for slot, holder in (("segments", "segments"), ("inbox", "inbox")):
        root = os.path.join(target, holder)
        if not plan[slot]:
            continue
        os.makedirs(root)
        for name, lines in sorted(plan[slot].items()):
            with open(os.path.join(root, name), "w") as handle:
                if lines:
                    handle.write("\n".join(lines) + "\n")
    for slot, holder in (("nested_inbox", "inbox"), ("scratch", "scratch")):
        for name, body in sorted(plan.get(slot, {}).items()):
            path = os.path.join(target, holder, name)
            parent = os.path.dirname(path)
            if not os.path.isdir(parent):
                os.makedirs(parent)
            with open(path, "w") as handle:
                handle.write(body)


BASE = {
    "hosts": 46,
    "span": SPAN,
    "window_edge": 6,
    "dur_low": DUR_LOW,
    "dur_high": DUR_HIGH,
    "sensors": 6,
    "layers": 5,
    "parents": 3,
    "touch": 5,
    "stall": 4,
    "twin_end": 7,
    "retries": 9,
    "restate": 6,
    "late_amends": 5,
    "seq_tie": 4,
    "bounds": True,
    "noise": 20,
    "merges": 13,
    "merge_agree": False,
    "admits": 10,
    "amends": 8,
    "quiet_amends": 2,
    "retracts": 3,
    "orphan_amends": 5,
    "orphan_retracts": 5,
    "incoherent": 5,
    "contend": 6,
    "segments": 4,
    "inbox_files": 3,
    "scratch": 3,
    "segment_faults": SEGMENT_FAULTS,
    "inbox_faults": INBOX_FAULTS,
}


def shape(**overrides):
    """Return the base shape with a few knobs moved."""
    spec = dict(BASE)
    spec.update(overrides)
    return spec


PLANS = {
    # the dragnet the image ships: a quiet shift, one contact into each host,
    # wide gaps between the bands, and co-observations that agree
    "dragnet-live": (20260214, shape(
        hosts=44, layers=5, parents=1, touch=0, stall=0, noise=16, merges=5,
        span=8000, dur_low=45000, dur_high=60000, window_edge=0,
        merge_agree=True, twin_end=0, retries=0, restate=0, late_amends=0,
        bounds=False, seq_tie=0,
        admits=5, amends=4, quiet_amends=0, retracts=2,
        orphan_amends=1, orphan_retracts=0, incoherent=0, contend=1,
        segments=3, inbox_files=2, scratch=2,
        segment_faults=("cut", "edited", "missing"),
        inbox_faults=("garbage", "twin"))),
    "held-broad": (770311, shape(parents=5, touch=5, stall=4)),
    "held-webbed": (770312, shape(hosts=52, layers=6, parents=6, touch=13,
                                  stall=10, merges=12, segments=5)),
    "held-stalled": (770313, shape(hosts=40, layers=5, parents=4, touch=14,
                                   stall=15, noise=26)),
    "held-crowded": (770314, shape(merges=18, admits=16, amends=13,
                                   quiet_amends=5, retracts=7,
                                   parents=5, touch=10, stall=8)),
    "held-orphaned": (770315, shape(orphan_amends=8, orphan_retracts=7,
                                    incoherent=6, contend=4,
                                    parents=5, touch=10, stall=8)),
    "held-shallow": (770316, shape(hosts=24, layers=2, parents=6, touch=9,
                                   stall=7, noise=8, segments=1,
                                   inbox_files=1)),
    "held-deep": (770317, shape(hosts=60, layers=9, parents=4, touch=15,
                                stall=12, noise=32, segments=6, inbox_files=4)),
    "held-quiet": (770318, shape(segment_faults=(), inbox_faults=(),
                                 orphan_amends=0, orphan_retracts=0,
                                 incoherent=0,
                                 parents=5, touch=10, stall=8)),
    "held-noinbox": (770319, shape(admits=0, amends=0, retracts=0,
                                   orphan_amends=0, orphan_retracts=0,
                                   incoherent=0, contend=0, inbox_faults=(),
                                   inbox_files=0,
                                   parents=5, touch=10, stall=8)),
    "held-noscratch": (770320, shape(scratch=0, merges=15, touch=16,
                                     parents=5, stall=8)),
    # seeds chosen so a segment lands exactly on the byte budget, which is the
    # only place the bound's inclusive edge decides anything
    # the correlator died before it packed anything: no segments/ at all, so
    # every settled flow has to arrive through the inbox
    "held-nosegments": (770322, shape(hosts=30, layers=4, parents=3, touch=4,
                                      stall=3, noise=10, merges=6, segments=0,
                                      admits=40, amends=6, retracts=2,
                                      inbox_files=4, segment_faults=())),
    "held-brimful": (882534, shape(hosts=38, layers=5, parents=5, touch=10,
                                   stall=8, noise=18, merges=8, segments=4,
                                   inbox_files=3)),
    "held-onesegment": (770321, shape(hosts=20, layers=3, parents=4, noise=6,
                                      segments=1, merges=10, touch=7)),
    # not graded: the only job of this dragnet is to source the truthful
    # fragments the charter's format sheet quotes
    "format-sheet": (99001, shape(hosts=18, layers=4, parents=2, touch=2,
                                  stall=2, noise=5, merges=3, admits=3,
                                  amends=2, retracts=1, segments=2,
                                  inbox_files=2, scratch=1)),
    "sweep-a": (5510, shape(hosts=30, layers=4, parents=5, touch=9, stall=7,
                            noise=7, merges=5, admits=4, amends=3, retracts=2,
                            segments=2, inbox_files=2, scratch=1)),
    "sweep-b": (5511, shape(hosts=24, layers=3, parents=4, touch=8, stall=7,
                            noise=5, merges=4, admits=3, amends=2,
                            quiet_amends=1, retracts=1, orphan_amends=1,
                            orphan_retracts=1, incoherent=1, contend=1,
                            segments=2, inbox_files=2, scratch=1)),
    "sweep-c": (5512, shape(hosts=32, layers=5, parents=4, touch=10, stall=8,
                            noise=8, merges=6, admits=3, amends=2, retracts=1,
                            segments=2, inbox_files=2, scratch=2)),
    "sweep-d": (5513, shape(hosts=26, layers=3, parents=5, touch=8, stall=6,
                            noise=4, merges=4, admits=2, amends=2, retracts=1,
                            segments=1, inbox_files=1, scratch=1,
                            inbox_faults=INBOX_FAULTS[:12])),
    "sweep-f": (770953, shape(hosts=24, layers=4, parents=3, touch=4, stall=3,
                              noise=7, merges=5, admits=4, amends=3, retracts=2,
                              segments=2, inbox_files=2, scratch=1)),
    "sweep-g": (771065, shape(hosts=24, layers=4, parents=3, touch=4, stall=3,
                              noise=7, merges=5, admits=4, amends=3, retracts=2,
                              segments=2, inbox_files=2, scratch=1)),
    "sweep-e": (5514, shape(hosts=28, layers=4, parents=4, touch=9, stall=7,
                            noise=6, merges=5, admits=3, amends=3,
                            quiet_amends=2, retracts=2, segments=2,
                            inbox_files=2, scratch=1,
                            segment_faults=SEGMENT_FAULTS[7:])),
}


def build_store(slot):
    """Return the plan of one named dragnet."""
    seed, spec = PLANS[slot]
    return build_plan(seed, spec)


def build_salted(salt):
    """Return the plan of a dragnet keyed to the submission's own digest."""
    rng = random.Random(salt)
    spec = shape(
        hosts=rng.choice((16, 20, 24, 28)),
        layers=rng.choice((4, 5, 6)),
        parents=rng.choice((2, 3, 4)),
        touch=rng.randint(2, 7),
        stall=rng.randint(2, 6),
        noise=rng.randint(8, 22),
        merges=rng.randint(4, 12),
        admits=rng.randint(4, 12),
        amends=rng.randint(4, 10),
        quiet_amends=rng.randint(1, 3),
        retracts=rng.randint(1, 5),
        orphan_amends=rng.randint(1, 5),
        orphan_retracts=rng.randint(1, 4),
        incoherent=rng.randint(1, 4),
        contend=rng.randint(1, 3),
        segments=rng.randint(2, 4),
        inbox_files=rng.randint(2, 4),
        scratch=rng.randint(0, 3),
    )
    return build_plan(salt ^ 0x5EA5A17, spec)


def digest_plan(plan):
    """Return a digest over one plan, so a rebuilt dragnet can be compared."""
    blob = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
