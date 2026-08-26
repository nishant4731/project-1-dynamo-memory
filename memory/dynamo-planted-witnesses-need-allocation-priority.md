---
name: dynamo-planted-witnesses-need-allocation-priority
description: Purpose-built fixture witnesses compete for room; allocate the fragile ones first and share a value when only the label differs.
metadata: 
  node_type: memory
  type: project
  originSessionId: 858c7146-cad6-4d04-a6cb-b2b908e4341d
  modified: 2026-08-14T19:20:44.857Z
---

When a generator plants one discriminating witness per decision boundary, the
witnesses compete for the same finite fixture room (free slots, and stations
still available to plant a backing count on). The ones built last silently fall
back or fail to allocate — the mutation sweep then reports them as "caught by a
single fixture only", which reads like a coverage hole but is really an
allocation-order bug.

**Why:** a sweep that passes on the full corpus can still fail inside the
verifier, which only sweeps a subset of fixtures. Measured on dynamo-9c93375:
three tie-break mutants were killed by 1 of 6 verifier fixtures and by 10 of 10
locally; simply moving those witnesses to the front of the generator took them
to 8-10 of 10 with no other change.

**How to apply:** (1) build the witnesses whose mutants are hardest to kill
*first*, before the bulk blocks that consume room. (2) Give the slot allocator an
explicit `room=N` requirement so a witness never claims a slot it cannot then
plant against. (3) Where two offers differ only in a *label* the output records
(an origin column, a provenance tag), give them the **same value** so they share
one planted backing count — this cuts the room a witness needs in half and keeps
it allocatable on the small fixtures. (4) Run the local sweep against exactly the
fixture subset the verifier sweeps, not the full corpus.

Related: [[dynamo-mutation-sweep-finds-witness-holes]],
[[dynamo-witness-must-be-the-selected-value]], [[dynamo-fixtures-must-survive-the-image]].
