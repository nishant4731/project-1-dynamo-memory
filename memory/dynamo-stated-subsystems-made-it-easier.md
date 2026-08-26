---
name: dynamo-stated-subsystems-made-it-easier
description: "Measured on dynamo-7aea78b: adding three fully-stated subsystems took pass@5 from 4/5 to 5/5 solved; only a dated dimension the shipped instance is constant in produced valid fails."
metadata:
  type: project
---

On `dynamo-7aea78b` (Fine tuning), pass@5 went **4 solved/1 valid (avg 0.800)** →
**5 solved/0 valid (avg 1.000)** after I added three whole stated subsystems: a
per-stage domain ceiling, a per-source ceiling, and a token carry across domains
and stage boundaries. All three were real, output-affecting and inert on the
shipped instance. They still made the task *easier* to solve.

The trial analysis named the reason: *"the specification is unambiguous enough
that the implementation is effectively determined by the spec once read
correctly."* Breadth of stated rules is transcription work, and transcription is
what these agents are good at. Confirms [[dynamo-stated-algorithms-are-transcription-too]]
and [[dynamo-widening-implementation-surface-measures-zero]].

What moved it to **1 solved/4 good valid (avg 0.200)** was making sections 4–8
settle **as of a day**, with each stage carrying its own date, licences having
terms that can lapse and be re-granted, and notices having a `lifted_on`. The
whole front half becomes a function of the day and moves in both directions; the
shipped instance settles every stage on the same day, so one global pass is right
there and wrong everywhere else.

**The rule: when pass@5 says too easy, do not add a subsystem. Add a dimension
the shipped instance is constant in.** See
[[dynamo-model-training-and-ml-infrastructure-fine-tuning-playbook]] and the
irrigation-season "dated outages" precedent in
[[dynamo-data-querying-and-databases-sql-querying-playbook]].

Corollary measured on the same task: before shipping anything you are calling a
"closure", check it is reachable. Folding the drift cap into the removal closure
looked like a deep mutual fixed point and measured **inert** — strain is monotone
along edges, so the over-drifted set is already closed downward. It would have
been a QC C3 hole. See [[dynamo-inert-rules-are-c3-holes]].
