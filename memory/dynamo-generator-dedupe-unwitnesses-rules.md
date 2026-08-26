---
name: dynamo-generator-dedupe-unwitnesses-rules
description: A dedupe key in the fixture generator silently deleted the only witness for a stated contract rule; audit shipped data against every clause the contract states.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78170f0c-ffe4-4520-83b2-fd6ece737755
  modified: 2026-08-14T20:04:28.929Z
---

On `dynamo-b296f2d` (tollgate-adjudicate) the charter stated "a grant is keyed by
`(principal, enclave, role)`; a triple may appear more than once with different validity
spans", and the screening rung read "rows exist for that triple, but **none of them**
covers the opening tick". The generator ended with a dedupe that keyed on the triple and
dropped later rows, so **every shipped window had exactly zero triples with two spans** —
the `any()` was never load-bearing anywhere in the graded corpus.

The mutation sweep did not catch it: single-span grants still exercised the inclusive
bounds, so `valid_from <= tick` and `tick <= valid_to` mutants both died. Only a direct
audit of the shipped data against each clause of the contract found it.

**Why:** QC C3/B6 delete or block any rule the graded fixtures never exercise, and a
generator's own bookkeeping (dedupe, sort, "clean up" passes) is invisible to a mutation
sweep because it changes the *inputs* rather than the reference logic.

**How to apply:** after materialising fixtures, walk every noun and quantifier the
contract states ("may appear more than once", "at least one", "either ... or") and count
its occurrences in the shipped data. Any clause with a zero count is either an unwitnessed
rule to fix by adding a witness, or a clause to delete. Then add the mutant that the new
witness kills — here, `grants[0]` instead of `any(grants)` — so the coverage cannot
regress. See [[dynamo-stated-rules-need-a-divergence-fixture]] and
[[dynamo-c3-needs-a-clause-sweep]].
