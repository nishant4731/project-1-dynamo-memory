---
name: dynamo-reconstruction-mold-hit-its-ceiling
description: "Measured on dynamo-c1fed49 across four heads: the recover-the-policy-from-a-log mold is now solved in 15-50 min by the reference pair, and neither a global-optimum re-key nor evidence consumption moved it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e848bdb-69db-4125-b540-9956c1880b3f
  modified: 2026-08-15T01:30:09.639Z
---

`dynamo-c1fed49` (`dynamo/calderwell-review`, 2026-08-15) ported the
[[dynamo-reconstruction-beats-specification]] engine into medical-and-clinical
workflows. Every gate except difficulty went green on every head — cosine 4/4,
Dynamo eval 30 PASS + 1 N/A each time, similarity, validation, deep_review, AVA,
tier1, qc_eval, qc_exec, qc_gate (37 checks, 0 required fixes). Difficulty is the
only thing that failed, and it failed four different ways:

| head | lever added | pass@2 | pass@5 |
|---|---|---|---|
| 1 | 21 constants + 6-rung ladder from a 553-row log, stateful 40-day replay | 1/2 (solve 50 min) | **5/5, avg 1.000** |
| 2 | log jittered to zero one-field-apart pairs; worked example cut to 3 days; priority band | 0/2, 1 valid fail (27 min) | not reached |
| 3 | assignment becomes a whole-day optimum (max total, lexicographic tie-break) | 2/2 (15 and 47 min) | not reached |
| 4 | replay retires the cycle it reads; per-queue closing backlog graded | 2/2 (15 and 37 min) | not reached |

**The ceiling is the mold, not the tuning.** Five pass@5 trials and six pass@2
trials all ran the same route: read the notes, fit the log with a Python script
until zero of N rows mispredict, implement, diff against the worked example, run
live. Each head made that route longer, never uncertain. Trial analyses said so
outright — "sufficient and unambiguous constraints", "no divergence from the
golden approach".

**Three levers measured as ineffective here, all of which my notes rated highly:**

- *Starving the sample.* Jitter removed every one-field-apart pair from the log
  (measured: several hundred → 0), so nothing can be read off by holding a
  pairing still. Agents switched to Gaussian elimination and brute-force search
  over the ladder's 720 permutations and lost no time.
- *An algorithmic re-key.* Making the day a global optimum instead of a per-case
  pass was genuinely load-bearing (greedy reproduces the worked example exactly
  yet is rejected on 12 of 17 graded cycles; the optimum is non-unique on 22% of
  days). Both agents wrote the bitmask DP directly — because the rule is stated,
  and fairness requires stating it.
- *Evidence consumption.* Retiring the cycle fired **0/2**: both trials tested on
  the example, confirmed retirement, and ran live once with a correct tool. The
  playbook's caveat is the whole story — it only bites agents who need a second
  run.

**The fairness floor that closes the last escape.** Publishing only the verdict
and reason, without the suitability number, leaves **9 of 21 constants
undetermined** (all the level constants: the three service bases, the panel bonus
and the ceiling — outcome-only evidence sees comparisons, not levels). Measured
by running the perturbation proof against outcome-only labels. So the observed
score column cannot be removed: the very thing that makes the fit cheap is what
makes the task answerable.

**How to apply.** Do not open a new task with this mold expecting 0–2/5. It
produces beautiful, provably-fair, all-green tasks that the reference pair
solves in under an hour. Reach instead for the shapes whose answer cannot be
checked locally at all — digest-driven assembly search, evidence-mined parameters
with decoys, byte-exact naming slips — i.e. the salvage/repair mold in
[[dynamo-reconstruction-beats-specification]]'s place. Related:
[[dynamo-recovered-constants-are-still-transcription]],
[[dynamo-spec-mold-caps-at-80pct-solve]], [[dynamo-stated-optimum-gets-solved]],
[[dynamo-do-not-narrate-the-trap]].
