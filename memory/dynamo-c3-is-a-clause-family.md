---
name: dynamo-c3-is-a-clause-family
description: A Dynamo qc_gate C3 finding names one probe but indicts every stated clause of that kind; fix the family and prove it with guard mutations.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d0dbd568-34b9-46db-9c5f-cf121220beaf
  modified: 2026-08-11T22:12:06.745Z
---

qc_gate C3 blocked `dynamo-19c8cbd` by deleting the duplicate-pin check from the reference and still scoring reward 1. The contract's rejection section listed seven conditions; only four had held-out workspaces, so the prober just picked an uncovered one. The accompanying "minor advisory" (untested advertised behaviour) had the same root cause — that pairing is the tell.

**Why:** C3 iterates stated clauses and crafts a discriminating instance. Patching only the clause it happened to name leaves the rest of the family exposed on the next run.

**How to apply:**
1. Add one held-out workspace per *stated* rejection clause, in the same push.
2. Ship a **guard sweep**: delete each rejection check from the grading oracle and require it to ACCEPT a workspace the true reading rejects. Every guard must flip exactly one workspace.
3. Design each workspace so deleting the check yields a *complete plausible* run, not an unsolvable input — otherwise the guard can't flip. Make the offending item reachable from nothing, or give it a serviceable sibling version.
4. Reproduce the probe verbatim before pushing: delete the exact lines QC named, rebuild, confirm reward 0 and that the failure names the clause.

Pairs with [[dynamo-mutation-sweep-finds-witness-holes]] — assert the anchor build count, not just "0 survivors".
