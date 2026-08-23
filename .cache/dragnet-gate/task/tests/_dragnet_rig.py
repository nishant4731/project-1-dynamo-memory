"""Verifier-side rig: isolation, staging, tree comparison and mutation probes.

Harbor overlays ``tests/`` at ``/tests`` only at verify time, so nothing in here
is reachable while the agent works.  Every expected answer is computed from the
protected dragnet copies this module builds, with the reference in
``_dragnet_engine``, before the submitted program is allowed to run once.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import _dragnet_engine as engine
import _dragnet_forge as forge

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

SUBMISSION = "/app/dragnet_restitch.py"
LIVE_STORE = "/app/data/dragnet"
CHARTER = "/app/data/DRAGNET_CHARTER.md"
HELPER = "/app/dragnet_io.py"
DECLARED_CONTACT = "/app/data/dragnet/CONTACT.tsv"
DECLARED_REACH = "/app/data/dragnet/REACH.tsv"
DECLARED_PIVOT = "/app/data/dragnet/PIVOT.tsv"
DECLARED_REPORT = "/app/data/dragnet/restitch_report.json"

LIVE_ID = "dragnet-live"
SHEET_ID = "format-sheet"
HELD_OUT = (
    "held-broad",
    "held-webbed",
    "held-stalled",
    "held-crowded",
    "held-orphaned",
    "held-shallow",
    "held-deep",
    "held-quiet",
    "held-noinbox",
    "held-noscratch",
    "held-onesegment",
    "held-brimful",
    "held-nosegments",
)
GRADED = (LIVE_ID,) + HELD_OUT + ("salted",)
# dragnets the mutation sweep runs over; chosen so both segment bounds, the
# ordinals, the orphan branches and the twin endings all bind somewhere
SWEEP = ("sweep-a", "sweep-b", "sweep-c", "sweep-d", "sweep-e", "sweep-f",
         "sweep-g")
# dragnets the submitted program restitches twice, to grade the settling rule
SETTLED = ("held-broad", "held-stalled", "held-quiet", "held-noinbox",
           "held-onesegment")

RUN_TIMEOUT = 180
NOBODY_UID = 65534

_CACHE = {}


class ProgramFailure(AssertionError):
    """Raised when the submitted program cannot run or leaves a dragnet wrong."""


# --------------------------------------------------------------------------
# path safety and trees
# --------------------------------------------------------------------------
def _walk_real(path, root):
    """Fail unless every component of ``path`` under ``root`` is a real entry.

    Each component is checked three ways: it must exist, it must not itself be a
    symbolic link, and ``os.path.realpath`` of the prefix so far must still be
    that prefix -- so a link anywhere above the leaf is refused even when the
    leaf is an ordinary file.  A path that resolves anywhere other than where it
    is spelled never reaches an ``open()``.
    """
    if not os.path.isabs(path):
        raise AssertionError("graded paths are absolute: %s" % path)
    walked = os.sep
    for part in path.split(os.sep):
        if not part:
            continue
        walked = os.path.join(walked, part)
        if not os.path.lexists(walked):
            raise AssertionError("missing path component: %s" % walked)
        if os.path.islink(walked):
            raise AssertionError("symlinked path component is not accepted: %s" % walked)
        if os.path.realpath(walked) != walked:
            raise AssertionError(
                "path component does not resolve to itself: %s -> %s"
                % (walked, os.path.realpath(walked)))
    if os.path.realpath(path) != path:
        raise AssertionError("path is not canonical: %s" % path)
    if not path.startswith(root + os.sep):
        raise AssertionError("path escapes %s: %s" % (root, path))
    return path


def guard_tree(root, boundary="/app"):
    """Refuse a whole tree that holds a link, at any depth, in either kind."""
    guard_dir(root, boundary)
    for base, dirs, files in os.walk(root):
        for name in sorted(dirs) + sorted(files):
            path = os.path.join(base, name)
            if os.path.islink(path):
                raise AssertionError("symlink inside %s: %s" % (root, path))
            if os.path.realpath(path) != path:
                raise AssertionError(
                    "%s does not resolve to itself: %s" % (path, os.path.realpath(path)))
    return root


def guard_dir(path, root="/app"):
    """Fail unless ``path`` is a real directory reached without a symlink."""
    _walk_real(path, root)
    if not os.path.isdir(path):
        raise AssertionError("not a directory: %s" % path)
    return path


def guard_path(path, root="/app"):
    """Fail unless ``path`` is a real file reached without a symlink."""
    _walk_real(path, root)
    if not os.path.isfile(path):
        raise AssertionError("not a regular file: %s" % path)
    return path


def read_guarded(path):
    """Return the bytes of a symlink-free, non-empty regular file under ``/app``."""
    guard_path(path)
    with open(path, "rb") as handle:
        payload = handle.read()
    if not payload:
        raise AssertionError("empty artifact: %s" % path)
    return payload


def tree_digest(root):
    """Return every file *and directory* of a dragnet, by relative path."""
    if os.path.islink(root):
        raise AssertionError("the dragnet root is a symlink: %s" % root)
    entries = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name != "__pycache__")
        for name in dirs:
            path = os.path.join(base, name)
            if os.path.islink(path):
                raise AssertionError("symlinked directory in the dragnet: %s" % path)
            entries[os.path.relpath(path, root) + "/"] = "dir"
        for name in sorted(files):
            path = os.path.join(base, name)
            if os.path.islink(path):
                raise AssertionError("symlink in the dragnet: %s" % path)
            with open(path, "rb") as handle:
                entries[os.path.relpath(path, root)] = hashlib.sha256(
                    handle.read()).hexdigest()
    return entries


def tree_problem(expected, actual, label):
    """Return a readable description of the first way two dragnets differ."""
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing:
        return "%s: the restitched dragnet is missing %s" % (label, missing[:4])
    if extra:
        return "%s: the restitched dragnet holds unexpected %s" % (label, extra[:4])
    for name in sorted(expected):
        if expected[name] != actual[name]:
            return "%s: %s differs from the reference" % (label, name)
    return None


def stable_part(tree):
    """The part of a dragnet a second restitch has to leave byte-for-byte alone."""
    return {
        name: mark for name, mark in tree.items()
        if name in ("CONTACT.tsv", "REACH.tsv", "PIVOT.tsv")
        or name.startswith("segments/")
    }


# --------------------------------------------------------------------------
# protected dragnets and reference answers
# --------------------------------------------------------------------------
def plan_for(slot):
    """Return the crashed-dragnet plan of one slot, built once and kept."""
    key = "plan-" + slot
    if key not in _CACHE:
        if slot == "salted":
            _CACHE[key] = forge.build_salted(
                int(hashlib.sha256(submitted_program()).hexdigest()[:12], 16)
                ^ 0x2D0D4C3)
        else:
            _CACHE[key] = forge.build_store(slot)
    return _CACHE[key]


def stage_crashed(slot, work):
    """Materialise one crashed dragnet inside a scratch directory."""
    target = os.path.join(work, slot)
    shutil.rmtree(target, ignore_errors=True)
    forge.write_plan(target, plan_for(slot))
    return target


def reference_tree(slot):
    """Return ``(tree, report)`` after the reference restitches one dragnet."""
    key = "ref-" + slot
    if key not in _CACHE:
        work = tempfile.mkdtemp(prefix="dragnet-ref-")
        try:
            target = stage_crashed(slot, work)
            report = engine.restitch(target)
            _CACHE[key] = (tree_digest(target), report)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return _CACHE[key]


def reference_settled(slot):
    """Return the reference tree after one restitch, and after restitching that."""
    key = "settled-" + slot
    if key not in _CACHE:
        work = tempfile.mkdtemp(prefix="dragnet-ref2-")
        try:
            target = stage_crashed(slot, work)
            engine.restitch(target)
            first = tree_digest(target)
            engine.restitch(target)
            _CACHE[key] = (first, tree_digest(target))
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return _CACHE[key]


def reference_artifacts(slot):
    """Return the text of the graded artefacts the reference writes for a slot."""
    key = "text-" + slot
    if key not in _CACHE:
        work = tempfile.mkdtemp(prefix="dragnet-text-")
        try:
            target = stage_crashed(slot, work)
            engine.restitch(target)
            held = {}
            for name in ("CONTACT.tsv", "REACH.tsv", "PIVOT.tsv"):
                with open(os.path.join(target, name), "r") as handle:
                    held[name] = handle.read()
            segments = {}
            for name in sorted(os.listdir(os.path.join(target, "segments"))):
                with open(os.path.join(target, "segments", name), "rb") as handle:
                    segments[name] = handle.read()
            refused = {}
            for name in sorted(os.listdir(os.path.join(target, "refused"))):
                with open(os.path.join(target, "refused", name), "r") as handle:
                    refused[name] = handle.read()
            held["segments"] = segments
            held["refused"] = refused
            _CACHE[key] = held
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return _CACHE[key]


def frozen_pins():
    """Return the authoring-time digests of the read-only material."""
    with open(os.path.join(TESTS_DIR, "reference_pins.json"), "r") as handle:
        return json.load(handle)


# --------------------------------------------------------------------------
# running the submitted program under isolation
# --------------------------------------------------------------------------
def _become_nobody():
    os.setgroups([])
    os.setgid(NOBODY_UID)
    os.setuid(NOBODY_UID)


def require_isolation():
    """Fail closed unless the answers can actually be put out of reach."""
    if os.geteuid() != 0:
        raise AssertionError(
            "the verifier must run as root so the submitted program can be dropped "
            "to uid %d with the overlay sealed; uid %d cannot isolate the run"
            % (NOBODY_UID, os.geteuid()))


def _seal(mode):
    try:
        os.chmod(TESTS_DIR, mode)
    except OSError:
        pass


def submitted_program():
    """Return the bytes of the submitted program, guarding against symlinks."""
    if "program" not in _CACHE:
        guard_path(SUBMISSION)
        if os.path.realpath(SUBMISSION) != SUBMISSION:
            raise AssertionError(
                "the submitted program is reached through a link: %s -> %s"
                % (SUBMISSION, os.path.realpath(SUBMISSION)))
        _CACHE["program"] = read_guarded(SUBMISSION)
    return _CACHE["program"]


def run_on(slot, timeout=RUN_TIMEOUT, passes=1):
    """Restitch a pristine crashed copy ``passes`` times; return each tree."""
    require_isolation()
    work = tempfile.mkdtemp(prefix="dragnet-run-")
    try:
        target = stage_crashed(slot, work)
        program = os.path.join(work, "candidate_restitch.py")
        with open(program, "wb") as handle:
            handle.write(submitted_program())
        with open(os.path.join(work, "dragnet_io.py"), "wb") as handle:
            handle.write(read_guarded(HELPER))
        os.chmod(work, 0o777)
        for base, dirs, files in os.walk(work):
            os.chmod(base, 0o777)
            for name in files:
                os.chmod(os.path.join(base, name), 0o666)
        os.chmod(program, 0o755)
        env = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": work,
            "LC_ALL": "C",
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        trees = []
        for attempt in range(1, passes + 1):
            _seal(0o000)
            try:
                # -s -E rather than -I: isolated mode also drops the script's
                # own directory from sys.path, which would break a submitted
                # program that imports the supplied plumbing by bare name
                proc = subprocess.run(
                    [sys.executable, "-s", "-E", program, target],
                    cwd=work, env=env, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, timeout=timeout,
                    preexec_fn=_become_nobody)
            finally:
                _seal(0o755)
            if proc.returncode != 0:
                raise ProgramFailure(
                    "program exited %d on %s (restitch %d of %d)\nstderr:\n%s"
                    % (proc.returncode, slot, attempt, passes,
                       proc.stderr.decode("utf-8", "replace")[-2000:]))
            trees.append(tree_digest(target))
        return trees
    finally:
        shutil.rmtree(work, ignore_errors=True)


def graded_runs():
    """Run the submitted program once per graded slot and cache every outcome."""
    if "runs" not in _CACHE:
        runs = {}
        for slot in GRADED:
            expected, report = reference_tree(slot)
            entry = {"expected": expected, "report": report, "error": None}
            try:
                entry["actual"] = run_on(slot)[0]
            except (ProgramFailure, subprocess.TimeoutExpired) as failure:
                entry["error"] = str(failure)
            runs[slot] = entry
        _CACHE["runs"] = runs
    return _CACHE["runs"]


def graded_run(slot):
    """Return one cached graded run, failing loudly if the program did not finish."""
    entry = graded_runs()[slot]
    if entry["error"]:
        raise AssertionError(entry["error"])
    return entry


def settled_runs():
    """Restitch each settling slot twice with the submitted program."""
    if "settled" not in _CACHE:
        runs = {}
        for slot in SETTLED:
            entry = {"error": None, "passes": None}
            try:
                entry["passes"] = run_on(slot, passes=2)
            except (ProgramFailure, subprocess.TimeoutExpired) as failure:
                entry["error"] = str(failure)
            runs[slot] = entry
        _CACHE["settled"] = runs
    return _CACHE["settled"]


def settled_run(slot):
    """Return the two trees a double restitch left, failing loudly if either did not."""
    entry = settled_runs()[slot]
    if entry["error"]:
        raise AssertionError(entry["error"])
    return entry["passes"]


# --------------------------------------------------------------------------
# strict parsing
# --------------------------------------------------------------------------
def _refuse_float(text):
    raise AssertionError("non-integer JSON number in the report: %r" % text)


def _refuse_constant(text):
    raise AssertionError("NaN/Infinity is not a valid report value: %r" % text)


def strict_load(raw):
    """Parse report bytes, rejecting floats, NaN and Infinity outright."""
    return json.loads(raw.decode("ascii"), parse_float=_refuse_float,
                      parse_constant=_refuse_constant)


def typed_diff(expected, actual, trail="report"):
    """Compare two JSON structures with exact types (so True never equals 1)."""
    if type(expected) is not type(actual):
        return "%s: expected %s, got %s" % (
            trail, type(expected).__name__, type(actual).__name__)
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            return "%s: key set differs (missing %s, extra %s)" % (
                trail, sorted(set(expected) - set(actual)),
                sorted(set(actual) - set(expected)))
        for key in sorted(expected):
            problem = typed_diff(expected[key], actual[key], "%s.%s" % (trail, key))
            if problem:
                return problem
        return None
    if expected != actual:
        return "%s: expected %r, got %r" % (trail, expected, actual)
    return None


# --------------------------------------------------------------------------
# mutation probes
# --------------------------------------------------------------------------
def engine_source():
    """Return the protected reference implementation's source text."""
    if "source" not in _CACHE:
        with open(os.path.join(TESTS_DIR, "_dragnet_engine.py"), "r") as handle:
            _CACHE["source"] = handle.read()
    return _CACHE["source"]


