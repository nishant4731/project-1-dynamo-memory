"""Grade the dragnet restitch.

Every expected byte comes from a reference that exists only in the verifier
overlay and restitches its own pristine copies of each crashed dragnet.  The
submitted ``/app/dragnet_restitch.py`` is then re-run -- root dropped, overlay
sealed -- against a fresh crash of the live dragnet, eleven dragnets it has
never seen and one built from its own digest, and each restitched tree is
compared file by file and directory by directory.
"""

import hashlib
import json
import os
import shutil
import tempfile

import pytest

import _dragnet_engine as engine
import _dragnet_rig as rig


# ------------------------------------------------------------- what was handed in
def test_the_program_sits_at_the_declared_path():
    """/app/dragnet_restitch.py is a real file, not a symlink, and holds code."""
    assert len(rig.submitted_program()) > 400, "the submitted program is too small"


def test_no_graded_path_is_reached_through_a_symlink():
    """Every path grading reads resolves to itself, component by component."""
    rig.guard_graded_paths()
    for path in rig.GRADED_FILES + rig.GRADED_DIRS:
        assert os.path.realpath(path) == path, (
            "%s resolves to %s" % (path, os.path.realpath(path)))
    rig.guard_tree(rig.LIVE_STORE)


def test_a_symlinked_graded_path_is_refused_rather_than_followed():
    """The guard rejects a link at the leaf, above it, and inside the tree."""
    work = tempfile.mkdtemp(prefix="dragnet-link-")
    try:
        real = os.path.join(work, "real")
        os.makedirs(os.path.join(real, "segments"))
        with open(os.path.join(real, "segments", "0001.jsonl"), "w") as handle:
            handle.write("{}\n")
        leaf = os.path.join(work, "leaf.jsonl")
        os.symlink(os.path.join(real, "segments", "0001.jsonl"), leaf)
        with pytest.raises(AssertionError):
            rig.guard_path(leaf, work)
        above = os.path.join(work, "above")
        os.symlink(real, above)
        with pytest.raises(AssertionError):
            rig.guard_path(os.path.join(above, "segments", "0001.jsonl"), work)
        with pytest.raises(AssertionError):
            rig.guard_tree(above, work)
        inside = os.path.join(real, "segments", "0002.jsonl")
        os.symlink(os.path.join(real, "segments", "0001.jsonl"), inside)
        with pytest.raises(AssertionError):
            rig.guard_tree(real, work)
        os.remove(inside)
        assert rig.guard_tree(real, work) == real, (
            "the guard rejects a tree that holds no link at all")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def test_the_live_dragnet_was_restitched_in_place():
    """/app/data/dragnet is exactly what a correct restitch leaves behind."""
    rig.guard_graded_paths()
    expected, _report = rig.reference_tree(rig.LIVE_ID)
    problem = rig.tree_problem(expected, rig.tree_digest(rig.LIVE_STORE),
                               "/app/data/dragnet")
    assert problem is None, problem


def test_the_live_report_describes_that_restitch():
    """restitch_report.json in the live dragnet carries the reference counts."""
    _tree, report = rig.reference_tree(rig.LIVE_ID)
    parsed = rig.strict_load(rig.read_guarded(rig.DECLARED_REPORT))
    problem = rig.typed_diff(report, parsed)
    assert problem is None, problem


def test_the_live_dragnet_spent_its_evidence():
    """The inbox and the scratch directory are gone from the live dragnet."""
    for name in ("inbox", "scratch"):
        assert not os.path.exists(os.path.join(rig.LIVE_STORE, name)), (
            "%s survived the restitch of the live dragnet" % name)


def test_the_read_only_material_is_untouched():
    """The charter and the sensor roster still hash to what shipped."""
    pins = rig.frozen_pins()
    assert hashlib.sha256(rig.read_guarded(rig.CHARTER)).hexdigest() == pins["charter"], (
        "DRAGNET_CHARTER.md was modified during the agent run")
    roster = rig.read_guarded(os.path.join(rig.LIVE_STORE, "FLEET.tsv"))
    assert hashlib.sha256(roster).hexdigest() == pins["fleet"], (
        "the live dragnet's FLEET.tsv was modified")


