---
name: dynamo-stated-invariants-need-a-graded-replay
description: QC C3 fires on any spec sentence about running the program twice unless the verifier actually runs it twice.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26baa8a5-9e75-43c9-b21a-1b948f75e740
  modified: 2026-08-16T18:47:49.566Z
---

QC blocked `dynamo/mend-finding-store` head `b3a99b4` with C3 "Narrow /
Hardcodable Held-Out Coverage" for one sentence: the spec promised "mending a
store that is already mended leaves the shards, the index and the quarantine
exactly as they are", and the verifier mended every store exactly once. The
finding quoted the grep it ran — `no twice/second/idempo`.

**Why:** this is [[dynamo-inert-rules-are-c3-holes]] and
[[dynamo-stated-rules-need-a-divergence-fixture]] applied to a *lifecycle*
rule rather than a parsing rule. QC treats any stated behaviour no graded run
exercises as hardcodable surface, and an idempotency claim can only be
exercised by a second invocation.

**How to apply:** if the contract says anything about re-running, resuming,
or repeating, make `run_on` take a `passes` argument and grade the second
pass. Compare the submitted program's pass-2 tree against its own pass-1 tree
*and* against the reference, and add a companion test asserting the reference
itself satisfies the rule so the promise cannot rot. Restrict the comparison
to exactly what the sentence promises — here shards, index and quarantine, not
the report — or you invent a fresh B1 ambiguity about what the repeat run
should write. Doing this cost ~40 lines and kept the irreversibility trap on
the live store intact (a second mend of it still scores 0).

Paired B1 finding on the same head: the spec used "survivors" for both the
post-journal and the post-collapse population. Give each population an
explicit name in the spec and make every report row point at one by name.
