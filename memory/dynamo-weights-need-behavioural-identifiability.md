---
name: dynamo-weights-need-behavioural-identifiability
description: "A linear scoring policy can never be pinned exactly by a log; prove all survivors are order-identical instead, using tie pairs presented in both tie-break orders."
metadata: 
  node_type: memory
  type: project
  originSessionId: 858c7146-cad6-4d04-a6cb-b2b908e4341d
  modified: 2026-08-14T19:20:31.912Z
---

When a withheld policy scores candidates with integer weights (`w1*a + w2*b - w3*c`),
no amount of logged evidence pins the weights exactly: finitely many strict sign
constraints always leave an open cone around the true ray, so an exhaustive grid
search will always report survivors. Chasing "zero survivors" on the constants is
the wrong target and burns hours.

**Why:** what fairness actually requires is that every surviving reading produces
the same graded output, not the same numbers. Positive multiples of the true
weights are the same policy written differently.

**How to apply:** (1) run the grid search anyway, then check whether each survivor
induces the *same ordering* over the whole reachable feature space — if the only
survivors are exact positive multiples, the policy is behaviourally identified and
QC B5 is answered. (2) To collapse the cone to that ray, ship **level contests**:
pairs the true policy ranks *equal*, emitted twice with the lower-tie-break field
swapped between them. Any rival that breaks the tie picks the wrong one in exactly
one of the two. Two linearly independent difference vectors from the null space of
the weight vector are enough — solve `w·Δ = 0` over the realisable feature ranges
rather than sampling randomly. On dynamo-9c93375 this took the survivor set from
four non-proportional triples to one (the exact 2× multiple).

Related: [[dynamo-reconstruction-beats-specification]],
[[dynamo-withhold-an-algorithm-not-a-clause]], [[dynamo-z3-collapses-joint-integer-fits]].