def test_the_shipped_dragnet_is_the_one_the_builder_lays_down():
    """The crashed dragnet in the image is exactly what the builder produces."""
    pins = rig.frozen_pins()
    assert rig.crashed_digest(rig.LIVE_ID) == pins["crashed_live"], (
        "the dragnet frozen into the image is not what the builder now produces")


def test_the_format_sheet_quotes_what_the_reference_writes():
    """Every fragment the charter shows is a real line the reference produces."""
    held = rig.reference_artifacts(rig.SHEET_ID)
    pool = set()
    for body in held["segments"].values():
        pool.update(body.decode("ascii").rstrip("\n").split("\n"))
    for name in ("CONTACT.tsv", "REACH.tsv", "PIVOT.tsv"):
        pool.update(held[name].rstrip("\n").split("\n"))
    for body in held["refused"].values():
        pool.update(body.rstrip("\n").split("\n"))
    stray = [line for line in rig.charter_fragments() if line not in pool]
    assert not stray, "the format sheet quotes lines the reference never wrote: %s" % stray


def test_every_decisive_value_is_quoted_in_the_agent_visible_charter():
    """Each value the reference grades by appears verbatim in DRAGNET_CHARTER.md."""
    charter = rig.read_guarded(rig.CHARTER).decode("utf-8")
    cited = {
        "segment record bound": str(engine.SEGMENT_CAPACITY),
        "segment byte bound": str(engine.SEGMENT_BYTE_BUDGET),
        "label limit": str(engine.LABEL_LIMIT),
        "relay window": str(engine.RELAY_WINDOW),
        "lowest port": str(engine.PORT_LOW),
        "highest port": str(engine.PORT_HIGH),
        "canonical dump": 'sort_keys=True, separators=(",", ":")',
        "check-value width": "sixteen",
    }
    for name, value in engine.__dict__.items():
        if name in ("STATES", "OPERATIONS", "CAUSES"):
            for member in value:
                cited["%s %s" % (name.lower(), member)] = member
    for column in engine.CONTACT_COLUMNS + engine.REACH_COLUMNS + engine.FLEET_COLUMNS:
        cited["column %s" % column] = column
    for key in engine.REPORT_KEYS:
        cited["counter %s" % key] = key
    for field in engine.RECORD_FIELDS + ("seq", "sum"):
        cited["field %s" % field] = field
    missing = sorted(name for name, value in cited.items() if value not in charter)
    assert not missing, (
        "the charter never states what the reference grades by: %s" % missing)
    sifting = charter[charter.index("## 3. Sifting"):charter.index("## 4.")]
    order = sorted(engine.CAUSES, key=lambda cause: sifting.index("`%s`" % cause))
    assert order == list(engine.CAUSES), (
        "the charter tries the causes in a different order than the reference: %s"
        % order)
    flat = " ".join(charter.split())
    for rule in ("the lowest `fid` among those settles a tie",
                 "the lowest host id settling a tie",
                 "equal `first` by ascending `fid`",
                 "two operations with the same `seq` are applied in file-name order",
                 "compare as text, character by character"):
        assert rule in flat, "the charter does not state the tie-break: %r" % rule


def test_the_charter_states_the_payload_the_check_value_covers():
    """The eleven keys the sum is taken over are the ones the charter lists."""
    charter = rig.read_guarded(rig.CHARTER).decode("utf-8")
    section = " ".join(
        charter[charter.index("The **check value**"):charter.index("## 3.")].split())
    quoted = [field for field in engine.RECORD_FIELDS if "`%s`" % field in section]
    assert quoted == list(engine.RECORD_FIELDS), (
        "the charter's canonical payload is not the reference's: %s" % quoted)
    for absent in ("seq", "sum"):
        assert "without `%s`" % absent in section, (
            "the charter does not say the payload leaves out %s" % absent)


