---
name: dynamo-irreversibility-does-not-fire-on-a-careful-agent
description: "Evidence consumption graded on the one live copy fired 0/2 — both agents deferred the live run until their tool was validated, so the destructive trap never triggered."
metadata: 
  node_type: memory
  type: project
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T09:32:05.257Z
---

Measured on dynamo-65cf2ab (2026-08-17), rebuilt as `dynamo/quorum-vault-reseat` after the
residue mill hit its ceiling. This was the playbook's **#1 kill lever by historical lethality**
built in its original form, and it did not fire.

The shape: `/app/data/vault` is the *only* copy, its end state is the graded answer, and a
reseating deletes the share tree it works from (protocol says so; reference does it last). A
half-finished tool run on the live vault destroys the seats permanently, and a correct tool
written afterwards finds a finished vault and changes nothing. I verified the mechanic before
pushing — a probe running a buggy draft then the reference scores 0.

**pass@2 came back 2 solved / 0 valid fails.** The trial analysis names the reason directly:

> "Defer the live-vault run until the tool was validated on the actual data."

Both agents did this independently, unprompted. They read the protocol in full, inspected the
vault structure, built the tool, validated it, and only then ran it once on the live copy. One
even self-patched a `UnicodeDecodeError` *before* any live run.

So the destructive trap only catches an agent that experiments on production data, and this model
does not. That matches the earlier c1fed49 measurement (`evidence consumption fired 0/2 — both
tools were right first time`) and makes it two independent confirmations on different concepts.

**Running tally of levers measured against this model on this repo, all fair and fully specified:**

| lever | draws | result |
|---|---|---|
| stated rules + starved instances (3 independent starves) | 7 | all solved |
| irreversibility / evidence consumption on the live copy | 2 | 2/2 solved both times, trap never triggered |

Every valid failure either concept ever produced traced to a gap in my own contract, and closing
each gap fairly returned the task to solved. Both concepts passed every soundness gate — cosine,
static, eval 31/31, duplicate, validation, deep review, AVA — on the rebuild's first push.

**What this means for the next task:** do not reach for irreversibility expecting it to carry a
task, and do not build a fourth sample-starve. See
[[dynamo-sample-starving-does-not-beat-a-general-implementer]]. What remains untested is whether
*any* fair, fully-specified contract in this subcategory can reach the band against this model —
the evidence so far says no, and the decision to keep spending draws is a budget question rather
than a design one.

## Third confirmation, different model (2026-08-22, dynamo-a8b2707)

`dynamo/sentinel-trace` head `7724496` turned a read-only pack into a live ward register:
the transaction folds a pending `intake/` queue, files refusals, **unlinks each batch it
spends**, and the register's end state is graded alongside the reports. I verified the
mechanic in-container before pushing — a second tool run scores 0, and a mis-folded draft
followed by a corrected rerun scores 0.

**pass@2: 2 solved / 0 valid-fail**, ~22 and ~39 min of 60. The analyser's trajectory notes
say both agents implemented the tool, "ran the script against the register and iterated on
failures", and still landed correct — i.e. they never spent the live queue on a draft. The
agent here was **DeepSeek-v4-pro under Terminus-2**, a different model from the 65cf2ab
measurement, which makes this a cross-model confirmation rather than a repeat.

**Updated conclusion:** irreversibility is not a lever against current frontier agents, on
any model measured so far. Do not spend a head on it. What the same task then reached for,
and the only thing the QC-B5 pincer leaves, is a quantity that is **cheap to state and
expensive to compute** — see [[dynamo-b5-vs-pass2-determinability-pincer]]'s closing advice
and the sentinel-trace entry in `PROJECT_MEMORY.md`.
