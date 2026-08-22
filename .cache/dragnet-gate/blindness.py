"""Patch the reference into plausible misreadings; report blind-on-live / caught."""
import os, shutil, subprocess, sys, tempfile
sys.path.insert(0, "/tests")
import _dragnet_rig as rig

SOLUTION = open("/solution/dragnet_restitch.py").read()

VARIANTS = [
 # --- the relay window: the natural code an agent writes
 ("reach_keeps_only_the_earliest_arrival",
  '        standing.setdefault(edge["dst"], set()).add(landed)',
  '        standing[edge["dst"]] = {min(min(standing.get(edge["dst"], {landed})), landed)}'),
 ("reach_keeps_only_the_latest_arrival",
  '        standing.setdefault(edge["dst"], set()).add(landed)',
  '        standing[edge["dst"]] = {max(max(standing.get(edge["dst"], {landed})), landed)}'),
 ("reach_ignores_the_relay_window",
  '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
  '                when <= edge["first"] for when in held)'),
 ("reach_window_measured_from_first",
  '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
  '                when <= edge["first"] <= when + RELAY_WINDOW for when in held) if True else None'),
 ("reach_window_is_exclusive_above",
  '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
  '                when <= edge["first"] < when + RELAY_WINDOW for when in held)'),
 ("reach_window_is_exclusive_below",
  '                when <= edge["first"] <= when + RELAY_WINDOW for when in held)',
  '                when < edge["first"] <= when + RELAY_WINDOW for when in held)'),
 ("pivot_ignores_the_relay_window",
  '                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW',
  '                and edge["last"] <= nxt["first"]'),
 ("pivot_is_reach_on_reversed_edges",
  'for edge in sorted(edges, key=lambda flow: (-flow["first"], flow["fid"])):',
  'for edge in sorted(edges, key=lambda flow: (flow["first"], flow["fid"])):'),
 ("pivot_opening_is_when_it_landed",
  'opening[edge["src"]] = min(opening.get(edge["src"], edge["first"]),\n                                       edge["first"])',
  'opening[edge["src"]] = min(opening.get(edge["src"], edge["last"]),\n                                       edge["last"])'),
 ("pivot_window_is_exclusive_above",
  '                and edge["last"] <= nxt["first"] <= edge["last"] + RELAY_WINDOW',
  '                and edge["last"] <= nxt["first"] < edge["last"] + RELAY_WINDOW'),

 # --- folding the inbox: order and contention
 ("ops_ordered_by_file_before_seq",
  'operations.sort(key=lambda item: (item[0]["seq"], item[1], item[2]))',
  'operations.sort(key=lambda item: (item[1], item[2], item[0]["seq"]))'),
 ("ops_tie_broken_by_line_before_file",
  'operations.sort(key=lambda item: (item[0]["seq"], item[1], item[2]))',
  'operations.sort(key=lambda item: (item[0]["seq"], item[2], item[1]))'),
 # --- the co-observation merge
 ("merge_keeper_is_the_lowest_seq",
  'keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))',
  'keeper = min(crowd, key=lambda flow: (flow["seq"], flow["fid"]))'),
 ("merge_keeper_tie_by_greatest_fid",
  'keeper = min(crowd, key=lambda flow: (-flow["seq"], flow["fid"]))',
  'keeper = min(crowd, key=lambda flow: (-flow["seq"], [-ord(c) for c in flow["fid"]]))'),
 ("merge_takes_greatest_fid",
  'flow["fid"] = min(item["fid"] for item in crowd)',
  'flow["fid"] = max(item["fid"] for item in crowd)'),
 ("merge_takes_least_last",
  'flow["last"] = max(item["last"] for item in crowd)',
  'flow["last"] = min(item["last"] for item in crowd)'),
 ("merge_takes_least_bytes",
  'flow["bytes"] = max(item["bytes"] for item in crowd)',
  'flow["bytes"] = min(item["bytes"] for item in crowd)'),
 ("merge_takes_least_pkts",
  'flow["pkts"] = max(item["pkts"] for item in crowd)',
  'flow["pkts"] = min(item["pkts"] for item in crowd)'),
 # --- the packer
 ("pack_capacity_off_by_one",
  'if current and (len(current) >= SEGMENT_CAPACITY',
  'if current and (len(current) > SEGMENT_CAPACITY'),
 ("pack_budget_off_by_one",
  'or used + size > SEGMENT_BYTE_BUDGET):',
  'or used + size >= SEGMENT_BYTE_BUDGET):'),
 ("pack_sorted_by_fid_first",
  'merged.sort(key=lambda flow: (flow["first"], flow["fid"]))',
  'merged.sort(key=lambda flow: (flow["fid"], flow["first"]))'),
]

GRADED = (rig.LIVE_ID,) + rig.HELD_OUT

def answers_for(text):
    work = tempfile.mkdtemp(prefix="blind-")
    try:
        prog = os.path.join(work, "cand.py")
        open(prog, "w").write(text)
        shutil.copy(rig.HELPER, os.path.join(work, "dragnet_io.py"))
        out = {}
        for slot in GRADED:
            target = rig.stage_crashed(slot, work)
            r = subprocess.run([sys.executable, "-s", "-E", prog, target],
                               capture_output=True, timeout=300)
            out[slot] = (r.returncode, rig.tree_digest(target) if r.returncode == 0 else None)
            shutil.rmtree(target, ignore_errors=True)
        return out
    finally:
        shutil.rmtree(work, ignore_errors=True)

good = answers_for(SOLUTION)
print("%-42s %-10s %s" % ("variant", "on live", "held-out wrong"))
blind = 0
for name, old, new in VARIANTS:
    if SOLUTION.count(old) != 1:
        print("%-42s ANCHOR MISSING (%d)" % (name, SOLUTION.count(old)))
        continue
    got = answers_for(SOLUTION.replace(old, new))
    live_same = got[rig.LIVE_ID] == good[rig.LIVE_ID]
    wrong = [s for s in rig.HELD_OUT if got[s] != good[s]]
    blind += live_same and len(wrong) > 0
    print("%-42s %-10s %d of %d" % (
        name, "BLIND" if live_same else "visible", len(wrong), len(rig.HELD_OUT)))
print("\nblind on the shipped dragnet and wrong held-out: %d of %d" % (blind, len(VARIANTS)))
