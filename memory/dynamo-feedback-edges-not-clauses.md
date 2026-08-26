---
name: dynamo-feedback-edges-not-clauses
description: "Three heads of sharper clauses solved 2/2; adding feedback edges between pipeline stages drew the first valid fail. Blindness breadth measured zero."
metadata:
  node_type: memory
  type: feedback
---

On `dynamo-d8a8539` (byte-exact chart renderer) three consecutive heads tightened
and added *clauses* and all measured **2/2 solved, `difficulty_crux: NA`**. The
blindness table grew 32/57 → 39/66 single-change misreadings invisible on the
shipped sample across those heads and **pass@2 did not move at all**.

What converted a solver was turning a linear pipeline into a **fixed point**:
scaling → annotation gained an edge back (a crowded band raises its ladder and
re-settles), and then page geometry → annotation gained one too (labels that
still do not fit reserve a margin, which narrows the plot, which moves every
point, which changes which labels fit). pass@2 went to **1 solved / 1 failed with
`difficulty_crux` PASS**, the failing agent's 23 failing tests being exactly
those loops.

**Why:** an agent transcribes clauses accurately however many there are. It does
not spontaneously invert control flow. A feedback edge is a structural property
of the program, not a fact to copy — and the natural implementation order
(compute the thing, then use it) is the wrong one.

**How to apply:** ask which stage's *output* could legitimately change an earlier
stage's *input*, and make it. Then starve the shipped sample so the loop never
fires there — [[dynamo-9b8a04d-rebuild-wave-dispatch]]. Prefer a **monotone**
closure so it terminates without an arbitrary cap (an unreachable cap is an
unwitnessed C3 clause). Budget for the fact that the natural misreading of a
monotone rule often does **not halt**: give every mutant-running tool a deadline.

Contrast [[dynamo-widening-implementation-surface-measures-zero]] — breadth of
blindness is not difficulty. See
[[dynamo-data-science-and-reporting-data-visualization-playbook]].