def build_probe(source, old, new):
    """Return mutated source, or ``None`` when the anchor no longer matches once."""
    if source.count(old) != 1:
        return None
    return source.replace(old, new)


def sweep_answers():
    """Return the reference tree of every sweep dragnet."""
    if "sweep" not in _CACHE:
        _CACHE["sweep"] = [reference_tree(slot)[0] for slot in SWEEP]
    return _CACHE["sweep"]


PROBE_DRIVER = """

if __name__ == "__main__":
    import sys as _sys

    for _target in _sys.argv[1:]:
        try:
            restitch(_target)
        except Exception:
            pass
"""


def run_probe(source, timeout=RUN_TIMEOUT):
    """Run one mutated reference, as a program, over every sweep dragnet."""
    work = tempfile.mkdtemp(prefix="dragnet-probe-")
    try:
        head = source.index('if __name__ == "__main__":')
        script = os.path.join(work, "probe_restitch.py")
        with open(script, "w") as handle:
            handle.write(source[:head] + PROBE_DRIVER.lstrip("\n"))
        targets = [stage_crashed(slot, work) for slot in SWEEP]
        try:
            subprocess.run([sys.executable, "-I", script] + targets, cwd=work,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout)
        except subprocess.TimeoutExpired:
            return [{"timed out": ""} for _slot in SWEEP]
        return [tree_digest(target) for target in targets]
    finally:
        shutil.rmtree(work, ignore_errors=True)


