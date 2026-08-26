---
name: dynamo-declare-the-hour-passat2-actually-gives
description: "Declaring [agent].timeout_sec above 3600 makes pass@2 attribute every near-miss to the harness override, so low_timeout FAILs and no failure counts as valid; setting it to 3600 flipped the gate on the same task."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 297b2cfd-3fd2-40f3-823f-9affe5775359
  modified: 2026-08-25T14:31:12.850Z
---

Measured on `dynamo-7a8c332` (cadence-uplift), 2026-08-25, across six evaluated
heads. `task.toml` declared `[agent].timeout_sec = 5400`. pass@2 pins
`override_timeout_sec = min(declared, 3600)`, so every run got 3600 — and every
analysis report attributed the failing trial to that gap rather than to the task:

> "the run-config override silently removed 25 % of that budget"
> "the override was shorter than the task-specified `timeout_sec`"
> "this makes the zero reward partly a configuration artifact"

The consequence is mechanical, not rhetorical. The `low_timeout` column asks
whether the agent had **enough time**, and the analyser answers "no — the task
asked for 5400 and got 3600". `low_timeout = FAIL` on an `AgentTimeoutError`
trial is classified `timeout_progress`, which counts for nothing, so a genuinely
wrong submission never registers as a valid fail. Three consecutive heads landed
`1 solved · 1 in-progress-timeout` this way, including one whose trial was
**deterministically wrong** (`difficulty_crux: PASS`, `near_miss: PASS`, wrong on
every workspace but two) and one at 63/64.

**Changing one number — 5400 → 3600 — took the same task from blocked to
`1 solved · 1 valid-fail · 0 timeouts · "Rerun Recommended: NO"`**, and the run
went on to pass AVA, deep_review, tier1 and all 37 QC checks.

**Why:** declaring the hour you are actually given makes the verdict honest. An
agent that runs out of clock has had the whole budget its own task asked for, so
the analyser stops blaming the harness and starts grading the work.

**How to apply:** unless the task genuinely needs longer *and you are willing to
lose every pass@2 near-miss to `low_timeout`*, set `[agent].timeout_sec = 3600`.
Check first that the deliverable actually fits: here three trials across three
heads had written a correct migrator inside 3600 s, the fastest in ~44 min, so
3600 was neither tight nor arbitrary. The second benefit is at pass@5, which
honours the file — 5400 there hands a self-correcting agent the extra half hour
it needs to repair the very mistake the traps planted, converting valid fails
into solves. Both of this task's last two near-misses had *found* their own bug
and were applying the fix when the clock stopped.

This refines [[dynamo-pass2-overrides-the-agent-timeout]] (which recorded the
mechanism) with the consequence: the mismatch is not merely cosmetic, it
suppresses the valid-fail classification outright. Related:
[[dynamo-timeouts-anchor-nothing]], [[dynamo-in-progress-timeouts-need-plumbing]].
