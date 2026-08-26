---
name: dynamo-naive-variant-probe-predicts-fails
description: "Before pushing, patch the reference into 6-10 plausible-wrong variants and require each to match the shipped sample but diverge on held-out packs — the surviving variants are what the pass@2 agent actually writes."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f823fb73-2967-4ba1-a7c7-d1300cef3afd
  modified: 2026-08-13T00:31:46.730Z
---

Built into `dynamo-3d96edf` (`dynamo/fabric-retime-audit`, RTL retiming audit) and
measured across both difficulty gates on its first commit: pass@2 came back **1/2 with a
clean valid fail** and pass@5 **1/5 solved with 3 good valid fails (avg@5 0.200)** — ALL-GREEN
on one push — and the trial analyser's root causes were *verbatim* from the naive-variant list
I had probed before pushing — the agent solved W/D, `period_before`, `iteration_bound` and `period_after`, then
built the retiming by relaxing the **reversed** constraint graph to the pointwise-maximum
solution and shifting per component, instead of the componentwise-minimum the contract
demands. Every downstream field and all seven held-out packs failed as a cascade. Two of the four
pass@5 failures were the same variant; the analyser's phrasing — *"the worked_fabric topology
happened to tolerate the misanchor; all 9 graded packs exposed it"* — is the starve-the-sample
mechanism reporting itself.

**The procedure.** Take the reference source, apply single-string patches that encode how a
competent engineer would plausibly cut a corner, and run each variant against the shipped
pack, the worked example, and every held-out pack. Classify:

| shipped + worked | held-out | meaning |
|---|---|---|
| same | differs | **blind kill** — keep it, this is your difficulty |
| differs | differs | ordinary mutation; fine for the sweep, buys no difficulty |
| same | same | the rule is unwitnessed — a C3 hole, add a fixture |

Variants worth writing every time: adjacency keyed by `(from, to)` (drops parallel edges),
counts treated as booleans, entity set rebuilt from the relation list (drops isolated
entities), single-source relaxation instead of all-zero seeding (drops disconnected
components), skipping the reflexive `(u, u)` pair, and any canonicalisation solved from the
opposite direction.

**Why it works.** It measures the thing pass@2 actually measures, hours before the
three-hour pipeline does, and for free. It also doubles as C3 coverage evidence: a variant
in the third row above is a fixture hole QC would have found later.

Pair it with [[dynamo-blind-sample-branch]] (choose the shipped sample so the hard branch is
never entered) and [[dynamo-mutation-sweep-finds-witness-holes]] (report the build count, not
just survivors).
