---
name: dynamo-silent-misread-converts-solvers
description: Measured on dynamo-56ae913 — adding a silently-wrong reading (not more rules) moved pass@5 from 4 solved/0 valid/1 timeout to 3 solved/2 valid/0 timeouts.
metadata: 
  node_type: memory
  type: project
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-13T00:19:31.651Z
---

Measured 2026-08-13 on `dynamo-56ae913`, same engine, two consecutive pushes.

| push | change | pass@5 |
|---|---|---|
| `7bea633` | a fourth graded artifact (volume) | 4 solved · 0 valid · **1 timeout** |
| `22d1a16` | one new *inference* step with a silent wrong reading | 3 solved · **2 valid** · 0 timeouts |

The ratchet that worked: a single symptom (a seat's calibration marks fit no one
affine lane) given **two** possible causes, told apart by which axis separates the
marks — raw score (hinged) vs observation time (drifted) — with some seats
admitting both readings at once and a disclosed precedence deciding them.

Why it converts where volume does not: both failures were the *same* analytical
bug in the fitting stage, and both agents **detected** the symptom (all judges
classified unlocked) and still burned ~20 steps failing to fix it. One even got a
synthetic test to pass and the real job still wrong. Volume raises the clock;
a wrong reading that still emits well-formed files raises the failure rate.

Corollary that guided the next push: prefer a wrong reading that is **silent**.
Making the hinge bonus signed (`-40..40`, non-zero) means a fitter assuming a
reward does not error on a penalty seat — it silently returns *drifted*, with two
lanes that fit and a plausible cut, and then rates every later verdict on that
seat through a stamp-keyed lane instead of a raw-keyed one.

**How to apply:** to move pass@5 on a fully-specified-spec task, add an inference
step whose natural-but-wrong reading produces plausible output, not another rule
to transcribe. See [[dynamo-spec-mold-caps-at-80pct-solve]] for the ceiling this
is pushing against, and [[dynamo-witness-must-be-the-selected-value]] for making
the new rule actually gradeable.
