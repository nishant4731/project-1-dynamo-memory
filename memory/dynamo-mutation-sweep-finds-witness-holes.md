---
name: dynamo-mutation-sweep-finds-witness-holes
description: Run the single-rule mutation sweep before pushing — surviving mutants name the exact missing fixture witness.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c8eb28ff-48a8-46b1-9e30-a4edf5944bfa
  modified: 2026-08-13T14:45:49.813Z
---

Build the mutation sweep *while* building the fixtures, not after. On
`dynamo/glint-profile` six of the first thirty-five single-rule mutants survived, and
each survivor named a concrete missing witness: a lane group with exactly one duplicated
address, an observable instruction after a nested region reconverges, a shared address
above half the memory size, arithmetic that actually overflows.

**Why:** fixture variety generated at random almost never hits boundary witnesses by
luck, and QC's C3 prober finds the same holes later — at the cost of a push that then
also needs a fresh cosine surface. Two survivors also turned out to be *provably
equivalent* rewrites (a `>=` at a point where the difference contributes zero; a modulo
already applied downstream) and were deleted rather than witnessed.

**How to apply:** report the **build count** (`built == declared`), not just "0
survivors" — an anchor whose literal was renamed silently no-ops. Fix a survivor by
adding a witness, never by dropping the mutant, unless it is provably equivalent. When
truncation itself must be observable, feed the wrapped value into an unsigned compare;
folding it into a later masked add hides it. See [[dynamo-calibration-blind-corpus]].

**A clean sweep only certifies the anchors you wrote.** On `dynamo-8ab540c` the sweep
reported 83 of 83 with zero survivors while QC C3 found a live hole: nudging
`SHIFT_ADD_LIMIT` from `1 << 12` to `1 << 13` left every graded chain byte-identical,
because the largest coefficient word in the whole corpus (main + 9 held-out + 200 salted
draws) was 805 and the rule capping words above 4096 was never exercised. None of my 83
anchors touched a *tuning constant* — they all rewrote logic. **Enumerate every numeric
threshold in the reference and mutate each one up and down**, then check the corpus
actually spans the range each constant partitions; a constant no fixture straddles is a
stated-but-unwitnessed rule. The witness that fixes it should straddle the boundary
exactly (4095 costs 1, 4097 costs 3 — one apart), not merely sit past it.
