---
name: dynamo-pass2-typo-is-not-difficulty
description: "A pass@2 \"valid fail\" caused by a typo is not difficulty evidence — read solve time vs budget, not the headline ratio."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-11T20:08:01.467Z
---

On `dynamo-56ae913` pass@2 returned **1 solved / 1 valid fail** — a passing verdict that
proceeds to pass@5. The trajectory analysis showed the failing trial had a byte-exact score
matrix and correct values, and lost only to `settls_clamped` (a one-character typo in a JSON
key) propagated to four code locations. The rubric scored that trial
`difficulty_crux: FAIL` and `near_miss: FAIL`.

**Why:** a pass@2 PASS says "at least one run failed", not "the task is hard". The signals
that actually predict pass@5 (which needs ≥3 valid fails of 5) are:
- **solve time vs the agent budget** — 16–20 min against 3600s is roughly half the load of
  accepted tasks in this mold (~35–50 min). This is the strongest single indicator.
- **`difficulty_crux` / `near_miss` on the failing trial** — if the agent solved every
  intended crux and died on something incidental, there is no crux evidence at all.
- the reviewer's own prose: "the task's difficulty signals are prominent in RUBRIC.md and
  the agents are reading and responding to them" = the spec is transcription, not derivation.

**How to apply:** when pass@2 passes at 1/2 with a non-crux failure and large spare budget,
ratchet before pass@5 runs rather than gambling — add 2–3 interacting subsystems that make
the agent *derive* something (hidden parameters recovered from evidence, state that
re-keys later stages), not merely type more rules. Do NOT ratchet when the solver used >90%
of the budget; there the fix is trimming breadth. Pair the ratchet with a fresh cosine
surface in the same push — see [[dynamo-reskin-clears-post-index-cosine]].
