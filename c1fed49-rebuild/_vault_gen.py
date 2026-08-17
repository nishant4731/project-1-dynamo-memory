"""Deterministic builder for crashed Wardline chart vaults.

Every vault the verifier grades -- the shipped one, the held-out ones and the
submission-shaped one -- is built here from a fixed integer seed.  Nothing in
this module reaches the agent's container: Harbor overlays ``tests/`` at
``/tests`` only at verify time.
"""

import hashlib
import json
import os
import random

import _vault_engine as engine

STATIONS = ("ST-1", "ST-2", "ST-3", "ST-4")
RETENTIONS = ("transient", "standard", "extended")
TITLE_STEMS = (
    "Discharge Summary",
    "Operative Note",
    "Radiology Report",
    "Pathology Report",
    "Consult Note",
    "Medication List",
    "Consent Form",
    "Progress Note",
)
EXTENSIONS = (".pdf", ".PDF", ".txt", ".tif")

DAY = engine.MINUTES_PER_DAY


def _content(rng, size):
    """Return deterministic document bytes of a given size."""
    return bytes(rng.randrange(32, 127) for _ in range(size))


def build_vault(vault_id, seed, encounters, documents, as_of_day):
    """Return the whole description of one vault before it is written out."""
    rng = random.Random(seed)
    offsets = {}
    for station in STATIONS:
        offsets[station] = rng.choice((-311, -137, -43, 0, 43, 137, 311, 509))
    as_of = as_of_day * DAY

    encounter_ids = ["E-%02d" % (index + 1) for index in range(encounters)]
    docs = []
    for index in range(documents):
        stem = rng.choice(TITLE_STEMS)
        title = stem.replace(" ", "_") + rng.choice(EXTENSIONS)
        if index % 17 == 5:
            title = "." + stem.replace(" ", "_").lower()
        if index % 23 == 7:
            title = stem.replace(" ", "_") + ".v2" + rng.choice(EXTENSIONS)
        size = rng.choice((180, 240, 320, 420, 560, 700, 880))
        docs.append(
            {
                "doc_id": "D-%04d" % (index + 1),
                "encounter": rng.choice(encounter_ids),
                "title": title,
                "station": rng.choice(STATIONS),
                "retention": rng.choice(RETENTIONS),
                "bytes": size,
                "age_days": rng.choice((3, 20, 40, 120, 300, 400, 900, 2600, 3000)),
            }
        )

    # deliberate collisions: three documents of one encounter share a title
    if len(docs) >= 6:
        for slot in (1, 3, 5):
            docs[slot]["encounter"] = encounter_ids[0]
            docs[slot]["title"] = "Discharge_Summary.pdf"
    # a leading-dot title and a two-dot title inside the collision encounter
    if len(docs) >= 8:
        docs[6]["encounter"] = encounter_ids[0]
        docs[6]["title"] = ".discharge_summary"
        docs[7]["encounter"] = encounter_ids[0]
        docs[7]["title"] = "Discharge_Summary.v2.pdf"

    holds = set()
    for encounter in encounter_ids:
        if rng.random() < 0.25:
            holds.add(encounter)

    return _populate(rng, vault_id, as_of, offsets, docs, encounter_ids, holds)


def _populate(rng, vault_id, as_of, offsets, docs, encounter_ids, holds):
    """Fill in fragments, receipts, anchors and the crash damage."""
    spool = {}
    receipts = dict((station, []) for station in STATIONS)
    registry = []
    counter = [0]

    def next_fragment():
        counter[0] += 1
        return "f%04d.part", counter[0]

    for position, doc in enumerate(docs):
        payload = _content(rng, doc["bytes"])
        pieces = rng.choice((1, 2, 2, 3, 4))
        cuts = sorted(rng.sample(range(1, doc["bytes"]), pieces - 1)) if pieces > 1 else []
        bounds = [0] + cuts + [doc["bytes"]]
        fragments = []
        for index in range(pieces):
            template, number = next_fragment()
            name = template % number
            spool[name] = payload[bounds[index] : bounds[index + 1]]
            fragments.append(name)

        true_stamp = as_of - doc["age_days"] * DAY - rng.randrange(0, DAY)
        station = doc["station"]
        anchored = position % 3 == 0
        # every station keeps at least one anchor so its offset is mineable
        registry.append(
            {
                "doc_id": doc["doc_id"],
                "encounter": doc["encounter"],
                "title": doc["title"],
                "station": station,
                "bytes": doc["bytes"],
                "sha256": hashlib.sha256(payload).hexdigest(),
                "retention": doc["retention"],
                "gateway_stamp": true_stamp if anchored else None,
                "_fragments": fragments,
                "_true_stamp": true_stamp,
            }
        )
        for ordinal, name in enumerate(fragments, start=1):
            receipts[station].append(
                {
                    "stamp": true_stamp + offsets[station],
                    "doc_id": doc["doc_id"],
                    "fragment": name,
                    "ordinal": ordinal,
                }
            )

    _ensure_anchor_per_station(registry, receipts)
    gaps = _open_receipt_gaps(rng, registry, receipts)
    damaged = _damage_fragments(rng, registry, spool, gaps)
    _add_orphans(rng, spool, counter)

    charter = {
        "vault_id": vault_id,
        "as_of": as_of,
        "declared_offsets": _declared(rng, offsets),
    }
    return charter, registry, receipts, holds, spool, offsets, gaps, damaged


def _ensure_anchor_per_station(registry, receipts):
    """Give every station an anchor document, so its offset is recoverable."""
    for station in STATIONS:
        has_anchor = any(
            row["gateway_stamp"] is not None
            and any(
                item["doc_id"] == row["doc_id"] and item["ordinal"] == 1
                for item in receipts[station]
            )
            for row in registry
        )
        if has_anchor:
            continue
        for row in registry:
            if row["station"] == station:
                row["gateway_stamp"] = row["_true_stamp"]
                break


