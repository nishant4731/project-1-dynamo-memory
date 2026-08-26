---
name: dynamo-normalization-needs-a-render-witness
description: A stated normalization rule (unsigned zero, trailing-zero stripping) blocks C3 unless some graded output actually renders a value that exercises it.
metadata:
  type: feedback
---

QC C3 blocked a task whose contract said "negative zero is written 0": deleting that
normalization from the reference still passed, because no shipped or held-out case ever produced
a value whose canonical text would have been `-0`.

**Why:** C3 mutates one stated rule and checks the verifier rejects it. A rule that is stated but
never *rendered* by any graded artifact is unobservable, so the mutant survives and the coverage
counts as hardcodable.

**How to apply:** for every normalization clause in the contract, plant a value that exercises it
in a field the packet actually emits — a sort key, a group key, a bounds value — not merely one
that exists in the input. Pair it with the arithmetic form too (a group whose exact total is
negative but rounds to zero discriminates a naive `quantize` emitting `-0.00`). Add a mutant that
deletes the normalization and confirm it dies. Same shape as [[dynamo-mutation-sweep-finds-witness-holes]]
and the inclusive-boundary lesson.
