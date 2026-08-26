---
name: dynamo-stated-rules-need-a-divergence-fixture
description: QC blocks rules that are stated but never exercised at the point two readings diverge; construct the witness and measure 0/7 to 7/7.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7110d418-8520-45e1-942a-0fd9ba7507cb
  modified: 2026-08-14T12:25:33.699Z
---

A rule can be stated plainly in the agent-visible notes and still be **ungraded**,
because no fixture exercises the point where a wrong reading differs. QC calls
this "Narrow / Hardcodable Held-Out Coverage" and blocks on it.

**Why:** three consecutive QC blockers on dynamo-7e6bfa7 were this exact species —
an undefined eviction victim (a registered-first rival reproduced both archived
runs exactly), a collision ordinal only ever reaching `~2` (so misplacing it from
the third collision on graded as correct), and a rounding tie-break where every
probe rounded strictly up or down so `>=` and `>` agreed everywhere.

**How to apply:** for every stated rule, build the fixture where the readings
diverge, then measure the mutation caught 0/7 before and 7/7 after. Note the
witness must *survive to the graded artifact* — a rejected or evicted ticket
grades nothing, and the lane budget silently evicts witnesses
([[dynamo-witness-must-be-the-selected-value]]). Keep a test pinning the set of
lesions the archive cannot distinguish, so a new one cannot appear unnoticed.