def test_the_supplied_plumbing_is_untouched_and_agrees_with_the_reference():
    """/app/dragnet_io.py still hashes to what shipped and renders as we grade."""
    pins = rig.frozen_pins()
    assert hashlib.sha256(rig.read_guarded(rig.HELPER)).hexdigest() == pins["helper"], (
        "/app/dragnet_io.py was modified during the agent run")
    supplied = rig.supplied_plumbing()
    assert tuple(supplied["RECORD_FIELDS"]) == engine.RECORD_FIELDS, (
        "the supplied plumbing names a different payload than the charter")
    checked = 0
    for slot in (rig.LIVE_ID,) + rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        for body in held["segments"].values():
            for line in body.decode("ascii").rstrip("\n").split("\n"):
                record = json.loads(line)
                assert supplied["flow_sum"](record) == record["sum"], (
                    "the supplied check value disagrees with a settled record")
                assert supplied["render_record"](record) == line, (
                    "the supplied record rendering disagrees with a settled record")
                checked += 1
        for name, body in held["refused"].items():
            for line in body.rstrip("\n").split("\n"):
                entry = json.loads(line)
                assert supplied["refusal_row"](
                    entry["cause"], entry["line"], entry["source"],
                    entry["text"]) == line + "\n", (
                    "the supplied refusal row disagrees with %s" % name)
    assert checked > 200, "too few settled records cross-checked the plumbing"


def test_no_protected_material_reached_the_agent_image():
    """Nothing under /app/data names a held-out dragnet or a reference module."""
    hits = rig.scan_for_leaks()
    assert not hits, "protected material readable by the agent: %s" % hits[:5]


# --------------------------------------------------------------- the program runs
def test_the_program_restitches_a_fresh_crash_of_the_live_dragnet():
    """Run again on a pristine crash of the live dragnet, it reproduces it."""
    run = rig.graded_run(rig.LIVE_ID)
    problem = rig.tree_problem(run["expected"], run["actual"], rig.LIVE_ID)
    assert problem is None, problem


@pytest.mark.parametrize("slot", rig.HELD_OUT)
def test_the_program_restitches_a_dragnet_it_has_never_seen(slot):
    """The program restitches a crashed dragnet it was never shown."""
    run = rig.graded_run(slot)
    problem = rig.tree_problem(run["expected"], run["actual"], slot)
    assert problem is None, problem


def test_the_program_restitches_a_dragnet_derived_from_itself():
    """A dragnet keyed to the submission's own digest is restitched correctly."""
    run = rig.graded_run("salted")
    problem = rig.tree_problem(run["expected"], run["actual"], "salted")
    assert problem is None, problem


@pytest.mark.parametrize("slot", rig.SETTLED)
def test_a_second_restitch_settles(slot):
    """Restitching a restitched dragnet touches no segment, index or reach row."""
    first, second = rig.settled_run(slot)
    reference, _settled = rig.reference_settled(slot)
    problem = rig.tree_problem(rig.stable_part(reference), rig.stable_part(first),
                               "%s (first restitch)" % slot)
    assert problem is None, problem
    problem = rig.tree_problem(rig.stable_part(first), rig.stable_part(second),
                               "%s (second restitch)" % slot)
    assert problem is None, problem


def test_the_reference_settles_after_one_restitch():
    """The settling rule the charter states is true of the reference itself."""
    for slot in rig.SETTLED:
        first, settled = rig.reference_settled(slot)
        problem = rig.tree_problem(rig.stable_part(first), rig.stable_part(settled),
                                   "%s (reference)" % slot)
        assert problem is None, problem
        assert rig.stable_part(first), "%s has no settling surface to grade" % slot


