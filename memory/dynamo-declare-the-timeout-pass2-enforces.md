---
name: dynamo-declare-the-timeout-pass2-enforces
description: "pass@2 pins override_timeout_sec=3600 whatever task.toml says; declaring 5400 makes low_timeout FAIL on the conflict. Declare 3600."
metadata:
  node_type: memory
  type: feedback
---

pass@2 runs the agent under **`override_timeout_sec = 3600` regardless of
`[agent].timeout_sec`**. `task.toml` is honoured at pass@5, not at pass@2.

On `dynamo-d8a8539` this cost a whole cycle. pass@2 came back 1 pass / 1 fail
with `difficulty_crux` **PASS** and every other criterion 2/2 PASS — a healthy
result — but `low_timeout` **FAILED**, and its complaint was the *conflict*:
"the override (3600s) conflicts with the task.toml spec (5400s) and directly
contributed to the only failing trial", the failing agent having been mid-fix at
the cut. Setting `[agent].timeout_sec = 3600.0` turned pass2 green with no other
change.

**Why:** the criterion is not "the agent needed more time", it is "the task
promised a budget the agent was not given". A declared budget larger than 3600
is a defect the analysis will find whenever a trial times out.

**How to apply:** declare `[agent].timeout_sec = 3600.0`, and calibrate the task
so a competent agent finishes well inside it — on this task the passing trial
took ~39 min of the 60. Do not declare 4200-5400 hoping pass@2 will honour it.
The advisory sticky may tell you to "re-run pass@2 with the timeout set to the
task-specified value"; that config is the harness's, not yours.

Sharpens [[dynamo-pass2-overrides-the-agent-timeout]]. Related:
[[dynamo-timeouts-anchor-nothing]], [[dynamo-in-progress-timeouts-need-plumbing]].
