---
name: dynamo-widening-implementation-surface-measures-zero
description: A stated, witnessed, re-keying subsystem drew 0 of 5 failures; agents implement stated rules correctly however far they reach.
metadata:
  type: project
---

dynamo-9c93375 head d08d500. Added a subsystem chosen off the playbook's "the
rule that breaks a deadlock RE-KEYS the whole algorithm": a value's corroboration
is counted within the station's own class when that class has >=3 ONLINE
stations, field-wide when thinner. It feeds admission, the withheld score's
backing term and backing_peak, so it reaches every graded byte.

Pre-push blindness table over the ten graded fields:
- missing the rule entirely: wrong on 9/10
- counting all class stations instead of the online ones: wrong on 3/10
- ignoring the thin-class fallback: wrong on 3/10
(the latter two miss on the VISIBLE field, and no reseated answer is published,
so all three are silent)

Then pass@5 drew **4 solved / 1 valid fail, and the one fail never reached
implementation**. All four solvers implemented the re-key correctly. As a
difficulty lever it measured exactly zero.

It cost nothing either - green at cosine, validation, pass2, ava_review,
deep_review, tier1, qc_eval, qc_exec, qc_gate - so it stays as a real stated
subsystem. But the lesson generalises with
[[dynamo-stated-algorithms-are-transcription-too]] and
[[dynamo-sample-starving-does-not-beat-a-general-implementer]]: a wide blindness
table predicts what a WRONG implementer produces, not how likely a frontier agent
is to be wrong. Breadth of consequence is not difficulty. Only the withheld
subsystem moved this task's numbers.

Operational note from the same push: re-keying a global quantity un-witnessed six
existing mutation anchors (3 survived every field, 3 fell to one field). The
corpus is deterministic from per-slot seeds, so the fix was to measure each
candidate seed's kill set and pick a covering assignment - see
[[dynamo-generator-dedupe-unwitnesses-rules]].