# ------------------------------------------------------------ dragnet invariants
def test_the_live_dragnet_holds_the_declared_shape():
    """Segments are named and bounded as the charter says and the index agrees."""
    root = rig.LIVE_STORE
    segment_dir = os.path.join(root, "segments")
    names = sorted(os.listdir(segment_dir)) if os.path.isdir(segment_dir) else []
    assert names == ["%04d.jsonl" % (n + 1) for n in range(len(names))], (
        "the segments are not named 0001.jsonl upward: %s" % names[:4])
    bodies = {}
    for name in names:
        with open(os.path.join(segment_dir, name), "rb") as handle:
            bodies[name] = handle.read()
        lines = bodies[name].rstrip(b"\n").split(b"\n")
        assert bodies[name].endswith(b"\n"), "%s does not end with a newline" % name
        assert len(lines) <= engine.SEGMENT_CAPACITY, (
            "%s holds more than %d records" % (name, engine.SEGMENT_CAPACITY))
        assert (len(bodies[name]) <= engine.SEGMENT_BYTE_BUDGET or len(lines) == 1), (
            "%s is over the %d byte budget" % (name, engine.SEGMENT_BYTE_BUDGET))
    index = rig.read_guarded(rig.DECLARED_CONTACT).decode("ascii")
    rows = [line.split("\t") for line in index.rstrip("\n").split("\n")]
    assert rows[0] == list(engine.CONTACT_COLUMNS), "the CONTACT.tsv header is wrong"
    previous = None
    for row in rows[1:]:
        assert len(row) == len(engine.CONTACT_COLUMNS), "index row width: %s" % row
        fid, segment, offset, src, dst, state, first, last = row
        assert segment in bodies, "the index names a segment that is not there: %s" % segment
        line = bodies[segment][int(offset):].split(b"\n", 1)[0].decode("ascii")
        record = json.loads(line)
        assert record["fid"] == fid, (
            "the byte offset recorded for %s lands on another record" % fid)
        for name, shown in (("src", src), ("dst", dst), ("state", state),
                            ("first", first), ("last", last)):
            assert str(record[name]) == shown, "the index %s disagrees for %s" % (name, fid)
        if previous is not None:
            assert (int(previous[6]), previous[0]) <= (int(first), fid), (
                "the index is not ordered by rising first then rising fid")
        previous = row


def test_the_reach_table_agrees_with_the_contacts_beside_it():
    """REACH.tsv's own identities hold against CONTACT.tsv and the report."""
    rows = [line.split("\t") for line in
            rig.read_guarded(rig.DECLARED_REACH).decode("ascii").rstrip("\n").split("\n")]
    assert rows[0] == list(engine.REACH_COLUMNS), "the REACH.tsv header is wrong"
    index = [line.split("\t") for line in
             rig.read_guarded(rig.DECLARED_CONTACT).decode("ascii").rstrip("\n").split("\n")][1:]
    contacts = [row for row in index if row[5] == "closed"]
    report = rig.strict_load(rig.read_guarded(rig.DECLARED_REPORT))
    origins = [row[0] for row in rows[1:]]
    assert origins == sorted(origins), "REACH.tsv is not in ascending host order"
    assert origins == sorted({row[3] for row in contacts}), (
        "REACH.tsv does not carry exactly the hosts that opened a contact")
    assert report["reach_origins"] == len(origins), "reach_origins disagrees with REACH.tsv"
    assert report["contacts"] == len(contacts), "contacts disagrees with CONTACT.tsv"
    assert report["reach_pairs"] == sum(int(row[1]) for row in rows[1:]), (
        "reach_pairs is not the reach column added up")
    reachable = {row[0] for row in contacts} | {row[4] for row in contacts}
    for origin, reach, horizon, farthest in rows[1:]:
        assert 1 <= int(reach) <= len(reachable), "%s: reach out of range" % origin
        assert farthest in reachable, "%s: farthest names no host of the graph" % origin
        assert int(horizon) <= max(int(row[7]) for row in contacts), (
            "%s: horizon is later than any contact ends" % origin)


