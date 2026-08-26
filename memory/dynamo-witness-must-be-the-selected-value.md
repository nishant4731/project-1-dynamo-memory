---
name: dynamo-witness-must-be-the-selected-value
description: "A mutation witness must be the value the pipeline actually selects and keeps — an extreme gets trimmed, a non-quiet cell gets overwritten, and the mutant survives."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-13T00:20:19.471Z
---

On `dynamo-56ae913`, the mutant `hinge_bonus_not_applied` survived even though every
graded job had bonus-paying verdicts. Three separate reasons, each of which makes a
planted witness invisible to a byte-exact diff:

1. **Trimmed as an extreme.** The witness verdict was the panel maximum, and the cell
   rating is a *lower median* — changing the largest value never moves it. Fix: bracket
   the witness with companions rating just under and just over it, so the witness **is**
   the median.
2. **Unreachable rating.** The anchor's rating (156) was outside every companion lane's
   range, so no companions could be placed, the panel fell under quorum, and the cell
   voided. Fix: choose the anchor's input so its rating lands in a band the companions
   can bracket.
3. **Overwritten downstream.** The witness sat on an item a later adjustment rewrote.
   Fix: plant it on a "quiet" item, and have the verdict planner and the adjustment
   planner read **one shared table** of witness cells rather than each recomputing it.

Also measured: a counter-based witness (`bonus_verdicts` was non-zero on every job)
proves nothing about a *rating* rule — that counter deliberately counts verdicts whose
rating a refusal later overrides.

**Why:** QC C3 deletes rules no graded fixture exercises, and a surviving mutant names
exactly which fixture is missing — but only if you check the mutant per seed. Two rules
in the same push turned out **provably unreachable** and were dropped rather than
shipped as unpinnable claims (a second viable hinge; a zero bonus).

**How to apply:** after adding any rule, run the mutant for it against *every* graded
seed, not just the sweep pair, and read the survivors as "the witness is not where you
think it is". Check reachability with a short proof before writing a tie-break clause.
See [[dynamo-mutation-sweep-finds-witness-holes]] and [[dynamo-canonical-spelling-needs-witnesses]].
