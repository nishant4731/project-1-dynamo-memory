---
name: dynamo-z3-collapses-joint-integer-fits
description: "A joint integer constraint recovery is not a difficulty wall — agents reach for z3 and SMT-solve it in seconds; internet is allowed, so budget for that."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cdcd2dbe-3dc2-46a2-8b7b-9b15206e9e4b
  modified: 2026-08-13T09:47:38.609Z
---

Measured on `dynamo-f1e47b1` (`dynamo/shadecast-refit`), 2026-08-13. To stop agents recovering
hidden constants group by group, the calibration was regrouped so no row ever exposed a single
probe's value: every row became a **meter total over 2-5 probes**, forcing the five surface
weights, a base, a gain, a hinge, a floor and a seam term to be solved out of the sums together,
against a law that both bends and clamps. Locally proved uniquely recoverable (73,000 candidate
values scanned coordinate-wise, zero aliases).

**Both pass@2 agents independently pip-installed `z3-solver` and SMT-solved it.** One finished
the whole recovery in **~13.5 seconds**. The trial analyser called out the convergence as
training-data knowledge — "z3 as a go-to tool for integer constraint problems" — rather than
first-principles derivation, and rated `approach_validity: PASS` (it is a legitimate method;
`allow_internet` must stay true, so it cannot be forbidden).

Deep Review independently flagged the consequence: "because internet is allowed and z3 collapses
the hard half to a ~14 s solve, the pass@5 gate may be at some risk."

**What the change was still worth.** It roughly tripled solve time (16 min → 24 and 60 min) and
it is what made the *failing* trajectory unrecoverable: the trial that did not reach for z3 wrote
nine successive solver scripts, none terminating, and wedged on an uninterruptible clamping
search. So it buys spread and cost, not a wall.

**How to apply.** Do not price a joint integer/linear constraint recovery as the crux — it is a
recognised problem class with an off-the-shelf solver, and the draw then hinges on whether a
trial reaches for the tool early. Put the discriminating difficulty somewhere SMT cannot help:
exactness of *reporting* (see [[dynamo-sampling-point-counters-beat-the-ceiling]]) or rules whose
correctness the shipped sample cannot witness ([[dynamo-blind-sample-branch]]).