def test_the_pivot_table_is_the_reach_table_read_backwards():
    """PIVOT.tsv's own identities hold against REACH.tsv and CONTACT.tsv."""
    pivot = [line.split("\t") for line in
             rig.read_guarded(rig.DECLARED_PIVOT).decode("ascii").rstrip("\n").split("\n")]
    assert pivot[0] == list(engine.PIVOT_COLUMNS), "the PIVOT.tsv header is wrong"
    index = [line.split("\t") for line in
             rig.read_guarded(rig.DECLARED_CONTACT).decode("ascii").rstrip("\n").split("\n")][1:]
    contacts = [row for row in index if row[5] == "closed"]
    report = rig.strict_load(rig.read_guarded(rig.DECLARED_REPORT))
    targets = [row[0] for row in pivot[1:]]
    assert targets == sorted(targets), "PIVOT.tsv is not in ascending host order"
    assert targets == sorted({row[4] for row in contacts}), (
        "PIVOT.tsv does not carry exactly the hosts a contact arrives at")
    assert report["pivot_targets"] == len(targets), "pivot_targets disagrees with PIVOT.tsv"
    assert report["pivot_pairs"] == sum(int(row[1]) for row in pivot[1:]), (
        "pivot_pairs is not the sources column added up")
    # the two tables count the same pairs, read from opposite ends
    assert report["pivot_pairs"] == report["reach_pairs"], (
        "the pivot totals disagree with the reach totals: %d vs %d"
        % (report["pivot_pairs"], report["reach_pairs"]))
    hosts = {row[3] for row in contacts} | {row[4] for row in contacts}
    opens = [int(row[6]) for row in contacts]
    for target, sources, opened, origin in pivot[1:]:
        assert 1 <= int(sources) <= len(hosts), "%s: sources out of range" % target
        assert origin in hosts, "%s: origin names no host of the graph" % target
        assert min(opens) <= int(opened) <= max(opens), (
            "%s: opened is not the first of any contact" % target)


def test_the_refused_files_are_named_as_the_charter_says():
    """Turned-away lines are filed under their source's name, with ordinals."""
    refused = os.path.join(rig.LIVE_STORE, "refused")
    assert os.path.isdir(refused), "the live dragnet has no refused/ directory"
    names = sorted(os.listdir(refused))
    report = rig.strict_load(rig.read_guarded(rig.DECLARED_REPORT))
    assert len(names) == report["refused_files_written"], (
        "refused/ holds %d files but the report claims %d"
        % (len(names), report["refused_files_written"]))
    filed = 0
    for name in names:
        assert name.endswith(".rej"), "unexpected file under refused/: %s" % name
        for line in rig.read_guarded(os.path.join(refused, name)).decode("ascii").split("\n"):
            if not line:
                continue
            entry = json.loads(line)
            assert sorted(entry) == ["cause", "line", "source", "text"], (
                "a refusal row carries the wrong keys: %s" % sorted(entry))
            assert entry["cause"] in engine.CAUSES, "unknown cause %r" % entry["cause"]
            filed += 1
    assert filed == report["lines_refused"], (
        "refused/ holds %d rows but the report claims %d" % (filed, report["lines_refused"]))
    assert report["refused_files_ordinalled"] >= 1, (
        "no refused file needed an ordinal in the live dragnet")


def test_both_segment_bounds_bind_across_the_graded_dragnets():
    """Some segment is closed by the record bound and some by the byte bound."""
    by_count = 0
    by_bytes = 0
    for slot in (rig.LIVE_ID,) + rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        names = sorted(held["segments"])
        for name in names[:-1]:
            lines = held["segments"][name].rstrip(b"\n").split(b"\n")
            if len(lines) == engine.SEGMENT_CAPACITY:
                by_count += 1
            else:
                by_bytes += 1
    assert by_count, "no segment is ever closed by the record bound"
    assert by_bytes, "no segment is ever closed by the byte bound"


