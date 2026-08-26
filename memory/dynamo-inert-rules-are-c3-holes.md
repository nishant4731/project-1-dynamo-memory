---
name: dynamo-inert-rules-are-c3-holes
description: A stated rule whose inputs the graded fixtures can never reach is dead weight the mutation sweep exposes; move the threshold so the rule becomes load-bearing rather than deleting the clause.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d555551c-8ce6-4f22-9ff0-31ffdbae2e56
  modified: 2026-08-14T19:20:20.717Z
---

Measured 2026-08-15 on `dynamo-25a45c7` (`dynamo/atlas-curate`) while building the
first mutation sweep. The charter stated the signed-division convention plainly —
"`//` is floor division, rounding toward negative infinity, and `separation` really
can come out negative" — and the fixtures did carry negative separations. Two mutants
still survived: `separation-absolute` (`abs(pos - neg) // W`) and
`separation-truncates` (`int(x / W)`, truncating toward zero).

**Why:** the admission floor was `+48`, so every negative-separation candidate was
excluded before its value reached any graded byte. Both readings agreed with the
reference on every artifact and on every counter, because `held_below_floor` counts
the candidate either way. The rule was stated, witnessed in the data, and still
completely inert.

**The fix is the threshold, not the clause.** Moving the floor to `-12` put seated
candidates with negative separations into the exhibit, where the value is a graded
field. Both mutants died immediately, and the same move made a third mutant
(`separation-ignores-negatives`) discriminate. Deleting the sentence would have been
the other option and it is worse: it trades a C3 hole for a B1 ambiguity, since a
solver still has to divide negative numbers somewhere.

**The general test, worth running on every stated rule before pushing:** ask which
graded byte changes if the rule is read the other way. If the answer is "none,
because the value is filtered out before it is ever printed", the rule is inert. A
rule can pass "is it stated?" and "does the fixture contain that input class?" and
still fail "does any graded output depend on it?" — that third question is the one
qc_gate's C3 prober actually asks.

Two cheap corollaries from the same sweep:

- **A mutant that hangs is caught, not a defect.** `budget-strict` (`<` for `<=`)
  made a pass seat nothing, so the pass loop never terminated. Give the mutant runner
  a short timeout and treat expiry as detected — it cannot produce the graded bytes
  either. Do not add a termination guard to the reference to make the mutant finish;
  that adds an unwitnessed branch to fix a non-problem.
- **Boundary mutants need equality witnesses that are actually seated.**
  `oversize-strict` (`>` → `>=`) and `support-threshold-high` (`< 2` → `< 3`) both
  survived until the generator planted a dashboard whose cells exactly equal a pass
  budget and a candidate engaging exactly two positive probes. Plant the equality
  case, not merely a case on each side.

Related: [[dynamo-normalization-needs-a-render-witness]],
[[dynamo-c3-needs-a-clause-sweep]], [[dynamo-mutation-sweep-finds-witness-holes]].