def _open_receipt_gaps(rng, registry, receipts):
    """Drop receipt rows for some documents, so their fragments must be searched.

    Only anchored documents lose their receipts, so a searched document still has
    an instant on the gateway clock and can be filed or disposed on its merits;
    and every station keeps one anchored document whose receipts survive, so its
    offset stays mineable.
    """
    spared = {}
    for row in sorted(registry, key=lambda item: item["doc_id"]):
        if row["gateway_stamp"] is not None:
            spared.setdefault(row["station"], row["doc_id"])
    candidates = [
        row
        for row in registry
        if row["gateway_stamp"] is not None and spared.get(row["station"]) != row["doc_id"]
    ]
    rng.shuffle(candidates)
    gaps = []
    for row in candidates[: max(3, len(registry) // 7)]:
        station = row["station"]
        receipts[station] = [
            item for item in receipts[station] if item["doc_id"] != row["doc_id"]
        ]
        gaps.append(row["doc_id"])
    return sorted(gaps)


def _damage_fragments(rng, registry, spool, gaps):
    """Corrupt one fragment of a receipt-covered document, so its digest fails."""
    damaged = []
    for row in registry:
        if row["doc_id"] in gaps:
            continue
        if len(damaged) >= 2:
            break
        if rng.random() < 0.35 and row["_fragments"]:
            name = row["_fragments"][-1]
            blob = spool[name]
            if blob:
                spool[name] = bytes((blob[0] ^ 0x5A,)) + blob[1:]
                damaged.append(row["doc_id"])
    return damaged


def _add_orphans(rng, spool, counter):
    """Leave a few fragments in the spool that belong to no registered document."""
    for _ in range(rng.choice((2, 3, 4))):
        counter[0] += 1
        spool["f%04d.part" % counter[0]] = _content(rng, rng.choice((90, 150, 210)))


def _declared(rng, offsets):
    """Return the handbook's declared offsets, wrong for two stations."""
    declared = dict(offsets)
    wrong = rng.sample(sorted(offsets), 2)
    for station in wrong:
        declared[station] = offsets[station] + rng.choice((-120, -60, 60, 120))
    return declared


# --------------------------------------------------------------------------
# writing a vault out
# --------------------------------------------------------------------------
def write_vault(target_dir, charter, registry, receipts, holds, spool):
    """Materialise one crashed vault on disk."""
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "vault.json"), "w") as handle:
        json.dump(charter, handle, indent=2, sort_keys=True)
        handle.write("\n")
    lines = ["\t".join(engine.REGISTRY_COLUMNS)]
    for row in registry:
        lines.append(
            "\t".join(
                [
                    row["doc_id"],
                    row["encounter"],
                    row["title"],
                    row["station"],
                    str(row["bytes"]),
                    row["sha256"],
                    row["retention"],
                    "-" if row["gateway_stamp"] is None else str(row["gateway_stamp"]),
                ]
            )
        )
    with open(os.path.join(target_dir, "registry.tsv"), "w") as handle:
        handle.write("\n".join(lines) + "\n")

    receipt_dir = os.path.join(target_dir, engine.RECEIPT_DIR)
    os.makedirs(receipt_dir, exist_ok=True)
    for station in sorted(receipts):
        rows = sorted(receipts[station], key=lambda item: (item["doc_id"], item["ordinal"]))
        lines = ["\t".join(engine.RECEIPT_COLUMNS)]
        for row in rows:
            lines.append(
                "\t".join(
                    [str(row["stamp"]), row["doc_id"], row["fragment"], str(row["ordinal"])]
                )
            )
        with open(os.path.join(receipt_dir, "%s.tsv" % station), "w") as handle:
            handle.write("\n".join(lines) + "\n")

    lines = ["encounter"]
    for encounter in sorted(holds):
        lines.append(encounter)
    with open(os.path.join(target_dir, "holds.tsv"), "w") as handle:
        handle.write("\n".join(lines) + "\n")

    spool_dir = os.path.join(target_dir, engine.SPOOL_DIR)
    os.makedirs(spool_dir, exist_ok=True)
    for name in sorted(spool):
        with open(os.path.join(spool_dir, name), "wb") as handle:
            handle.write(spool[name])



# --------------------------------------------------------------------------
# the graded corpus
# --------------------------------------------------------------------------
# name, seed, encounters, documents, as_of day
VAULT_SPECS = (
    ("live-vault", 311001, 7, 34, 4000),
    ("example-vault", 322002, 3, 9, 3800),
    ("held-wide", 333003, 9, 44, 4200),
    ("held-narrow", 344004, 4, 18, 3900),
    ("held-old", 355005, 6, 30, 5200),
    ("held-fresh", 366006, 6, 28, 3600),
    ("held-held", 377007, 5, 24, 4100),
    ("held-single", 388008, 2, 8, 4000),
    ("held-dense", 399009, 3, 40, 4300),
    ("sweep-probe", 411011, 6, 26, 4050),
)

VAULTS = dict((spec[0], spec) for spec in VAULT_SPECS)


def materialise(target_dir, spec):
    """Build and write one vault of the graded corpus."""
    charter, registry, receipts, holds, spool, offsets, gaps, damaged = build_vault(*spec)
    write_vault(target_dir, charter, registry, receipts, holds, spool)
    return offsets, gaps, damaged


def build_salted(salt):
    """Return a vault specification derived from a submission digest."""
    return (
        "salt-%08x" % (salt & 0xFFFFFFFF),
        500000 + (salt % 300000),
        4 + salt % 5,
        16 + (salt // 3) % 20,
        3700 + salt % 900,
    )
