---
name: dynamo-canonical-spelling-needs-witnesses
description: A stated input-format rule with no corrupt fixture is a QC C3 block — every parsing rule needs its own refusal witness.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 589469b6-5088-434c-a2be-3e8b63665d9f
  modified: 2026-08-11T23:28:53.450Z
---

QC C3 blocked `dynamo-0a072a0` on a rule I had written into the protocol and
implemented in the reference but never fed a fixture: integer fields are spelled
canonically (no padding zeros, `-0` illegal), and a wrongly spelled field makes
the run unusable. The prober mutated the reference to drop that check, and the
verifier still paid reward 1 — because no graded run ever carried a badly spelled
integer.

**Why:** C3 asks "could a submission skip this rule and still pass?" A rule that
only ever fires on inputs you never ship is free to delete. Prose in the contract
plus code in the reference is not coverage; only a fixture is.

**How to apply:** when the contract states a *parsing* or *well-formedness* rule
— canonical integer spelling, header text, field count, trailing newline, path
safety, range bounds — ship one refusal fixture per rule, and split the reference
so each rule is a separately mutable anchor. Then prove it: the mutation sweep
must catch the deletion of each rule on its own. Same pass caught a B1 finding on
a reuse rule that was undecided when a value matched *several* earlier records;
name the tie ("the earliest in processing order, never the most recent") and add
a witness with two later matches.

Related: [[dynamo-mutation-sweep-finds-witness-holes]],
[[dynamo-aggregate-evidence-pins-curves]].
