#!/usr/bin/env python3
"""Author-side build: materialise fixtures, the notes example and the pins."""

import hashlib
import json
import os
import shutil
import sys

TASK = "/Users/utkarsha/Documents/Project 1/dynamo/c1fed49/task"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TASK, "tests"))

import _desk_engine as engine  # noqa: E402
import _desk_gen as gen  # noqa: E402

DATA = os.path.join(TASK, "environment", "data", "calderwell")
CYCLES = os.path.join(TASK, "tests", "cycles")


def build_fixtures():
    if os.path.isdir(CYCLES):
        shutil.rmtree(CYCLES)
    for spec in gen.CYCLE_SPECS:
        gen.write_cycle(os.path.join(CYCLES, spec[0]), *gen.build_cycle(*spec))
    os.makedirs(DATA, exist_ok=True)
    for slot, name in (("live-cycle", "live_cycle"), ("example-cycle", "example_cycle")):
        target = os.path.join(DATA, name)
        if os.path.isdir(target):
            shutil.rmtree(target)
        shutil.copytree(os.path.join(CYCLES, slot), target)
    with open(os.path.join(DATA, "determination_log.tsv"), "wb") as handle:
        handle.write(gen.log_bytes())


def build_notes():
    with open(os.path.join(SCRATCH, "NOTES_TEMPLATE.md")) as handle:
        text = handle.read()
    manifest, queues, reviewers, pressure = gen.build_cycle(*gen.CYCLES["example-cycle"])
    report, daybook_rows, assignment_rows, closing = engine.run_cycle(
        manifest, queues, reviewers, pressure
    )
    daybook_bytes = engine.render_rows(engine.DAYBOOK_COLUMNS, daybook_rows)
    assignments_bytes = engine.render_rows(engine.ASSIGNMENT_COLUMNS, assignment_rows)
    retired = engine.retirement_record(manifest, closing, daybook_bytes, assignments_bytes)
    text = text.replace("<<DAYBOOK>>", daybook_bytes.decode("ascii").rstrip("\n"))
    text = text.replace("<<ASSIGNMENTS>>", assignments_bytes.decode("ascii").rstrip("\n"))
    text = text.replace("<<REPORT>>", engine.canonical_json(report).decode("ascii").rstrip("\n"))
    text = text.replace("<<RETIRED>>", engine.canonical_json(retired).decode("ascii").rstrip("\n"))
    with open(os.path.join(DATA, "REVIEW_DESK_NOTES.md"), "w") as handle:
        handle.write(text)


def copy_modules():
    shutil.copyfile(
        os.path.join(TASK, "environment", "calderwell_io.py"),
        os.path.join(TASK, "tests", "calderwell_io.py"),
    )
    src = os.path.join(TASK, "tests", "_desk_engine.py")
    dst = os.path.join(TASK, "solution", "cycle_replay.py")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o755)


def _sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def build_pins():
    pins = {"inputs": {}, "cycles": {}}
    pins["inputs"]["notes"] = _sha(os.path.join(DATA, "REVIEW_DESK_NOTES.md"))
    pins["inputs"]["log"] = _sha(os.path.join(DATA, "determination_log.tsv"))
    pins["inputs"]["provided_io"] = _sha(os.path.join(TASK, "environment", "calderwell_io.py"))
    for spec in gen.CYCLE_SPECS:
        slot = spec[0]
        manifest, queues, reviewers, pressure = engine.load_cycle(os.path.join(CYCLES, slot))
        report, daybook_rows, assignment_rows, closing = engine.run_cycle(
            manifest, queues, reviewers, pressure
        )
        daybook_bytes = engine.render_rows(engine.DAYBOOK_COLUMNS, daybook_rows)
        assignments_bytes = engine.render_rows(engine.ASSIGNMENT_COLUMNS, assignment_rows)
        retired = engine.retirement_record(
            manifest, closing, daybook_bytes, assignments_bytes
        )
        pins["cycles"][slot] = {
            "report": hashlib.sha256(engine.canonical_json(report)).hexdigest(),
            "daybook": hashlib.sha256(daybook_bytes).hexdigest(),
            "assignments": hashlib.sha256(assignments_bytes).hexdigest(),
            "retired": hashlib.sha256(engine.canonical_json(retired)).hexdigest(),
        }
    with open(os.path.join(TASK, "tests", "reference_pins.json"), "w") as handle:
        json.dump(pins, handle, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    build_fixtures()
    build_notes()
    copy_modules()
    build_pins()
    print("built fixtures, notes, modules and pins")