def test_the_graded_dragnets_exercise_every_counter():
    """Across the graded corpus no counter the report carries stays trivial."""
    totals = {}
    for slot in (rig.LIVE_ID,) + rig.HELD_OUT:
        _tree, report = rig.reference_tree(slot)
        for key, value in report.items():
            totals[key] = totals.get(key, 0) + value
    thin = {key: totals.get(key, 0) for key in engine.REPORT_KEYS
            if totals.get(key, 0) < 4}
    assert not thin, "the graded corpus is too thin for %s" % thin


def test_every_rejection_cause_is_witnessed_by_a_planted_line():
    """Each of the six causes turns a line away somewhere in the graded corpus."""
    seen = dict.fromkeys(engine.CAUSES, 0)
    for slot in (rig.LIVE_ID,) + rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        for body in held["refused"].values():
            for line in body.rstrip("\n").split("\n"):
                seen[json.loads(line)["cause"]] += 1
    missing = [cause for cause in engine.CAUSES if seen[cause] < 2]
    assert not missing, "no graded dragnet exercises %s" % missing


def test_every_inclusive_bound_sits_on_a_planted_record():
    """A settled flow sits on each edge the charter states inclusively."""
    seen = {"sport_low": 0, "dport_high": 0, "one_byte": 0, "one_packet": 0,
            "zero_seq": 0, "full_label": 0, "brimful_segment": 0,
            "amend_on_the_instant": 0}
    for slot in rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        for name, body in held["segments"].items():
            if len(body) == engine.SEGMENT_BYTE_BUDGET:
                seen["brimful_segment"] += 1
            for line in body.decode("ascii").rstrip("\n").split("\n"):
                record = json.loads(line)
                seen["sport_low"] += record["sport"] == engine.PORT_LOW
                seen["dport_high"] += record["dport"] == engine.PORT_HIGH
                seen["one_byte"] += record["bytes"] == 1
                seen["one_packet"] += record["pkts"] == 1
                seen["zero_seq"] += record["seq"] == 0
                seen["full_label"] += len(record["label"]) == engine.LABEL_LIMIT
        _tree, report = rig.reference_tree(slot)
        seen["amend_on_the_instant"] += report["amends_incoherent"] > 0
    missing = sorted(key for key, count in seen.items() if count < 1)
    assert not missing, "no graded dragnet sits on the bound for %s" % missing


def test_a_merge_group_disagrees_about_its_label():
    """Two observations of one flow carry different labels somewhere in the corpus.

    Section 5 says whose `label` carries.  If every co-observation agreed on it
    the rule would be inert, and a reading that took the lowest `fid`'s label
    instead would be indistinguishable from the one the charter states.
    """
    seen = 0
    for slot in rig.HELD_OUT:
        plan = rig.plan_for(slot)
        groups = {}
        for holder in ("segments", "inbox"):
            for _name, lines in sorted(plan.get(holder, {}).items()):
                for line in lines:
                    try:
                        record = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(record, dict):
                        continue
                    if record.get("op") in ("amend", "retract"):
                        continue
                    if not isinstance(record.get("label"), str):
                        continue
                    key = tuple(record.get(name) for name in
                                ("src", "dst", "sport", "dport", "first"))
                    if any(part is None for part in key):
                        continue
                    groups.setdefault(key, set()).add(record["label"])
        seen += sum(1 for labels in groups.values() if len(labels) > 1)
    assert seen > 0, (
        "no graded dragnet holds a merge group whose observations disagree "
        "about `label`, so section 5's provenance for it is never exercised")


def test_the_duplicate_rule_is_witnessed_inside_the_inbox_too():
    """A held-out dragnet refuses an admit whose fid an earlier admit took.

    Every other planted twin duplicates a record the segments already held, so
    without this the reading "the duplicate rule only guards the segments" is
    never exercised anywhere in the graded corpus.
    """
    seen = 0
    for slot in rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        admitted = set()
        for name in sorted(held["refused"]):
            for line in held["refused"][name].rstrip("\n").split("\n"):
                row = json.loads(line)
                if row["cause"] != "duplicate_id" or not row["source"].startswith("inbox/"):
                    continue
                fid = json.loads(row["text"])["fid"]
                # the fid it duplicates must not be one the segments carried
                if any(fid in body.decode("ascii") for body in held["segments"].values()):
                    continue
                admitted.add(fid)
        seen += len(admitted)
    assert seen > 0, (
        "no graded dragnet refuses an inbox admit whose fid only an earlier "
        "inbox admit had taken; the duplicate rule is unwitnessed across the sift")


