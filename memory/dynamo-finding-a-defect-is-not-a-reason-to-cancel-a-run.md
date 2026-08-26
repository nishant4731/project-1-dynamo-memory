---
name: dynamo-finding-a-defect-is-not-a-reason-to-cancel-a-run
description: "Spotting a real defect mid-pipeline is not a reason to push; the fix can wait for the run to settle, and pushing cancels every gate that has not reported yet."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T13:11:04.806Z
---

On dynamo-65cf2ab PR #5 (2026-08-17) pass@2 passed on head `b7a530c`, and while reading the trial
detail I found that the specification quoted worked examples the engine does not produce — a real
defect that had cost both agents their hour. I pushed the fix immediately.

`deep_review` and `ava_review` had posted "⏳ running…" **twenty seconds earlier**. The push
cancelled them. Cost: deep review, AVA, tier1 and the whole QC tier never reported on that head,
a pass@2 draw was spent from the daily six re-running the same gate, and a full cycle of
wall-clock went. The user challenged the push and was right to.

`concurrency: dynamo-review-<pr>` has `cancel-in-progress: true`. Any push cancels everything
still in flight, so the cost of pushing is not "one more run", it is **every gate that had not yet
reported**.

The rule was already written in AGENTS.md and the playbook — harvest all feedback before editing;
never push while trials are live — and I broke it anyway, because finding a bug felt like a reason
to act now. It was not. The defect was static: nobody else was going to hit it in the next twenty
minutes, and the run had information to give that I then had to do without.

**How to apply:** when a defect surfaces mid-run, write it down and keep working locally. Push only
after every check has settled, bundling the fix with whatever the remaining gates surfaced. The one
case that might justify cancelling is a defect that would make an expensive downstream gate produce
actively misleading recorded data — and even then, weigh it against the gates being thrown away,
because a superseded pass@5 costs less than losing deep review, AVA and QC.

Related: [[dynamo-block-replacement-swallows-earlier-edits]] and
[[patch-scripts-need-readback]] — the defect itself was another hand-written artefact that
diverged from the engine.
