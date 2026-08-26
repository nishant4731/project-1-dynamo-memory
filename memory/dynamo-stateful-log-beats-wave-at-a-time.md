---
name: dynamo-stateful-log-beats-wave-at-a-time
description: "When an inferred-policy task solves 2/2, make one recovered constant span consecutive logged records — it costs the solver no typing and breaks the \"each line is an independent labelled example\" approach."
metadata: 
  node_type: memory
  type: project
  originSessionId: aa56c786-6506-4eba-8d63-1aad69d56fde
  modified: 2026-08-14T23:55:13.902Z
---

dynamo-229910c (`palisade-vet`) went 2/2 solved at 21 and 48 minutes. Both
pass@2 trajectories used the same method, and the analyser said so: *"treat each
line as one labelled example"*, brute-force the order and the three limits,
done. A per-record policy small enough to enumerate is enumerable.

**The ratchet that costs implementation nothing:** change one recovered limit
from a property of a single record to a property of a record **and the one
before it** (here: a module's seats capped across a wave and its predecessor,
rather than within a wave). Four lines to implement once known. But the logged
waves stop being independent examples — a policy fitted a record at a time fits
nothing — so the solver must group the log by lane, read it in order, and carry
state forward.

This is the right shape when `low_timeout` is a live risk
([[dynamo-provide-the-plumbing-clears-the-hard-side]]): difficulty that adds
*recovery depth* without adding *typing* does not push trials over the wall the
way volume does. Pair it with a compensating disclosure that shrinks the search
— here §4 started naming the five quantities the order draws from, keeping back
only their arrangement and directions — so the budget goes on inference.

Verifier side: the rival "limit confined to a single record" must be an
explicit neighbouring reading the log contradicts, and the survivor search needs
the reach-back as a searched dimension, not a constant. See
[[dynamo-log-consistent-readings-must-agree]].