def test_every_bound_is_also_witnessed_from_just_outside_it():
    """A turned-away line sits one step outside each bound, not only on it."""
    outside = {
        "port_below_low": lambda r: r.get("sport") == engine.PORT_LOW - 1,
        "port_above_high": lambda r: r.get("dport") == engine.PORT_HIGH + 1,
        "no_bytes": lambda r: r.get("bytes") == 0,
        "no_packets": lambda r: r.get("pkts") == 0,
        "sequence_below_zero": lambda r: r.get("seq") == -1,
        "window_not_open": lambda r: r.get("last") == r.get("first"),
        "label_over_the_limit":
            lambda r: len(str(r.get("label", ""))) == engine.LABEL_LIMIT + 1,
        "sum_one_short": lambda r: len(str(r.get("sum", ""))) == 15,
        "sum_not_lowercase":
            lambda r: str(r.get("sum", "")) != str(r.get("sum", "")).lower(),
        "fid_wrong_width": lambda r: str(r.get("fid", "")) == "f-0123",
        "host_not_all_digits": lambda r: str(r.get("src", "")) == "h-a04",
    }
    seen = dict.fromkeys(outside, 0)
    for slot in rig.HELD_OUT:
        held = rig.reference_artifacts(slot)
        for body in held["refused"].values():
            for line in body.rstrip("\n").split("\n"):
                try:
                    record = json.loads(json.loads(line)["text"])
                except ValueError:
                    continue
                if not isinstance(record, dict):
                    continue
                for name, holds in outside.items():
                    try:
                        seen[name] += bool(holds(record))
                    except TypeError:
                        pass
    missing = sorted(name for name, count in seen.items() if count < 1)
    assert not missing, "no graded dragnet turns a line away just outside %s" % missing


# ---------------------------------------------------------------- verifier rigour
def test_single_rule_probes_of_the_reference_are_all_rejected():
    """Every one-rule change to the reference leaves a dragnet we reject."""
    source = rig.engine_source()
    answers = rig.sweep_answers()
    built = 0
    survivors = []
    thin = []
    for name, old, new in rig.PROBES:
        probe = rig.build_probe(source, old, new)
        assert probe is not None, "probe anchor %s no longer matches exactly once" % name
        built += 1
        produced = rig.run_probe(probe)
        killed = [slot for slot, want, got in zip(rig.SWEEP, answers, produced)
                  if got != want]
        if not killed:
            survivors.append(name)
        elif len(killed) < 2:
            thin.append((name, killed))
    assert built == len(rig.PROBES), "only %d probe anchors built" % built
    assert not survivors, "probes survived every sweep dragnet: %s" % survivors
    assert not thin, "probes caught by a single dragnet only: %s" % thin


def test_an_equivalent_reference_still_restitches_correctly():
    """A no-op edit of the reference reproduces the sweep answers exactly."""
    control = rig.build_probe(rig.engine_source(), *rig.CONTROL_PROBE[1:])
    assert control is not None, "the control anchor is missing"
    assert rig.run_probe(control) == rig.sweep_answers(), (
        "the probe harness rejects an equivalent reference")


def test_reference_answers_match_the_frozen_pins():
    """Frozen digests confirm the reference did not drift at verify time."""
    pins = rig.frozen_pins()["dragnets"]
    for slot, digest in pins.items():
        tree, _report = rig.reference_tree(slot)
        blob = "".join("%s=%s\n" % (name, tree[name]) for name in sorted(tree))
        assert hashlib.sha256(blob.encode("ascii")).hexdigest() == digest, (
            "the reference restitch drifted for %s" % slot)
