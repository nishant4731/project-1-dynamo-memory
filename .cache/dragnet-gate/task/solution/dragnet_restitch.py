#!/usr/bin/env python3
"""Restitch a dragnet correlation store in place.

    python3 /app/dragnet_restitch.py <dragnet_dir>

The passes follow DRAGNET_CHARTER.md in the order it sets them out: read and
sift the segments and then the inbox, fold the operations in sequence order,
merge the co-observations, re-take every sum, repack into segments and index
them, walk the contact graph forward into REACH.tsv and back into PIVOT.tsv,
file what was turned away, consume the inbox and the scratch directory, and
write the report.
"""


import json
import os
import re
import sys

sys.path.insert(0, "/app")
import dragnet_io

RECORD_FIELDS = dragnet_io.RECORD_FIELDS
flow_sum = dragnet_io.flow_sum
render_record = dragnet_io.render_record
record_size = dragnet_io.record_size
render_report = dragnet_io.render_report
listing = dragnet_io.listing
read_lines = dragnet_io.read_lines
parse_line = dragnet_io.parse_line
load_fleet = dragnet_io.load_fleet
discard = dragnet_io.discard
refusal_row = dragnet_io.refusal_row
import shutil

# ------------------------------------------------------------------ the schema
RECORD_KEYS = frozenset(RECORD_FIELDS + ("seq", "sum"))
AMEND_KEYS = frozenset(("op", "seq", "fid", "bytes", "pkts", "state", "last"))
RETRACT_KEYS = frozenset(("op", "seq", "fid"))
STATES = ("closed", "reset", "timeout")
OPERATIONS = ("admit", "amend", "retract")
CAUSES = ("unparsable", "incomplete", "malformed", "unknown_sensor",
          "tampered", "duplicate_id")

FID_SHAPE = re.compile(r"\Af-[0-9]{5}\Z")
HOST_SHAPE = re.compile(r"\Ah-[0-9]{3}\Z")
SUM_SHAPE = re.compile(r"\A[0-9a-f]{16}\Z")
LABEL_SHAPE = re.compile(r"\A[a-z][a-z0-9]*([/-][a-z0-9]+)*\Z")
LABEL_LIMIT = 120
PORT_LOW = 1
PORT_HIGH = 65535

SEGMENT_CAPACITY = 13
SEGMENT_BYTE_BUDGET = 3450
CONTACT_COLUMNS = ("fid", "segment", "offset", "src", "dst", "state",
                   "first", "last")
REACH_COLUMNS = ("origin", "reach", "horizon", "farthest")
PIVOT_COLUMNS = ("target", "sources", "opened", "origin")
RELAY_WINDOW = 380000
FLEET_COLUMNS = ("sensor", "site")

REPORT_KEYS = (
    "segment_files_read", "segment_lines_read", "inbox_files_read",
    "inbox_lines_read", "lines_refused", "refused_unparsable",
    "refused_incomplete", "refused_malformed", "refused_unknown_sensor",
    "refused_tampered", "refused_duplicate_id", "refused_from_segments",
    "refused_from_inbox", "refused_files_written", "refused_files_ordinalled",
    "ops_admitted", "ops_amended", "ops_retracted", "orphan_amends",
    "orphan_retracts", "amends_incoherent", "observations_settled",
    "merge_groups", "observations_merged_away", "flows_settled",
    "sums_rewritten", "segments_written", "bytes_written", "contacts",
    "reach_origins", "reach_pairs", "pivot_targets", "pivot_pairs",
    "inbox_consumed", "scratch_consumed",
)


# ------------------------------------------------------------------ primitives
def is_int(value):
    """A JSON integer: booleans are not integers and neither are floats."""
    return isinstance(value, int) and not isinstance(value, bool)


def record_cause(obj, sensors, taken, extra=frozenset()):
    """Return the cause that turns a flow record away, or ``None`` if it stands."""
    for name in RECORD_FIELDS + ("seq", "sum"):
        if name not in obj:
            return "incomplete"
    if set(obj) != RECORD_KEYS | extra:
        return "malformed"
    if not isinstance(obj["fid"], str) or not FID_SHAPE.match(obj["fid"]):
        return "malformed"
    for name in ("src", "dst"):
        if not isinstance(obj[name], str) or not HOST_SHAPE.match(obj[name]):
            return "malformed"
    for name in ("sport", "dport", "first", "last", "bytes", "pkts", "seq"):
        if not is_int(obj[name]):
            return "malformed"
    for name in ("sport", "dport"):
        if not PORT_LOW <= obj[name] <= PORT_HIGH:
            return "malformed"
    if obj["bytes"] < 1 or obj["pkts"] < 1:
        return "malformed"
    if obj["last"] <= obj["first"]:
        return "malformed"
    if obj["seq"] < 0:
        return "malformed"
    if obj["state"] not in STATES:
        return "malformed"
    if (not isinstance(obj["label"], str) or len(obj["label"]) > LABEL_LIMIT
            or not LABEL_SHAPE.match(obj["label"])):
        return "malformed"
    if not isinstance(obj["sum"], str) or not SUM_SHAPE.match(obj["sum"]):
        return "malformed"
    if obj["sensor"] not in sensors:
        return "unknown_sensor"
    if obj["sum"] != flow_sum(obj):
        return "tampered"
    if obj["fid"] in taken:
        return "duplicate_id"
    return None