PROBES = (
    # --- what a record is, and the check value taken over it
    ("sum_payload_drops_label",
     '    payload = {name: record[name] for name in RECORD_FIELDS}',
     '    payload = {name: record[name] for name in RECORD_FIELDS\n               if name != "label"}'),
    ("sum_payload_takes_seq",
     '    payload = {name: record[name] for name in RECORD_FIELDS}',
     '    payload = dict(record)\n    payload.pop("sum", None)'),
    ("sum_width", 'return hashlib.sha256(blob.encode("ascii")).hexdigest()[:16]',
     'return hashlib.sha256(blob.encode("ascii")).hexdigest()[:12]'),
    ("sum_is_not_sorted", 'blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))',
     'blob = json.dumps(payload, sort_keys=False, separators=(",", ":"))'),
    # --- the sieve, clause by clause
    ("accept_missing_field", '    for name in RECORD_FIELDS + ("seq", "sum"):\n        if name not in obj:\n            return "incomplete"\n', ''),
    ("accept_extra_key", '    if set(obj) != RECORD_KEYS | extra:\n        return "malformed"\n', ''),
    ("accept_fid_shape",
     '    if set(obj) != RECORD_KEYS | extra:\n        return "malformed"\n    if not isinstance(obj["fid"], str) or not FID_SHAPE.match(obj["fid"]):\n        return "malformed"\n',
     '    if set(obj) != RECORD_KEYS | extra:\n        return "malformed"\n'),
    ("accept_host_shape", '        if not isinstance(obj[name], str) or not HOST_SHAPE.match(obj[name]):\n            return "malformed"\n', ''),
    ("accept_integer_excludes_bool",
     'return isinstance(value, int) and not isinstance(value, bool)',
     'return isinstance(value, int)'),
    ("accept_integer_excludes_float",
     'return isinstance(value, int) and not isinstance(value, bool)',
     'return isinstance(value, (int, float)) and not isinstance(value, bool)'),
    ("accept_port_low_inclusive",
     '        if not PORT_LOW <= obj[name] <= PORT_HIGH:',
     '        if not PORT_LOW < obj[name] <= PORT_HIGH:'),
    ("accept_port_high_inclusive",
     '    for name in ("sport", "dport"):\n        if not PORT_LOW <= obj[name] <= PORT_HIGH:',
     '    for name in ("sport", "dport"):\n        if not PORT_LOW <= obj[name] < PORT_HIGH:'),
    ("accept_bytes_at_one",
     '    if obj["bytes"] < 1 or obj["pkts"] < 1:',
     '    if obj["bytes"] <= 1 or obj["pkts"] < 1:'),
    ("accept_pkts_at_one",
     '    if obj["bytes"] < 1 or obj["pkts"] < 1:\n        return "malformed"',
     '    if obj["bytes"] < 1 or obj["pkts"] <= 1:\n        return "malformed"'),
    ("accept_seq_at_zero", '    if obj["seq"] < 0:\n        return "malformed"',
     '    if obj["seq"] <= 0:\n        return "malformed"'),
    ("accept_label_at_the_limit", 'len(obj["label"]) > LABEL_LIMIT',
     'len(obj["label"]) >= LABEL_LIMIT'),
    ("accept_port_range", '    for name in ("sport", "dport"):\n        if not PORT_LOW <= obj[name] <= PORT_HIGH:\n            return "malformed"\n', ''),
    ("accept_port_high", "PORT_HIGH = 65535", "PORT_HIGH = 70000"),
    ("accept_counts_positive", '    if obj["bytes"] < 1 or obj["pkts"] < 1:\n        return "malformed"\n', ''),
    ("accept_window_is_open", '    if obj["last"] <= obj["first"]:\n        return "malformed"',
     '    if obj["last"] < obj["first"]:\n        return "malformed"'),
    ("accept_seq_not_negative", '    if obj["seq"] < 0:\n        return "malformed"\n', ''),
    ("accept_state_set",
     '    if obj["state"] not in STATES:\n        return "malformed"\n    if (not isinstance(obj["label"], str)',
     '    if (not isinstance(obj["label"], str)'),
    ("accept_label_shape", '    if (not isinstance(obj["label"], str) or len(obj["label"]) > LABEL_LIMIT\n            or not LABEL_SHAPE.match(obj["label"])):\n        return "malformed"\n', ''),
    ("accept_label_limit", "LABEL_LIMIT = 120", "LABEL_LIMIT = 400"),
    ("accept_sum_shape", '    if not isinstance(obj["sum"], str) or not SUM_SHAPE.match(obj["sum"]):\n        return "malformed"\n', ''),
    ("accept_sensor_roster", '    if obj["sensor"] not in sensors:\n        return "unknown_sensor"\n', ''),
    ("accept_check_value", '    if obj["sum"] != flow_sum(obj):\n        return "tampered"\n', ''),
    ("accept_fid_is_free", '    if obj["fid"] in taken:\n        return "duplicate_id"\n', ''),
    ("accept_cause_order_sensor_first",
     '    if obj["sensor"] not in sensors:\n        return "unknown_sensor"\n    if obj["sum"] != flow_sum(obj):\n        return "tampered"',
     '    if obj["sum"] != flow_sum(obj):\n        return "tampered"\n    if obj["sensor"] not in sensors:\n        return "unknown_sensor"'),
    ("accept_amend_shape", '    if set(obj) != AMEND_KEYS:\n        return "malformed"\n', ''),
    ("accept_amend_state", '    if obj["state"] not in STATES:\n        return "malformed"\n    return None\n\n\ndef retract_cause', '    return None\n\n\ndef retract_cause'),
    ("accept_retract_shape", '    if set(obj) != RETRACT_KEYS:\n        return "malformed"\n', ''),
    ("accept_unknown_op", '            else:\n                cause = "malformed"', '            else:\n                cause = None'),
    # --- reading order
    ("read_segments_by_name",
     '    return sorted(name for name in os.listdir(root)\n                  if os.path.isfile(os.path.join(root, name)))',
     '    return sorted((name for name in os.listdir(root)\n                   if os.path.isfile(os.path.join(root, name))), reverse=True)'),
    ("read_claims_in_fold_order", '            taken.add(obj["fid"])\n            carried[obj["fid"]] = obj["sum"]\n            settled.append(dict(obj))',
     '            carried[obj["fid"]] = obj["sum"]\n            settled.append(dict(obj))'),
    # --- the fold
    ("fold_by_sequence", 'operations.sort(key=lambda item: (item[0]["seq"], item[1], item[2]))',
     'operations.sort(key=lambda item: (item[1], item[2]))'),
    ("fold_tie_by_file_name", 'operations.sort(key=lambda item: (item[0]["seq"], item[1], item[2]))',
     'operations.sort(key=lambda item: (item[0]["seq"], item[2]))'),
    ("fold_amend_incoherent", 'elif operation["last"] <= held[fid]["first"]:', 'elif False:'),
    ("fold_incoherent_at_the_boundary",
     'elif operation["last"] <= held[fid]["first"]:',
     'elif operation["last"] < held[fid]["first"]:'),
    ("fold_amend_bumps_seq", '                target["seq"] = operation["seq"]\n                amended += 1', '                amended += 1'),
    ("fold_amend_writes_state", '                for name in ("bytes", "pkts", "state", "last"):',
     '                for name in ("bytes", "pkts", "last"):'),
    ("fold_retract_removes",
     '                del held[fid]\n                order.remove(fid)\n                retracted += 1',
     '                retracted += 1'),
    ("fold_orphan_is_current", '            if fid not in held:\n                orphan_amends += 1',
     '            if fid not in carried:\n                orphan_amends += 1'),
    # --- co-observations
    ("merge_key", 'mark = (flow["src"], flow["dst"], flow["sport"], flow["dport"], flow["first"])',
     'mark = (flow["src"], flow["dst"], flow["sport"], flow["dport"])'),
    ("merge_keeper_by_seq", 'keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))',
     'keeper = min(crowd, key=lambda flow: (-flow["last"], flow["fid"]))'),
    ("merge_keeper_tiebreak", 'keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))',
     'keeper = max(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))'),
    ("merge_keeper_tiebreak_is_lowest_fid",
     'keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))',
     'keeper = min(crowd, key=lambda flow: (-flow["seq"], [-ord(c) for c in flow["fid"]]))'),
    ("settle_order_tiebreak", 'merged.sort(key=lambda flow: (flow["first"], flow["fid"]))',
     'merged.sort(key=lambda flow: (flow["first"], [-ord(c) for c in flow["fid"]]))'),
    ("merge_label_from_the_keeper", '        flow = dict(keeper)',
     '        flow = dict(keeper)\n        flow["label"] = min(item["label"] for item in crowd)'),
    ("merge_lowest_fid", '        flow["fid"] = min(item["fid"] for item in crowd)',
     '        flow["fid"] = max(item["fid"] for item in crowd)'),
    ("merge_greatest_last", '        flow["last"] = max(item["last"] for item in crowd)', '        pass'),
    ("merge_greatest_bytes", '        flow["bytes"] = max(item["bytes"] for item in crowd)', '        pass'),
    ("merge_greatest_pkts", '        flow["pkts"] = max(item["pkts"] for item in crowd)', '        pass'),
    ("sums_are_retaken", '        flow["sum"] = fresh', '        pass'),
    # --- packing and the index
    ("settle_order", 'merged.sort(key=lambda flow: (flow["first"], flow["fid"]))',
     'merged.sort(key=lambda flow: (flow["fid"],))'),
    ("segment_capacity", "SEGMENT_CAPACITY = 13", "SEGMENT_CAPACITY = 11"),
    ("segment_capacity_binds", 'len(current) >= SEGMENT_CAPACITY\n', 'False\n'),
    ("segment_capacity_at_the_bound", 'len(current) >= SEGMENT_CAPACITY\n',
     'len(current) > SEGMENT_CAPACITY\n'),
    ("segment_budget_at_the_bound", 'or used + size > SEGMENT_BYTE_BUDGET):',
     'or used + size >= SEGMENT_BYTE_BUDGET):'),
    ("segment_budget", "SEGMENT_BYTE_BUDGET = 3450", "SEGMENT_BYTE_BUDGET = 2900"),
    ("segment_budget_binds", '                        or used + size > SEGMENT_BYTE_BUDGET):',
     '                        or False):'),
    ("segment_size_counts_newline", 'return len(render_record(record).encode("ascii")) + 1',
     'return len(render_record(record).encode("ascii"))'),
    ("segment_naming", 'name = "%04d.jsonl" % number', 'name = "%03d.jsonl" % number'),
    ("segment_trailing_newline", 'body.append(render_record(flow) + "\\n")',
     'body.append(render_record(flow))'),
    ("index_offset_is_bytes", '            offset += record_size(flow)', '            offset += 1'),
    ("index_offset_restarts", '        offset = 0\n        body = []', '        body = []'),
    ("index_header", 'index = ["\\t".join(CONTACT_COLUMNS)]', 'index = []'),
    ("index_columns", 'CONTACT_COLUMNS = ("fid", "segment", "offset", "src", "dst", "state",\n                   "first", "last")',
     'CONTACT_COLUMNS = ("fid", "segment", "offset", "src", "dst", "state",\n                   "first")'),
    ("record_is_sorted", '    return json.dumps(body, sort_keys=True, separators=(",", ":"))',
     '    return json.dumps(body, sort_keys=False, separators=(",", ":"))'),
    # --- the inclusive edges of the bounds, one probe per edge and per path.
    # --- The record, amend and retract paths each state their own; a witness on
    # --- one of them says nothing about the other two.
    ("record_bytes_bound", 'if obj["bytes"] < 1 or obj["pkts"] < 1:',
     'if obj["bytes"] <= 1 or obj["pkts"] < 1:'),
    ("record_pkts_bound", 'if obj["bytes"] < 1 or obj["pkts"] < 1:',
     'if obj["bytes"] < 1 or obj["pkts"] <= 1:'),
    ("record_seq_bound", '    if obj["seq"] < 0:\n        return "malformed"\n    if obj["state"]',
     '    if obj["seq"] <= 0:\n        return "malformed"\n    if obj["state"]'),
    ("amend_bytes_bound", 'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
     'if obj["bytes"] <= 1 or obj["pkts"] < 1 or obj["seq"] < 0:'),
    ("amend_pkts_bound", 'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
     'if obj["bytes"] < 1 or obj["pkts"] <= 1 or obj["seq"] < 0:'),
    ("amend_seq_bound", 'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] < 0:',
     'if obj["bytes"] < 1 or obj["pkts"] < 1 or obj["seq"] <= 0:'),
    ("retract_seq_bound", 'if not is_int(obj["seq"]) or obj["seq"] < 0:',
     'if not is_int(obj["seq"]) or obj["seq"] <= 0:'),
    ("label_alphabet_holds_digits",
     'LABEL_SHAPE = re.compile(r"\\A[a-z][a-z0-9]*([/-][a-z0-9]+)*\\Z")',
     'LABEL_SHAPE = re.compile(r"\\A[a-z][a-z0-1]*([/-][a-z0-1]+)*\\Z")'),
    ("segment_budget_over_by_one", "SEGMENT_BYTE_BUDGET = 3450",
     "SEGMENT_BYTE_BUDGET = 3451"),
    ("segment_capacity_over_by_one", "SEGMENT_CAPACITY = 13",
     "SEGMENT_CAPACITY = 14"),
    # --- the duplicate rule spans the whole sift, not just the segments
    ("sift_inbox_admit_claims_its_fid",
     '                taken.add(obj["fid"])\n                carried[obj["fid"]] = obj["sum"]',
     '                carried[obj["fid"]] = obj["sum"]'),
    ("sift_segment_record_claims_its_fid",
     '            taken.add(obj["fid"])\n            carried[obj["fid"]] = obj["sum"]',
     '            carried[obj["fid"]] = obj["sum"]'),
    # --- the contact graph, looking forward
    ("reach_only_closed", 'edges = [flow for flow in flows if flow["state"] == "closed"]',
     'edges = [flow for flow in flows if flow["state"] != "timeout"]'),
    ("reach_origin_is_unconstrained",
     '        if edge["src"] == origin:\n            open_now = True',
     '        if False:\n            open_now = True'),
    ("reach_window_lower_edge",
     '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
     '                when < edge["first"] <= when + RELAY_WINDOW for when in held)'),
    ("reach_window_upper_edge",
     '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
     '                when <= edge["first"] < when + RELAY_WINDOW for when in held)'),
    ("reach_window_is_bounded",
     '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
     '                when <= edge["first"] for when in held)'),
    ("reach_window_width", 'RELAY_WINDOW = 380000', 'RELAY_WINDOW = 380001'),
    ("reach_window_width_down", 'RELAY_WINDOW = 380000', 'RELAY_WINDOW = 379999'),
    ("reach_keeps_every_arrival",
     '        standing.setdefault(edge["dst"], set()).add(landed)',
     '        standing[edge["dst"]] = {min(min(standing.get(edge["dst"], {landed})), landed)}'),
    ("reach_arrives_at_last", '        landed = edge["last"]', '        landed = edge["first"]'),
    ("reach_keeps_earliest",
     '        arrival[edge["dst"]] = min(arrival.get(edge["dst"], landed), landed)',
     '        arrival[edge["dst"]] = max(arrival.get(edge["dst"], landed), landed)'),
    ("reach_propagates",
     '        standing.setdefault(edge["dst"], set()).add(landed)',
     '        pass'),
    ("reach_counts_hosts", 'rows.append((origin, len(arrival), horizon, farthest))',
     'rows.append((origin, len(arrival) + 1, horizon, farthest))'),
    ("reach_horizon_is_greatest", 'horizon = max(arrival.values())', 'horizon = min(arrival.values())'),
    ("reach_farthest_lowest_id", 'farthest = min(host for host in arrival if arrival[host] == horizon)',
     'farthest = max(host for host in arrival if arrival[host] == horizon)'),
    ("reach_origins_are_sources", 'origins = sorted({edge["src"] for edge in edges})',
     'origins = sorted({edge["dst"] for edge in edges})'),
    ("reach_header", 'table = ["\\t".join(REACH_COLUMNS)]', 'table = []'),
    # --- the inbound view, looking back
    ("pivot_walks_backward",
     'for edge in sorted(edges, key=lambda flow: (-flow["first"], flow["fid"])):',
     'for edge in sorted(edges, key=lambda flow: (flow["first"], flow["fid"])):'),
    ("pivot_window_lower_edge",
     '                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW',
     '                and edge["last"] < nxt["first"] <= edge["last"] + RELAY_WINDOW'),
    ("pivot_window_upper_edge",
     '                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW',
     '                and edge["last"] <= nxt["first"] < edge["last"] + RELAY_WINDOW'),
    ("pivot_window_is_bounded",
     '                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW',
     '                and edge["last"] <= nxt["first"]'),
    ("pivot_lands_at_target", '        if edge["dst"] == target:', '        if edge["src"] == target:'),
    ("pivot_needs_a_landing_contact",
     '                enough.get(nxt["fid"])\n',
     '                True\n'),
    ("pivot_opening_is_the_first",
     'opening[edge["src"]] = min(opening.get(edge["src"], edge["first"]),\n                                       edge["first"])',
     'opening[edge["src"]] = min(opening.get(edge["src"], edge["last"]),\n                                       edge["last"])'),
    ("pivot_opening_is_least",
     'opening[edge["src"]] = min(opening.get(edge["src"], edge["first"]),\n                                       edge["first"])',
     'opening[edge["src"]] = max(opening.get(edge["src"], edge["first"]),\n                                       edge["first"])'),
    ("pivot_origin_lowest_id",
     'origin = min(host for host in opening if opening[host] == opened)',
     'origin = max(host for host in opening if opening[host] == opened)'),
    ("pivot_opened_is_least", 'opened = min(opening.values())', 'opened = max(opening.values())'),
    ("pivot_targets_are_destinations", 'targets = sorted({edge["dst"] for edge in edges})',
     'targets = sorted({edge["src"] for edge in edges})'),
    ("pivot_header", 'board = ["\\t".join(PIVOT_COLUMNS)]', 'board = []'),
    ("pivot_columns", 'PIVOT_COLUMNS = ("target", "sources", "opened", "origin")',
     'PIVOT_COLUMNS = ("target", "sources", "opened")'),
    # --- the refusals
    ("refused_stem", '            stem = name.rpartition(".")[0]', '            stem = name'),
    ("refused_first_takes_plain", '                filed[source] = "%s.rej" % stem',
     '                filed[source] = "%s-1.rej" % stem'),
    ("refused_next_ordinal", '                filed[source] = "%s-%d.rej" % (stem, claimed[stem])',
     '                filed[source] = "%s-%d.rej" % (stem, claimed[stem] - 1)'),
    ("refused_line_number", '        entry = {"cause": cause, "line": number, "source": source, "text": text}',
     '        entry = {"cause": cause, "line": number - 1, "source": source, "text": text}'),
    ("refused_keeps_reading_order", '    for source, name, number, cause, text in refusals:',
     '    for source, name, number, cause, text in sorted(refusals):'),
    # --- consumption and the report
    ("consume_inbox", '    inbox_consumed = discard(inbox_dir)', '    inbox_consumed = 0'),
    ("consume_counts_the_whole_tree",
     '    for base, _dirs, files in os.walk(root):\n        held += len(files)',
     '    held += len([name for name in os.listdir(root)\n                 if os.path.isfile(os.path.join(root, name))])'),
    ("consume_scratch", '    scratch_consumed = discard(os.path.join(dragnet, "scratch"))',
     '    scratch_consumed = 0'),
    ("report_refused_split", '        "refused_from_segments": refused_from_segments,',
     '        "refused_from_segments": len(refusals),'),
    ("report_ordinalled", '                ordinalled += 1', '                pass'),
    ("report_observations_settled", '        "observations_settled": len(folded),',
     '        "observations_settled": len(merged),'),
    ("report_merge_groups", '            merge_groups += 1', '            pass'),
    ("report_bytes_written", '        bytes_written += len(payload)',
     '        bytes_written += len(payload) - len(chunk)'),
    ("report_contacts", '"contacts": len([flow for flow in merged if flow["state"] == "closed"]),',
     '"contacts": len(merged),'),
    ("report_reach_pairs", '"reach_pairs": sum(row[1] for row in rows),', '"reach_pairs": len(rows),'),
    ("report_sums_rewritten", '            sums_rewritten += 1', '            pass'),
    ("report_is_sorted", 'text = json.dumps(report, sort_keys=True, separators=(",", ":"))',
     'text = json.dumps(report, sort_keys=False, separators=(",", ":"))'),
    ("report_separators", 'text = json.dumps(report, sort_keys=True, separators=(",", ":"))',
     'text = json.dumps(report, sort_keys=True, separators=(", ", ": "))'),
    ("report_trailing_newline", 'return (text + "\\n").encode("ascii")', 'return text.encode("ascii")'),
)

