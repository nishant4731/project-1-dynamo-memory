---
name: dynamo-ambiguity-is-the-only-valid-fail
description: "Measured on dynamo-9df6709: both pass@2 valid fails came from spec ambiguities, and fixing them (as QC requires) removed the failures — 1/2, 2/2, 1/2, 2/2."
metadata: 
  node_type: memory
  type: project
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-12T16:54:40.796Z
---

The salvage mold at full strength — in-place vault mend, evidence consumed as it files, clocks recovered from superseded anchors, digest-driven fragment assembly with decoys, cascading reference eviction, 22 counters, 51 mutations with zero survivors — measured **1/2, 2/2, 1/2, 2/2**. Both valid failures were spec ambiguities ("each such insertion is one resolved collision"; a counter defined as "rows the window left" but read after a later eviction). QC and the trial analyser both require fixing those, and each fix removed the failure with it. The heads with unambiguous specs produced no failures at all, in 14–26 minutes of a 60-minute budget.

**The irreversibility lever fired zero times in four trials.** Every agent copied `/app/vault` to `/tmp` and developed against the copy — including after the prompt stopped prescribing that remedy while still disclosing the hazard. Treat the playbook's caveat ("it fired 0/5 once") as the expected case for current agents.

**Why:** for this reference pair, a fair deterministic pipeline is derivable however many interacting subsystems it carries; ratcheting raises solve time, not failure rate. See [[dynamo-recovered-constants-are-still-transcription]] for the same conclusion reached from the opposite shape.

**How to apply:** before building, ask what could fail a careful agent *without* being ambiguous. If the only honest answer is an obscure convention, that is a rejection waiting to happen, not difficulty — raise the calibration question with the Dynamo team instead of spending three-hour pipelines on ratchets.

**Correction (2026-08-13, `dynamo-6bb0151`): the irreversibility lever does fire.** On
`dynamo/tapline-recut` one of five pass@5 agents ran a clock-buggy tool directly on `/app/case`
at step 22, permanently consumed the spool, and could never recover it — a clean reward-0 valid
fail. The two passing agents both developed against `/tmp` copies first. So "agents always copy
to /tmp" is a tendency, not a law: budget the lever at roughly one kill in five rather than
zero. See [[dynamo-blindness-table-before-pushing]].
