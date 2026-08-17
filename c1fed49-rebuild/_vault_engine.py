#!/usr/bin/env python3
"""Reference mender for a crashed Wardline chart vault.

Reads a vault directory, rebuilds the documents the ingest run left unfinished,
files or disposes each one under the retention schedule, and consumes the
evidence it used.  ``VAULT_HANDBOOK.md`` documents the vault layout, the filing
and retention rules and the report; the per-station clock offsets the retention
arithmetic depends on are not written anywhere and have to be mined from the
receipts.
"""

import hashlib
import json
import os
import shutil
import sys

SCHEMA = "wardline-chartvault/v1"

REPORT_NAME = "mend_report.json"
SPOOL_DIR = "spool"
RECEIPT_DIR = "receipts"
FILED_DIR = "filed"
CONSUMED_DIRS = (SPOOL_DIR, RECEIPT_DIR)

REGISTRY_COLUMNS = (
    "doc_id",
    "encounter",
    "title",
    "station",
    "bytes",
    "sha256",
    "retention",
    "gateway_stamp",
)
RECEIPT_COLUMNS = ("stamp", "doc_id", "fragment", "ordinal")

# Retention classes, in days, from the handbook's schedule.
RETENTION_DAYS = {"transient": 30, "standard": 365, "extended": 2555}

MINUTES_PER_DAY = 1440
NO_STATION_SENTINEL = "-"


# --------------------------------------------------------------------------
# vault loading
# --------------------------------------------------------------------------
def _read_table(path):
    """Return the rows of a tab-separated table as dicts keyed by its header."""
    with open(path, "r") as handle:
        text = handle.read()
    lines = [line for line in text.split("\n") if line]
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"))) for line in lines[1:]]


def load_vault(vault_dir):
    """Return ``(charter, registry, receipts, holds, spool)`` for a vault."""
    with open(os.path.join(vault_dir, "vault.json"), "r") as handle:
        charter = json.load(handle)
    registry = []
    for row in _read_table(os.path.join(vault_dir, "registry.tsv")):
        registry.append(
            {
                "doc_id": row["doc_id"],
                "encounter": row["encounter"],
                "title": row["title"],
                "station": row["station"],
                "bytes": int(row["bytes"]),
                "sha256": row["sha256"],
                "retention": row["retention"],
                "gateway_stamp": (
                    None if row["gateway_stamp"] == "-" else int(row["gateway_stamp"])
                ),
            }
        )
    receipts = {}
    receipt_dir = os.path.join(vault_dir, RECEIPT_DIR)
    for name in sorted(os.listdir(receipt_dir)):
        if not name.endswith(".tsv"):
            continue
        station = name[: -len(".tsv")]
        rows = []
        for row in _read_table(os.path.join(receipt_dir, name)):
            rows.append(
                {
                    "stamp": int(row["stamp"]),
                    "doc_id": row["doc_id"],
                    "fragment": row["fragment"],
                    "ordinal": int(row["ordinal"]),
                }
            )
        receipts[station] = rows
    holds = set()
    for row in _read_table(os.path.join(vault_dir, "holds.tsv")):
        holds.add(row["encounter"])
    spool = {}
    spool_dir = os.path.join(vault_dir, SPOOL_DIR)
    for name in sorted(os.listdir(spool_dir)):
        with open(os.path.join(spool_dir, name), "rb") as handle:
            spool[name] = handle.read()
    return charter, registry, receipts, holds, spool


# --------------------------------------------------------------------------
# mining the station clocks
# --------------------------------------------------------------------------
def station_offsets(registry, receipts):
    """Return each station's clock offset in minutes, mined from its receipts.

    A document the intake gateway stamped is an anchor: the gateway stamp is
    true, the station's receipt for that document's first fragment is the same
    instant read off the station's own clock, so their difference is the
    station's offset.  Stations are consistent, so any anchor gives the offset;
    the handbook's declared value is not evidence.
    """
    anchors = dict(
        (row["doc_id"], row["gateway_stamp"])
        for row in registry
        if row["gateway_stamp"] is not None
    )
    offsets = {}
    for station in sorted(receipts):
        found = None
        for row in sorted(receipts[station], key=lambda item: (item["doc_id"], item["ordinal"])):
            if row["ordinal"] != 1 or row["doc_id"] not in anchors:
                continue
            candidate = row["stamp"] - anchors[row["doc_id"]]
            if found is None:
                found = candidate
        offsets[station] = 0 if found is None else found
    return offsets


