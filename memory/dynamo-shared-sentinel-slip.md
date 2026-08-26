---
name: dynamo-shared-sentinel-slip
description: "Differential fuzzing between your engine and your referee cannot catch a design slip both share — QC's A6 prober can."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e16f2925-7e62-47aa-847e-41b5cce5d5aa
  modified: 2026-08-11T21:43:46.814Z
---

400 randomised cross-checks between the reference engine and the protected referee found zero
divergence, yet QC A6 still found a real oracle bug: both implementations used Python `None` as
both "no bound set yet" and "the clause value is genuinely JSON null", so a `gt null` bound
silently became an unbounded scan.

**Why:** a differential check only proves the two implementations agree. When the same author
writes both, they share design decisions — especially sentinel choices, default arguments, and
"empty means absent" conventions — so agreement proves nothing about correctness on the classes
where the shared assumption is wrong.

**How to apply:** before pushing, enumerate every value in the contract's own domain that could
collide with an in-band sentinel (`None`/null, empty string, empty list, zero, missing key) and
write a probe for each one explicitly. Prefer an out-of-band sentinel object over `None` whenever
a graded value may legitimately be null. Treat "my two implementations agree" as necessary, not
sufficient — see [[dynamo-mutation-sweep-finds-witness-holes]].