CONTROL_PROBE = ("control_no_op", "RECORD_KEYS = ", "RECORD_KEYS  = ")


# --------------------------------------------------------------------------
# leak scan and graded paths
# --------------------------------------------------------------------------
GRADED_DIRS = ("/app/data", "/app/data/dragnet", "/app/data/dragnet/segments")
GRADED_FILES = (SUBMISSION, CHARTER, HELPER, "/app/data/dragnet/FLEET.tsv",
                DECLARED_CONTACT, DECLARED_REACH, DECLARED_PIVOT, DECLARED_REPORT)


def guard_graded_paths():
    """Walk every path the grader reads, refusing any symlinked component."""
    for path in GRADED_DIRS:
        guard_dir(path)
    for path in GRADED_FILES:
        guard_path(path)
    for root in ("/app/data/dragnet/segments", "/app/data/dragnet/refused"):
        if not os.path.isdir(root):
            continue
        guard_tree(root)
    # the whole live dragnet, at any depth: a link anywhere in it is refused
    guard_tree(LIVE_STORE)


def scan_for_leaks(root="/app/data"):
    """Return shipped files that name a held-out dragnet or a reference module."""
    guard_dir(root)
    needles = [slot.encode("ascii") for slot in HELD_OUT + SWEEP]
    needles += [b"reference_pins", b"_dragnet_engine", b"_dragnet_forge",
                b"_dragnet_rig"]
    hits = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name != "__pycache__"]
        for name in files:
            path = os.path.join(base, name)
            if os.path.islink(path):
                raise AssertionError("symlink under the shipped data: %s" % path)
            try:
                if os.path.getsize(path) > 8_000_000:
                    continue
                with open(path, "rb") as handle:
                    blob = handle.read()
            except OSError:
                continue
            if any(needle in blob for needle in needles):
                hits.append(path)
    return hits