def corrected_stamp(stamp, offset):
    """Return a station stamp moved back onto the gateway's clock."""
    return stamp - offset


# --------------------------------------------------------------------------
# rebuilding documents
# --------------------------------------------------------------------------
def assemble_from_receipts(entry, receipts, spool):
    """Return the bytes a station's receipts claim for one document, or ``None``.

    Receipts are only usable when they cover the document's fragments from
    ordinal 1 with no gap and every named fragment is still in the spool.
    """
    rows = [
        row
        for station in sorted(receipts)
        for row in receipts[station]
        if row["doc_id"] == entry["doc_id"]
    ]
    if not rows:
        return None
    rows.sort(key=lambda row: row["ordinal"])
    if [row["ordinal"] for row in rows] != list(range(1, len(rows) + 1)):
        return None
    payload = b""
    for row in rows:
        if row["fragment"] not in spool:
            return None
        payload += spool[row["fragment"]]
    return payload


def assemble_by_search(entry, loose, spool):
    """Return the fragments whose concatenation matches the registry digest.

    Fragments the receipts never accounted for are searched by backtracking:
    the document's registered length prunes every partial run that overshoots,
    and a run is only accepted when its digest matches the registry exactly.
    """
    names = sorted(loose)
    wanted = entry["bytes"]
    target = entry["sha256"]
    chosen = []

    def walk(start, size):
        if size == wanted:
            payload = b"".join(spool[name] for name in chosen)
            return hashlib.sha256(payload).hexdigest() == target
        for position in range(start, len(names)):
            name = names[position]
            length = len(spool[name])
            if size + length > wanted:
                continue
            chosen.append(name)
            if walk(position + 1, size + length):
                return True
            chosen.pop()
        return False

    if walk(0, 0):
        return list(chosen)
    return None


# --------------------------------------------------------------------------
# filing names
# --------------------------------------------------------------------------
def filed_name(title):
    """Return the byte-exact filed name of a document title.

    The stem is case-folded; an extension is split at the last dot, except that
    a leading dot never starts one, so ``.private`` files whole.
    """
    dot = title.rfind(".")
    if dot <= 0:
        return title.lower()
    return title[:dot].lower() + "." + title[dot + 1 :].lower()


def collision_suffix(name, taken):
    """Return the name a collision within one encounter is filed under."""
    if name not in taken:
        return name
    dot = name.rfind(".")
    ordinal = 2
    while True:
        if dot <= 0:
            candidate = "%s~%d" % (name, ordinal)
        else:
            candidate = "%s~%d%s" % (name[:dot], ordinal, name[dot:])
        if candidate not in taken:
            return candidate
        ordinal += 1


