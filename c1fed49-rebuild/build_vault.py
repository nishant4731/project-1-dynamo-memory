#!/usr/bin/env python3
"""Author-side build: freeze vault fixtures, render the handbook, write the pins."""
import hashlib, json, os, shutil, sys, tempfile
TASK = "/Users/utkarsha/Documents/Project 1/dynamo/c1fed49/task"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TASK, "tests"))
import _vault_engine as engine
import _vault_gen as gen
import _vault_kit as kit
DATA = os.path.join(TASK, "environment", "data", "wardline")
VAULTS = os.path.join(TASK, "tests", "vaults")

def build_fixtures():
    if os.path.isdir(VAULTS):
        shutil.rmtree(VAULTS)
    for spec in gen.VAULT_SPECS:
        gen.materialise(os.path.join(VAULTS, spec[0]), spec)
    handbook = os.path.join(DATA, "VAULT_HANDBOOK.md")
    keep = open(handbook).read() if os.path.exists(handbook) else None
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(DATA)
    for slot, name in (("live-vault", "live_vault"), ("example-vault", "example_vault")):
        shutil.copytree(os.path.join(VAULTS, slot), os.path.join(DATA, name))

def build_handbook():
    text = open(os.path.join(HERE, "HANDBOOK_TEMPLATE.md")).read()
    work = tempfile.mkdtemp(prefix="handbook-")
    try:
        target = os.path.join(work, "example-vault")
        shutil.copytree(os.path.join(VAULTS, "example-vault"), target)
        report = engine.mend_vault(target)
        station = sorted(report["station_offsets"])[0]
        offset = json.dumps(
            {station: report["station_offsets"][station]}, sort_keys=True, separators=(",", ":")
        )
        collision = next(
            row for row in report["outcomes"] if "~" in row["filed_as"]
        )
        leading = next(
            (row for row in report["outcomes"] if row["filed_as"].startswith(".")),
            next(row for row in report["outcomes"] if row["filed_as"] == "-"),
        )
        rows = "\n".join(
            json.dumps(row, sort_keys=True, separators=(",", ":"))
            for row in (collision, leading)
        )
        text = text.replace("<<SAMPLE_OFFSET>>", offset)
        text = text.replace("<<SAMPLE_ROWS>>", rows)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    open(os.path.join(DATA, "VAULT_HANDBOOK.md"), "w").write(text)

def copy_solution():
    dst = os.path.join(TASK, "solution", "chart_mend.py")
    shutil.copyfile(os.path.join(TASK, "tests", "_vault_engine.py"), dst)
    os.chmod(dst, 0o755)

def build_pins():
    pins = {"inputs": {}, "vaults": {}}
    pins["inputs"]["handbook"] = hashlib.sha256(
        open(os.path.join(DATA, "VAULT_HANDBOOK.md"), "rb").read()).hexdigest()
    work = tempfile.mkdtemp(prefix="pins-")
    try:
        for spec in gen.VAULT_SPECS:
            slot = spec[0]
            target = os.path.join(work, slot)
            shutil.copytree(os.path.join(VAULTS, slot), target)
            report = engine.mend_vault(target)
            pins["vaults"][slot] = {
                "report": hashlib.sha256(engine.canonical_json(report)).hexdigest(),
                "manifest": hashlib.sha256(kit.filed_manifest(target)).hexdigest(),
            }
    finally:
        shutil.rmtree(work, ignore_errors=True)
    with open(os.path.join(TASK, "tests", "reference_pins.json"), "w") as handle:
        json.dump(pins, handle, indent=2, sort_keys=True)
        handle.write("\n")

if __name__ == "__main__":
    build_fixtures(); build_handbook(); copy_solution(); build_pins()
    print("built vault fixtures, handbook, solution and pins")
