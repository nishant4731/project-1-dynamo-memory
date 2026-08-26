---
name: dynamo-calibration-blind-corpus
description: Dynamo difficulty pattern — a calibration corpus that pins hidden constants but never exercises the graded traps.
metadata: 
  node_type: memory
  type: project
  originSessionId: c8eb28ff-48a8-46b1-9e30-a4edf5944bfa
  modified: 2026-08-11T19:28:16.024Z
---

For Dynamo tasks where the agent must recover hidden constants from measured evidence,
make the calibration corpus **narrow on purpose**: it pins the constants uniquely, but
never walks the rules the graded instances depend on. Built for `dynamo/glint-profile`
(GPU kernels and accelerators, 2026-08-12) — calibration kernels use aligned addresses,
never repeat a shared address inside a lane group, and never straddle a sector, so a
wrong memory model still reproduces every measured cycle count and only diverges where
no measurement exists.

**Why:** it gives the agent a real, honest self-check (the constants must fit every
calibration row) while leaving the decisive rules unverifiable locally — fair, fully
disclosed, and still self-check-blind. It also entangles the subsystems: the equations
are built from the agent's own counters, so one counter bug poisons every constant.

**How to apply:** assert both directions in the generator — the calibration features must
be *zero* on the trap counters, and the graded fixtures must witness each of them. Pick a
hinge constant *after* building the graded fixtures (one below a value they actually
reach), then prove identifiability by exact rank: full rank at the true hinge, and an
*inconsistent* augmented system at every other hinge value, since a rank-deficient system
can hide a second admissible assignment. See [[dynamo-mutation-sweep-finds-witness-holes]].
