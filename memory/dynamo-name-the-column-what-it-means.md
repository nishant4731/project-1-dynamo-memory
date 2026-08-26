---
name: dynamo-name-the-column-what-it-means
description: A graded column whose value only the withheld subsystem knows is an undisclosed convention; redefine it structurally instead of disclosing the mechanism.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4ba242f-9e0e-4fb9-ad2a-ae0d21e1b541
  modified: 2026-08-15T04:11:21.591Z
---

Measured on dynamo-e3b1da9, 2026-08-15. A trial **recovered the withheld policy
184/184**, produced byte-exact state, plan and all 23 counters, and still scored
zero — solely on a ledger column, `chain_bytes`. Deep Review blocked the head and
the pass@2 analyser graded that trial `approach_validity: FAIL`, calling it a
spec gap rather than an agent error.

The column was documented as "the total the pass weighed when it considered this
generation on its own account". The verifier wanted the *marginal* cost, which
excludes ancestors already retained; the name and the gloss both read as the
chain's own total. The log recorded only which candidates were retained, never
this value, so nothing agent-visible decided it. The two readings differed on 25
of 80 graded rows.

**Why:** when a subsystem is deliberately withheld, any graded field whose value
depends on that subsystem's internals is by construction underivable. Disclosing
the internals to fix it leaks the crux; leaving it is an undisclosed convention.

**How to apply:** take the third route — redefine the field as something
*structural and derivable from the other artifacts*, so its name matches its
meaning. Here `chain_bytes` became the sum of sizes over the generation's own
chain, computable from `resume_state.json`, and the policy callback stopped
reporting it. That closed the fairness hole without giving away a single rule,
and made the field cross-checkable against the submitted state.

Two corollaries paid for in the same session:
- Removing an informative column **costs mutation coverage**. Four anchors on the
  policy's chain logic went from caught to surviving, because the ledger no
  longer exposed the cost. Fix by building fixtures where the decision changes
  the retained set — including deliberately tiny vaults where a self-referential
  base loops without tripping a count limit — not by retiring the mutants.
- Pair the ambiguity fix with a ratchet aimed only at the recovery, or the fix
  hands out solves: Deep Review said outright the trial "would pass once §8.3 is
  fixed". See [[dynamo-ambiguity-fix-needs-a-paired-algorithmic-trap]].
