#!/usr/bin/env python3
"""Reading and writing for a dragnet, in the shapes DRAGNET_CHARTER.md fixes.

This module is supplied, read-only, and carries only the mechanical half of a
restitch: the source order lines are read in, the canonical payload a check
value is taken over, the one canonical text of a settled record, of a report and
of a refusal row, and the removal of a consumed directory.  Every decision the
charter asks for -- what stands and what is turned away and under which cause,
the order operations fold in, what makes two observations one flow, how segments
are bounded, what a trail through the contact graph is, what each counter counts
and how the files under refused/ are named -- is not here and is not implied by
anything here.
"""

import hashlib
import json
import os
import shutil

# the eleven keys of a flow record that the check value is taken over, in the
# order DRAGNET_CHARTER.md section 2 lists them
RECORD_FIELDS = ("fid", "src", "dst", "sport", "dport", "first", "last",
                 "bytes", "pkts", "sensor", "label", "state")


def listing(root):
    """Return the file names directly under ``root`` in name order, or ``[]``."""
    if not os.path.isdir(root):
        return []
    return sorted(name for name in os.listdir(root)
                  if os.path.isfile(os.path.join(root, name)))


def read_lines(path):
    """Return the lines of one source file, without their closing newline."""
    with open(path, "rb") as handle:
        blob = handle.read()
    text = blob.decode("utf-8", "replace")
    if text.endswith("\n"):
        text = text[:-1]
    if not text:
        return []
    return text.split("\n")


def parse_line(text):
    """Return the JSON object a line holds, or ``None`` when it is not one."""
    try:
        obj = json.loads(text)
    except ValueError:
        return None
    if not isinstance(obj, dict):
        return None
    return obj


def load_fleet(dragnet):
    """Return the set of sensor ids on the roster of one dragnet."""
    sensors = set()
    with open(os.path.join(dragnet, "FLEET.tsv"), "r") as handle:
        rows = handle.read().rstrip("\n").split("\n")
    for row in rows[1:]:
        if row:
            sensors.add(row.split("\t")[0])
    return sensors


def flow_sum(record):
    """Return the check value of a record: section 2's sixteen hex characters."""
    payload = {name: record[name] for name in RECORD_FIELDS}
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("ascii")).hexdigest()[:16]


def render_record(record):
    """Return the one canonical text of a settled flow, without its newline."""
    body = {name: record[name] for name in RECORD_FIELDS}
    body["seq"] = record["seq"]
    body["sum"] = record["sum"]
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


def record_size(record):
    """Return the bytes a settled flow takes in a segment, newline included."""
    return len(render_record(record).encode("ascii")) + 1


def render_report(report):
    """Return the one canonical text of the report, newline included."""
    text = json.dumps(report, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("ascii")


def refusal_row(cause, line, source, text):
    """Return the one canonical row of a file under refused/, newline included."""
    entry = {"cause": cause, "line": line, "source": source, "text": text}
    return json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n"


def discard(root):
    """Remove a directory a restitch consumes; return how many files it held."""
    if not os.path.isdir(root):
        return 0
    held = 0
    for _base, _dirs, files in os.walk(root):
        held += len(files)
    shutil.rmtree(root)
    return held