def amend_cause(obj):
    """Return the cause that turns an amend away, or ``None`` if it stands."""
    for name in sorted(AMEND_KEYS):
        if name not in obj:
            return "incomplete"
    if set(obj) != AMEND_KEYS:
        return "malformed"
    if not isinstance(obj["fid"], str) or not FID_SHAPE.match(obj["fid"]):
        return "malformed"
    for name in ("seq", "bytes", "pkts", "last"):
        if not is_int(obj[name]):
            return "malformed"
    if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:
        return "malformed"
    if obj["state"] not in STATES:
        return "malformed"
    return None


def retract_cause(obj):
    """Return the cause that turns a retract away, or ``None`` if it stands."""
    for name in sorted(RETRACT_KEYS):
        if name not in obj:
            return "incomplete"
    if set(obj) != RETRACT_KEYS:
        return "malformed"
    if not isinstance(obj["fid"], str) or not FID_SHAPE.match(obj["fid"]):
        return "malformed"
    if not is_int(obj["seq"]) or obj["seq"] < 0:
        return "malformed"
    return None


# ------------------------------------------------------------------ the reader
def contact_edges(flows):
    """Return the contact graph edges: settled flows that closed, in time order."""
    edges = [flow for flow in flows if flow["state"] == "closed"]
    edges.sort(key=lambda flow: (flow["first"], flow["fid"]))
    return edges


def arrivals_from(origin, edges):
    """Return, per host reached from ``origin``, the earliest time it is reached.

    A host is not reached *at a time* — it is reached at every time some trail
    lands it there, and the relay window makes those times matter separately: a
    contact taken out of a host is only a continuation of the one that brought a
    trail there when it opens within ``RELAY_WINDOW`` of that arrival.  Keeping
    only the earliest arrival is therefore not enough, because a later one can
    still be standing when an onward contact opens that the earliest has already
    let lapse.  So every arrival a host has is carried forward, and the table
    reports the least of them.
    """
    standing = {}
    arrival = {}
    for edge in edges:                       # ascending (first, fid)
        if edge["src"] == origin:
            open_now = True
        else:
            held = standing.get(edge["src"])
            open_now = held is not None and any(
                when <= edge["first"] <= when + RELAY_WINDOW for when in held)
        if not open_now:
            continue
        landed = edge["last"]
        arrival[edge["dst"]] = min(arrival.get(edge["dst"], landed), landed)
        standing.setdefault(edge["dst"], set()).add(landed)
    return arrival


def approaches_to(target, edges):
    """Return, per host that approaches ``target``, the least opening of one.

    The mirror of ``arrivals_from``.  Walking the contacts in *descending*
    ``first`` settles, for each contact, whether taking it is enough to land at
    ``target`` — either it arrives there itself, or some contact out of where it
    ends opens inside its relay window and is itself enough.  A host approaches
    ``target`` when one of its own contacts is, and its opening is the least
    ``first`` among those.  Reversing the edges and walking forward answers a
    different question, and so does keeping one latest departure per host.
    """
    onward = {}
    for edge in edges:
        onward.setdefault(edge["src"], []).append(edge)
    enough = {}
    opening = {}
    for edge in sorted(edges, key=lambda flow: (-flow["first"], flow["fid"])):
        if edge["dst"] == target:
            lands = True
        else:
            lands = any(
                enough.get(nxt["fid"])
                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW
                for nxt in onward.get(edge["dst"], ()))
        enough[edge["fid"]] = lands
        if lands:
            opening[edge["src"]] = min(opening.get(edge["src"], edge["first"]),
                                       edge["first"])
    return opening


def pivot_rows(flows):
    """Return one pivot row per host that at least one contact arrives at."""
    edges = contact_edges(flows)
    targets = sorted({edge["dst"] for edge in edges})
    rows = []
    for target in targets:
        opening = approaches_to(target, edges)
        opened = min(opening.values())
        origin = min(host for host in opening if opening[host] == opened)
        rows.append((target, len(opening), opened, origin))
    return rows


def reach_rows(flows):
    """Return one reach row per host that opened at least one contact."""
    edges = contact_edges(flows)
    origins = sorted({edge["src"] for edge in edges})
    rows = []
    for origin in origins:
        arrival = arrivals_from(origin, edges)
        horizon = max(arrival.values())
        farthest = min(host for host in arrival if arrival[host] == horizon)
        rows.append((origin, len(arrival), horizon, farthest))
    return rows


