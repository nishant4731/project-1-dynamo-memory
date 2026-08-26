---
name: dynamo-recovery-tasks-are-bimodal
description: "Policy-recovery tasks fail as \"solved\" or \"ran out of clock\", almost never \"finished and wrong\" — 14 heads on dynamo-4242b2d oscillated without ever landing the band."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26baa8a5-9e75-43c9-b21a-1b948f75e740
  modified: 2026-08-15T22:35:02.334Z
---

dynamo-4242b2d (exposure-triage-bench, 2026-08-15/16). Fourteen heads. Every
non-difficulty gate went green repeatedly — cosine (0.70/0.83, stable across all
14 pushes), Dynamo eval 31/31, duplicate UNIQUE, validation, deep_review, AVA,
tier1, qc_eval, qc_exec, qc_gate 44/44 — and the difficulty band never settled.

Measured, in order:

| configuration | result |
| --- | --- |
| 37 constants, 386-row ledger | pass@5 0/5, 2 valid + 3 in-progress timeouts (blocked: <3 counted) |
| + I/O plumbing handed over | pass@2 **2/2 solved** |
| + supersession + per-service allowance | pass@2 1 solved/1 valid, then 1 solved/1 timeout |
| + severity×tier witness grid (459 rows) | pass@2 0/2, **both** productive timeouts |
| keying stated instead of witnessed | pass@5 **4/5 solved** |
| + 46 constants, one-pair brackets | pass@2 1 solved/1 timeout, twice |
| + 7200s budget, 3 subsystems starved, 239 rows | pass@2 1 solved/1 timeout, then **2/2 solved** twice |
| + allowance cutting through equal-index ties | pass@2 1 solved/1 timeout, then **2/2 solved** |
| + score censored on 4 codes, backgrounds confounded | pass@2 1 solved/1 timeout, twice |
| + score censored on `below_bar` too (inequality-only evidence) | pass@2 **0/2, both timeouts** |

**Why:** the failure mode of a recover-the-policy task is "hasn't finished
fitting yet", not "fitted it wrong". An agent either separates the constants and
is then byte-exact, or it is still converging when the clock stops — and an
in-progress timeout counts for nothing. Every lever that raises inference cost
buys timeouts; every lever that lowers it buys solves. The band between them is
narrow and the draw is noisy enough to cross it in both directions on the *same*
head.

Two things that did **not** work, against expectation:
- Starving the visible material of three whole stated subsystems (collapse
  rules, a supersession closure, a per-service allowance) — agents implemented
  all three correctly from the notes alone and still solved 2/2. Starving only
  pays when the *natural* reading diverges from the stated one; a rule that is
  merely unexercised but clearly written gets implemented right.
- A tie-break trap built to order: services filled past their allowance at an
  *identical* index, so the rising-id half of the ordering decides who keeps a
  ticket. Measured to make the natural index-only sort wrong on 6 of 14 graded
  drops, invisible from anything the agent can run — and the next two draws
  still solved 2/2. Frontier agents read a stated tie-break and implement it.
  Traps that a careful reader can simply *follow* do not convert solvers; only
  something they must *derive and can get wrong* does.
- Raising `[agent].timeout_sec`. The pre-check caps the agent at 3600s whatever
  task.toml says (the sticky states this outright), so it only moves the trials
  stage — confirming [[dynamo-pass2-overrides-the-agent-timeout]] but making the
  pre-check the binding gate, since it needs a valid fail and can only produce
  timeouts for the slow half.

The censoring lever is the one the platform's own difficulty suggestions asked
for twice, and it worked in the intended *direction* — it defeats "fit every
published index, confirm zero mismatches, stop", which is how both passing
trials won — but the cost lands on the clock, and the pre-check turns clock into
nothing. Solve times sat at 36-58 minutes against a 60-minute cap the whole way,
so any lever that adds inference tips the slow half from "solved" straight to
"no output at all", skipping "finished and wrong" entirely. That is the bind:
for this concept the window where an agent finishes *and* is wrong is narrower
than the noise in a two-trial draw.

**How to apply:** for this mold, budget the whole task so a solver finishes in
~30 of the 60 pre-check minutes, and put every gram of difficulty into readings
that *diverge* rather than into quantity to recover. If two consecutive heads
alternate between all-timeouts and 2/2-solved, stop tuning volume — see
[[dynamo-volume-bound-tasks-oscillate]] and [[dynamo-timeouts-anchor-nothing]].
The pass@2 difficulty suggestions are worth reading but pushed the wrong lever
here: both told me to raise the budget, which the pre-check ignores.
