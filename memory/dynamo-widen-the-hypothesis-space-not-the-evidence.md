---
name: dynamo-widen-the-hypothesis-space-not-the-evidence
description: "Measured on dynamo-b296f2d (ALL-GREEN, pass@5 0/5 with 3 valid fails): a reconstruction task solved 2/2 by exhaustive search flipped out of band by adding one dimension outside the natural enumeration — not by adding rules or evidence."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78170f0c-ffe4-4520-83b2-fd6ece737755
  modified: 2026-08-14T23:20:48.577Z
---

`dynamo-b296f2d` (`dynamo/tollgate-adjudicate`) is a reconstruction task: recover
an undocumented access-broker admission policy from a labelled round log. After
the plumbing fix cleared the timeout side, pass@2 came back **2/2 solved,
byte-exact on all 14 graded windows**, both trials converging in ~10 minutes.
Both agents had independently run the same exhaustive search over sort keys ×
limits × blocking behaviour and walked straight to the answer.

**The lever that flipped it was one extra dimension in the policy's *shape*, not
more constants, rules, or evidence.** The elevation budget stopped being kept for
the fleet and started being kept per zone — which is not the reading the phrase
"per-round budget" invites, and was outside the enumeration both agents wrote.
Next draw: **1 solved / 1 valid fail, every rubric criterion uniform PASS**, and
the analyser named the crux exactly ("including decoy columns in the ordering
search and never testing per-zone budget scope"). Critically `low_timeout` went
FAIL 0/2 → **PASS 2/2**: the failing agent was "looping in a categorically
incorrect hypothesis family; more time would not have resolved" it.

**Prove the trap with two stand-in solvers before pushing.** Write the solution
an agent would write with the *natural* hypothesis space, and the same one with
the extra dimension. Measured here: old space terminates with `no policy fits the
ledger` → reward 0; corrected space recovers in 0.27 s → reward 1. A *loud*
failure ("nothing fits") rather than a silent wrong answer is what keeps it fair
— a solver who widens the search can still get there.

**Corollary: an isolating calibration suite is an answer key.** This ledger had
31 hand-built rounds holding petitions alike on every column but one, in both
directions, announced in the fixture notes as a commissioning suite. That let
every key be *read off a controlled experiment* instead of fitted. Replaced with
490 rounds of ordinary traffic plus **three** constructed rounds written as
ordinary traffic. Measure which witnesses you actually need rather than guessing:
random traffic alone left 21 consistent policies at 182 rounds and **plateaued at
4** however many more were added — and the only two things it never pinned were
one class seat limit and the last-resort ordering direction. Two witnesses fixed
those; a third was needed because the first tie-pair's decoy columns happened to
run the same way as the id order (mirror every tie-pair).

Disclosure stays fair by naming the *openness*, not the answer:
"the ledger settles all four, and what each limit and the budget are counted
against along with them" — [[dynamo-never-hand-the-agent-the-map]].

**Outcome: ALL-GREEN.** pass@5 came back **0 solved · 3 good valid fails · 0
soft timeouts · avg@5 0.000**, final gate PASS, qc_gate 37/37 with an empty fix
list. All five trials "adopted brute-force parameter grid search over a
hypothesis space that structurally cannot contain the correct admission policy."
That sentence is the whole lever in one line: the wall is the *shape* of the
hypothesis space, not the size of the search.

Related: [[dynamo-reconstruction-beats-specification]],
[[dynamo-withhold-an-algorithm-not-a-clause]],
[[dynamo-provide-the-plumbing-clears-the-hard-side]] (the other half of this
task's calibration), [[dynamo-z3-collapses-joint-integer-fits]] (why more
constants would not have worked).
