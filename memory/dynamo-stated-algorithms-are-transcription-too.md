---
name: dynamo-stated-algorithms-are-transcription-too
description: A stated least-fixed-point closure with a plausible one-pass misreading still solved 2/2 in 38 minutes; only withholding the rule moved it.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T22:30:19.125Z
---

`[[dynamo-starve-execution-not-rules]]` says starve algorithms, not clauses. Measured on
dynamo-65cf2ab, that is **not sufficient**: a stated algorithm is still transcription.

The build: which instances get answered was a least fixed point — anchors seat themselves, an
instance joins when its ceiling shares a factor with the denominator of an already-seated
answer, repeat until a sweep adds nothing. The naive one-pass reading under-seats every corpus
by 1–7 rows and produces a ledger correct in every column but short of lines, which byte-exact
grading refuses. Generator asserted the divergence per corpus; sweep carried four seating
mutations; no answer key shipped for the working corpus.

**Result: pass@2 2/2 solved, ~38 minutes, every rubric item PASS.** The trajectory quoted the
spec's own sentence about the set being complete "only when a sweep adds nothing" and
implemented the closure directly. `difficulty_crux` PASS explicitly credited "seating closure
via repeated sweeps until stable."

**Why:** the spec has to state the rule for QC C3, and a stated rule — however global,
relational, or fixed-point shaped — is a specification the model implements. Being an
*algorithm* rather than a *clause* does not help when the algorithm is written down. The
plausible wrong reading only bites agents who don't read carefully, and these agents read
carefully.

**How to apply:** on a fully-specified mold, do not reach for a harder stated rule — that is
the same move at higher cost. Move the rule out of the spec entirely and make historic
artefacts its only normative record (`[[dynamo-reconstruction-beats-specification]]`,
`[[dynamo-calibration-ledger-not-an-oracle]]`). Then prove the artefacts *pin* it: enumerate
every rival law an agent could fit and require each to be refuted by at least one shipped
corpus (`[[dynamo-enumerate-the-rival-space]]`), and check no per-row predicate reproduces a
relational law. Keep the graded corpus without an answer key so a wrong fit gets no warning
(`[[dynamo-oracle-corpus-solve-or-timeout]]`).

Also: I had narrated the trap again — §5 warned about sweeping to a fixed point, which is
exactly what `[[dynamo-do-not-narrate-the-trap]]` and `[[dynamo-never-hand-the-agent-the-map]]`
forbid. Stating the rule *and* flagging its failure mode is two gifts, not one.
