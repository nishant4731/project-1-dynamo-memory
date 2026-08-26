---
name: dynamo-self-verifiable-recovery-never-commits
description: "Measured on dynamo-25a45c7: when a log uniquely determines the withheld policy, agents can always tell they are wrong, so they never stop early — pass@2 at the pinned 3600s yields in-progress timeouts, not countable failures."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d555551c-8ce6-4f22-9ff0-31ffdbae2e56
  modified: 2026-08-16T05:15:09.231Z
---

Thirty-four trials across eighteen draws on one repo, **zero solves ever**, and
pass@2 still blocked most draws. The reason is structural and worth designing
around from the start.

**The mechanism.** QC B5 requires the disclosed evidence to *uniquely determine*
every graded answer. In a policy-recovery task that means the log lets the agent
replay its own hypothesis and see it fail. So an agent holding a wrong reading
*knows* it is wrong and keeps searching. It never reaches the "confidently
wrong, committed, finished" state the gate counts. At a fixed budget it either
solves (rare, if the crux is good) or is cut off mid-search — and
`in-progress-timeout` counts for **nothing**.

This is the exact inverse of the playbook's silent-misread doctrine, where the
model commits to a plausible wrong answer. A self-verifiable corpus removes the
commit. You cannot have both "the evidence pins the answer" (fairness) and "the
agent confidently commits to a wrong answer" (countability) from the same
corpus.

**The measured trap: making the task better made the gate worse.** Countable
failures per draw went 2,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0. Early draws had agents
flailing, which the analyser scored *idle-loop → valid fail*. As the task got
cleaner (plumbing provided, log reordered, shape disclosed) agents converged
steadily, which scores *still-progressing → uncounted*. Improving convergence
moved trials out of the counted bucket.

**Do not respond by adding difficulty.** The analyser said outright: "the
difficulty is genuine and correctly placed… no task or verifier fix is
warranted." Adding work pushes more trials past the wall, so the gate gets
strictly harder to clear. Every lever that helped was *removal*: hand over the
fully-specified pipeline as working code, cut per-hypothesis replay cost, put
the decisive calibration pools first in the log, disclose the ranking's *shape*
(lexicographic, five terms) while withholding its content.

**The budget asymmetry that decides it.** pass@2 pins the agent to
`override_timeout_sec=3600` no matter what `task.toml` says; `trials` honours the
configured value. So a task calibrated for 7200s can never demonstrate itself at
pass@2 — and pass@2 gates pass@5. The analyser itself called this "a systematic
configuration error" and twice quoted the task's own comment back as
corroboration. If a concept needs more than an hour to *finish*, that is a
design constraint, not a tuning knob.

**How to apply.** Before committing to a log-recovery concept, ask: after the
agent has the wrong answer, what makes it *stop*? If the answer is "nothing,
it can always test another hypothesis", expect uncounted timeouts and pick a
different shape — or bound the hypothesis space so tightly that exhausting it
inside the budget is the natural end. Related:
[[dynamo-reconstruction-beats-specification]] (why the shape is attractive),
[[dynamo-timeouts-anchor-nothing]], [[dynamo-pass2-overrides-the-agent-timeout]],
[[dynamo-provide-the-plumbing-clears-the-hard-side]].
