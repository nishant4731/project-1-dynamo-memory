"""Regenerate: shipped live dragnet, charter format-sheet fragments, pins."""
import hashlib, json, os, shutil, sys
sys.path.insert(0, "/tests")
import _dragnet_rig as rig

MODE = sys.argv[1]

if MODE == "live":
    work = "/out/live"
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    shutil.rmtree("/out/dragnet", ignore_errors=True)
    shutil.move(rig.stage_crashed(rig.LIVE_ID, work), "/out/dragnet")
    print("wrote /out/dragnet")

elif MODE == "sheet":
    held = rig.reference_artifacts(rig.SHEET_ID)
    seg = sorted(held["segments"])[1]
    lines = held["segments"][seg].decode("ascii").rstrip("\n").split("\n")
    contact = held["CONTACT.tsv"].rstrip("\n").split("\n")
    rows = [r for r in contact[1:] if r.split("\t")[1] == seg][:2]
    record = [l for l in lines if json.loads(l)["fid"] == rows[1].split("\t")[0]][0]
    print(json.dumps({
        "segment_name": seg, "record": record, "contact": rows,
        "reach": held["REACH.tsv"].rstrip("\n").split("\n")[1:3],
        "pivot": held["PIVOT.tsv"].rstrip("\n").split("\n")[1:3],
        "refused": held["refused"][sorted(held["refused"])[0]].rstrip("\n").split("\n")[0]}))

elif MODE == "pins":
    pins = {
        "charter": hashlib.sha256(open(rig.CHARTER, "rb").read()).hexdigest(),
        "helper": hashlib.sha256(open(rig.HELPER, "rb").read()).hexdigest(),
        "fleet": hashlib.sha256(
            open(os.path.join(rig.LIVE_STORE, "FLEET.tsv"), "rb").read()).hexdigest(),
        "crashed_live": rig.crashed_digest(rig.LIVE_ID),
    }
    old = json.load(open("/tests/reference_pins.json"))
    dragnets = {}
    for slot in sorted(old["dragnets"]):
        tree, _ = rig.reference_tree(slot)
        blob = "".join("%s=%s\n" % (n, tree[n]) for n in sorted(tree))
        dragnets[slot] = hashlib.sha256(blob.encode("ascii")).hexdigest()
    pins["dragnets"] = dragnets
    print(json.dumps(pins, indent=2, sort_keys=True))