# ------------------------------------------------------------------ the packer
def pack_segments(flows):
    """Split settled flows into segments under the record and byte bounds."""
    chunks = []
    current = []
    used = 0
    for flow in flows:
        size = record_size(flow)
        if current and (len(current) >= SEGMENT_CAPACITY
                        or used + size > SEGMENT_BYTE_BUDGET):
            chunks.append(current)
            current = []
            used = 0
        current.append(flow)
        used += size
    if current:
        chunks.append(current)
    return chunks


def restitch(dragnet):
    """Restitch one dragnet in place and return the report it wrote."""
    sensors = load_fleet(dragnet)
    segment_dir = os.path.join(dragnet, "segments")
    inbox_dir = os.path.join(dragnet, "inbox")

    taken = set()
    refusals = []
    settled = []
    operations = []
    carried = {}
    tally = dict.fromkeys(CAUSES, 0)
    segment_lines = 0
    inbox_lines = 0
    refused_from_segments = 0

    segment_names = listing(segment_dir)
    for name in segment_names:
        for number, text in enumerate(read_lines(os.path.join(segment_dir, name)), 1):
            segment_lines += 1
            obj = parse_line(text)
            cause = "unparsable" if obj is None else record_cause(obj, sensors, taken)
            if cause is not None:
                tally[cause] += 1
                refused_from_segments += 1
                refusals.append(("segments/" + name, name, number, cause, text))
                continue
            taken.add(obj["fid"])
            carried[obj["fid"]] = obj["sum"]
            settled.append(dict(obj))

    inbox_names = listing(inbox_dir)
    for name in inbox_names:
        for number, text in enumerate(read_lines(os.path.join(inbox_dir, name)), 1):
            inbox_lines += 1
            obj = parse_line(text)
            if obj is None:
                cause = "unparsable"
            elif "op" not in obj:
                cause = "incomplete"
            elif obj["op"] == "admit":
                cause = record_cause(obj, sensors, taken, extra=frozenset(("op",)))
            elif obj["op"] == "amend":
                cause = amend_cause(obj)
            elif obj["op"] == "retract":
                cause = retract_cause(obj)
            else:
                cause = "malformed"
            if cause is not None:
                tally[cause] += 1
                refusals.append(("inbox/" + name, name, number, cause, text))
                continue
            if obj["op"] == "admit":
                taken.add(obj["fid"])
                carried[obj["fid"]] = obj["sum"]
            operations.append((obj, name, number))

    # --- fold: sequence order first, then the file the collector flushed it to
    operations.sort(key=lambda item: (item[0]["seq"], item[1], item[2]))
    held = {}
    for flow in settled:
        held[flow["fid"]] = flow
    order = [flow["fid"] for flow in settled]
    admitted = amended = retracted = 0
    orphan_amends = orphan_retracts = incoherent = 0
    for operation, _name, _number in operations:
        kind = operation["op"]
        fid = operation["fid"]
        if kind == "admit":
            flow = {name: operation[name] for name in RECORD_FIELDS}
            flow["seq"] = operation["seq"]
            flow["sum"] = operation["sum"]
            held[fid] = flow
            order.append(fid)
            admitted += 1
        elif kind == "amend":
            if fid not in held:
                orphan_amends += 1
            elif operation["last"] <= held[fid]["first"]:
                incoherent += 1
            else:
                target = held[fid]
                for name in ("bytes", "pkts", "state", "last"):
                    target[name] = operation[name]
                target["seq"] = operation["seq"]
                amended += 1
        else:
            if fid not in held:
                orphan_retracts += 1
            else:
                del held[fid]
                order.remove(fid)
                retracted += 1

    folded = [held[fid] for fid in order]

    # --- merge: several sensors may have watched one flow
    groups = {}
    marks = []
    for flow in folded:
        mark = (flow["src"], flow["dst"], flow["sport"], flow["dport"], flow["first"])
        if mark not in groups:
            groups[mark] = []
            marks.append(mark)
        groups[mark].append(flow)
    merged = []
    merge_groups = 0
    for mark in marks:
        crowd = groups[mark]
        if len(crowd) > 1:
            merge_groups += 1
        keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))
        flow = dict(keeper)
        flow["fid"] = min(item["fid"] for item in crowd)
        flow["last"] = max(item["last"] for item in crowd)
        flow["bytes"] = max(item["bytes"] for item in crowd)
        flow["pkts"] = max(item["pkts"] for item in crowd)
        merged.append(flow)

    sums_rewritten = 0
    for flow in merged:
        fresh = flow_sum(flow)
        if fresh != carried.get(flow["fid"]):
            sums_rewritten += 1
        flow["sum"] = fresh

    merged.sort(key=lambda flow: (flow["first"], flow["fid"]))

    # --- write the segments and the index in one pass
    shutil.rmtree(segment_dir, ignore_errors=True)
    os.makedirs(segment_dir)
    index = ["\t".join(CONTACT_COLUMNS)]
    bytes_written = 0
    chunks = pack_segments(merged)
    for number, chunk in enumerate(chunks, 1):
        name = "%04d.jsonl" % number
        offset = 0
        body = []
        for flow in chunk:
            index.append("\t".join((
                flow["fid"], name, str(offset), flow["src"], flow["dst"],
                flow["state"], str(flow["first"]), str(flow["last"]))))
            offset += record_size(flow)
            body.append(render_record(flow) + "\n")
        payload = "".join(body).encode("ascii")
        with open(os.path.join(segment_dir, name), "wb") as handle:
            handle.write(payload)
        bytes_written += len(payload)
    with open(os.path.join(dragnet, "CONTACT.tsv"), "wb") as handle:
        handle.write(("\n".join(index) + "\n").encode("ascii"))

    # --- walk the contact graph
    rows = reach_rows(merged)
    table = ["\t".join(REACH_COLUMNS)]
    for origin, reach, horizon, farthest in rows:
        table.append("\t".join((origin, str(reach), str(horizon), farthest)))
    with open(os.path.join(dragnet, "REACH.tsv"), "wb") as handle:
        handle.write(("\n".join(table) + "\n").encode("ascii"))

    pivots = pivot_rows(merged)
    board = ["\t".join(PIVOT_COLUMNS)]
    for target, sources, opened, origin in pivots:
        board.append("\t".join((target, str(sources), str(opened), origin)))
    with open(os.path.join(dragnet, "PIVOT.tsv"), "wb") as handle:
        handle.write(("\n".join(board) + "\n").encode("ascii"))

    # --- file the refusals under the name of the file they came from
    refused_dir = os.path.join(dragnet, "refused")
    shutil.rmtree(refused_dir, ignore_errors=True)
    os.makedirs(refused_dir)
    claimed = {}
    filed = {}
    ordinalled = 0
    for source, name, number, cause, text in refusals:
        if source not in filed:
            stem = name.rsplit(".", 1)[0]
            claimed[stem] = claimed.get(stem, 0) + 1
            if claimed[stem] == 1:
                filed[source] = "%s.rej" % stem
            else:
                filed[source] = "%s-%d.rej" % (stem, claimed[stem])
                ordinalled += 1
        with open(os.path.join(refused_dir, filed[source]), "a") as handle:
            handle.write(refusal_row(cause, number, source, text))

    inbox_consumed = discard(inbox_dir)
    scratch_consumed = discard(os.path.join(dragnet, "scratch"))

    report = {
        "segment_files_read": len(segment_names),
        "segment_lines_read": segment_lines,
        "inbox_files_read": len(inbox_names),
        "inbox_lines_read": inbox_lines,
        "lines_refused": len(refusals),
        "refused_unparsable": tally["unparsable"],
        "refused_incomplete": tally["incomplete"],
        "refused_malformed": tally["malformed"],
        "refused_unknown_sensor": tally["unknown_sensor"],
        "refused_tampered": tally["tampered"],
        "refused_duplicate_id": tally["duplicate_id"],
        "refused_from_segments": refused_from_segments,
        "refused_from_inbox": len(refusals) - refused_from_segments,
        "refused_files_written": len(filed),
        "refused_files_ordinalled": ordinalled,
        "ops_admitted": admitted,
        "ops_amended": amended,
        "ops_retracted": retracted,
        "orphan_amends": orphan_amends,
        "orphan_retracts": orphan_retracts,
        "amends_incoherent": incoherent,
        "observations_settled": len(folded),
        "merge_groups": merge_groups,
        "observations_merged_away": len(folded) - len(merged),
        "flows_settled": len(merged),
        "sums_rewritten": sums_rewritten,
        "segments_written": len(chunks),
        "bytes_written": bytes_written,
        "contacts": len([flow for flow in merged if flow["state"] == "closed"]),
        "reach_origins": len(rows),
        "reach_pairs": sum(row[1] for row in rows),
        "pivot_targets": len(pivots),
        "pivot_pairs": sum(row[1] for row in pivots),
        "inbox_consumed": inbox_consumed,
        "scratch_consumed": scratch_consumed,
    }
    with open(os.path.join(dragnet, "restitch_report.json"), "wb") as handle:
        handle.write(render_report(report))
    return report


def main(argv):
    """Restitch the dragnet the command line names."""
    if len(argv) != 2:
        raise SystemExit("usage: dragnet_restitch.py <dragnet_dir>")
    restitch(argv[1])
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv))
