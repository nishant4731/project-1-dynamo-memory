---
name: dynamo-recovered-set-must-be-a-proper-subset
description: A digest/checksum subsystem that must be search-recovered is dead code unless the hidden set is a strict subset of the visible candidates.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eac1eec9-b2d0-4fc2-b475-c921b4661fbe
  modified: 2026-08-13T20:03:48.712Z
---

Measured on `dynamo-6e8e4c7` (`dynamo/tessera-reconcile`, 2026-08-14). A replica in
the dump could answer with a **sketch** — a count plus a salted SHA-256 over the dots
it holds — instead of a version listing, so the agent has to recover the held set by
searching subsets of the dots the other replicas listed.

The first build placed every sketch on a key that ended with a full broadcast, so all
replicas held the same set. That made `count == len(listed)` on **17 of 17** sketched
buckets: the naive reading "a sketch holds whatever the others listed" reproduced the
reference exactly, and the whole subset search was dead code. The mutation
`recover_sketch(...) -> set(versions)` survived the sweep.

**How to apply:** whenever a subsystem exists to make the agent *search*, assert in the
generator that the hidden answer is a **strict** subset (or otherwise a proper
restriction) of the candidate space, add a coverage property counting the strict cases,
and add a mutation anchor for each naive shortcut ("empty", "everything", "the first
one") rather than only for the deletion of the rule.

Two related traps found in the same sweep:

- A canonicalisation rule inside the digest (`sorted(dots)`) is unobservable when the
  reference enumerates candidates in already-sorted order. Enumerate in **reverse**
  order so the sort is load-bearing, and ship subsets of size ≥ 2. See
  [[dynamo-normalization-needs-a-render-witness]] for the same shape on rendering.
- A `[::-1]` mutation of a container order is not adversarial: on four separate
  fixtures the reversed bucket order happened to produce the same eviction order as
  sorted. Use `sorted(..., reverse=True)` so the mutant is deterministically different.

Related: [[dynamo-mutation-sweep-finds-witness-holes]], [[dynamo-blind-sample-branch]].