# --------------------------------------------------------------------------
# the mend
# --------------------------------------------------------------------------
def mend_vault(vault_dir):
    """Mend a vault in place and return the report it should carry."""
    charter, registry, receipts, holds, spool = load_vault(vault_dir)
    as_of = charter["as_of"]
    offsets = station_offsets(registry, receipts)

    claimed = set()
    for station in receipts:
        for row in receipts[station]:
            claimed.add(row["fragment"])
    loose = set(name for name in spool if name not in claimed)

    filed_by_encounter = {}
    consumed = set()
    counters = dict(
        (name, 0)
        for name in (
            "filed",
            "disposed",
            "held",
            "quarantined",
            "rebuilt_from_receipts",
            "rebuilt_by_search",
            "receipt_gaps",
            "digest_failures",
            "collisions",
            "fragments_used",
            "fragments_orphaned",
            "anchors_used",
            "stations_mined",
            "stations_declared_wrong",
        )
    )
    counters["anchors_used"] = sum(
        1 for row in registry if row["gateway_stamp"] is not None
    )
    counters["stations_mined"] = len(offsets)
    counters["stations_declared_wrong"] = sum(
        1
        for station in sorted(offsets)
        if charter["declared_offsets"].get(station) != offsets[station]
    )

    outcomes = []
    for entry in sorted(registry, key=lambda row: row["doc_id"]):
        payload = assemble_from_receipts(entry, receipts, spool)
        route = "receipts"
        if payload is None:
            counters["receipt_gaps"] += 1
            picked = assemble_by_search(entry, loose, spool)
            if picked is None:
                counters["quarantined"] += 1
                outcomes.append((entry["doc_id"], "quarantined", "-"))
                continue
            payload = b"".join(spool[name] for name in picked)
            route = "search"
            for name in picked:
                loose.discard(name)
                consumed.add(name)
        if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            counters["digest_failures"] += 1
            counters["quarantined"] += 1
            outcomes.append((entry["doc_id"], "quarantined", "-"))
            continue
        if route == "receipts":
            counters["rebuilt_from_receipts"] += 1
            for station in sorted(receipts):
                for row in receipts[station]:
                    if row["doc_id"] == entry["doc_id"]:
                        consumed.add(row["fragment"])
        else:
            counters["rebuilt_by_search"] += 1

        stamp = _document_stamp(entry, receipts, offsets)
        due = stamp + RETENTION_DAYS[entry["retention"]] * MINUTES_PER_DAY
        if due <= as_of:
            if entry["encounter"] in holds:
                counters["held"] += 1
                outcome = "held"
            else:
                counters["disposed"] += 1
                outcomes.append((entry["doc_id"], "disposed", "-"))
                continue
        else:
            outcome = "filed"

        taken = filed_by_encounter.setdefault(entry["encounter"], {})
        name = filed_name(entry["title"])
        final = collision_suffix(name, taken)
        if final != name:
            counters["collisions"] += 1
        taken[final] = entry["doc_id"]
        if outcome == "filed":
            counters["filed"] += 1
        _write_filed(vault_dir, entry["encounter"], final, payload)
        outcomes.append((entry["doc_id"], outcome, final))

    counters["fragments_used"] = len(consumed)
    counters["fragments_orphaned"] = len(spool) - len(consumed)

    report = {
        "schema": SCHEMA,
        "vault_id": charter["vault_id"],
        "as_of": as_of,
        "documents": len(registry),
        "station_offsets": dict((station, offsets[station]) for station in sorted(offsets)),
        "outcomes": [
            {"doc_id": doc_id, "outcome": outcome, "filed_as": filed_as}
            for doc_id, outcome, filed_as in sorted(outcomes)
        ],
    }
    report.update(counters)
    return report


def _document_stamp(entry, receipts, offsets):
    """Return the gateway-clock instant a document finished ingesting."""
    if entry["gateway_stamp"] is not None:
        return entry["gateway_stamp"]
    best = None
    for station in sorted(receipts):
        for row in receipts[station]:
            if row["doc_id"] != entry["doc_id"]:
                continue
            moved = corrected_stamp(row["stamp"], offsets[station])
            if best is None or moved > best:
                best = moved
    return 0 if best is None else best


def _write_filed(vault_dir, encounter, name, payload):
    """Write one rebuilt document into the vault's filed tree."""
    target = os.path.join(vault_dir, FILED_DIR, encounter)
    os.makedirs(target, exist_ok=True)
    with open(os.path.join(target, name), "wb") as handle:
        handle.write(payload)


def canonical_json(report):
    """Return the canonical byte encoding of the mend report."""
    text = json.dumps(report, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("ascii")


def consume_evidence(vault_dir):
    """Take the spool and the receipts away once the mend has filed everything."""
    for name in CONSUMED_DIRS:
        shutil.rmtree(os.path.join(vault_dir, name))


def mend_dir(vault_dir):
    """Mend a vault directory and return the report bytes it was left holding."""
    report = mend_vault(vault_dir)
    payload = canonical_json(report)
    with open(os.path.join(vault_dir, REPORT_NAME), "wb") as handle:
        handle.write(payload)
    consume_evidence(vault_dir)
    return payload


def main(argv):
    """Mend the vault directory named on the command line."""
    if len(argv) != 2:
        sys.stderr.write("usage: chart_mend.py <vault_dir>\n")
        return 2
    mend_dir(argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
