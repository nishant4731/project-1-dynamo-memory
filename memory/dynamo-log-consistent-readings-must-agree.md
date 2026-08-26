---
name: dynamo-log-consistent-readings-must-agree
description: "For an inferred-policy task, assert every reading consistent with the log plans the graded instances identically — stronger and more honest than \"exactly one reading survives\"."
metadata: 
  node_type: memory
  type: project
  originSessionId: aa56c786-6506-4eba-8d63-1aad69d56fde
  modified: 2026-08-14T23:55:00.636Z
---

On dynamo-229910c (`palisade-vet`) the fairness test for a withheld policy
started as "search every ordering of the policy's fields; exactly one survives
the log". Deep Review blocked it anyway: the charter invited a field
(`attempt`) into the order that the log had no column for, so an
`attempt`-inclusive order fitted all 189 logged waves and still lost every
graded cycle. The benchmark near-miss trial was exactly that reading.

The uniqueness assertion could not have caught it, because it only searched the
fields already known to be used.

**The property to assert instead:** enumerate every arrangement, direction and
subset of *all* the quantities the contract lets the policy read, keep the ones
that reproduce every logged wave, and require **each of those** to reproduce
the reference's own decisions on every graded instance. Measured on this task:
31 readings fitted the log, **6 of them diverged** on a graded cycle. After two
purpose-built calibration lanes, 13 fitted and **0 diverged**. Later, after a
ratchet, exactly 1 fitted and 0 diverged.

Two consequences worth keeping:

- Readings that append unreachable keys *after* a totalising tie-break are
  equivalent, not rival — a uniqueness test reports them as failures and sends
  you chasing nothing. The agree-on-graded-instances test is indifferent to
  them, which is correct.
- When a reading does diverge, the fix is a **calibration lane**, not a charter
  narrowing. Narrowing deletes the inference; see
  [[dynamo-ambiguity-fix-needs-a-paired-algorithmic-trap]].

Related: [[dynamo-reconstruction-beats-specification]],
[[dynamo-withhold-an-algorithm-not-a-clause]].