def supplied_plumbing():
    """Load the shipped helper the way a submitted program would import it."""
    if "helper" not in _CACHE:
        work = tempfile.mkdtemp(prefix="dragnet-io-")
        try:
            copy = os.path.join(work, "dragnet_io.py")
            with open(copy, "wb") as handle:
                handle.write(read_guarded(HELPER))
            namespace = {"__name__": "dragnet_io", "__file__": copy}
            with open(copy, "r") as handle:
                exec(compile(handle.read(), copy, "exec"), namespace)
            _CACHE["helper"] = namespace
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return _CACHE["helper"]


def crashed_digest(slot):
    """Return a digest over the crashed dragnet the builder lays down for a slot."""
    work = tempfile.mkdtemp(prefix="dragnet-crash-")
    try:
        target = stage_crashed(slot, work)
        tree = tree_digest(target)
        blob = "".join("%s=%s\n" % (name, tree[name]) for name in sorted(tree))
        return hashlib.sha256(blob.encode("ascii")).hexdigest()
    finally:
        shutil.rmtree(work, ignore_errors=True)


def charter_fragments():
    """Return the indented fragments the charter's format sheet quotes."""
    text = read_guarded(CHARTER).decode("utf-8")
    sheet = text[text.index("## 12. Format sheet"):]
    return [line[4:] for line in sheet.split("\n")
            if line.startswith("    ") and line.strip()]
