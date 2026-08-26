---
name: dynamo-repair-mold-beats-recovery-ceiling
description: "The salvage/repair mold drew pass@2 0/2 with 2 stratified valid fails on head 1, where 23 heads of the recovery mold could not stop solving."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26baa8a5-9e75-43c9-b21a-1b948f75e740
  modified: 2026-08-16T18:47:36.231Z
---

Task `dynamo/mend-finding-store` (repo dynamo-4242b2d-security, PR #2, head
`b3a99b4`, 2026-08-16) scored **pass@2 0/2 solved, 2 valid-fail, 0 timeouts,
0 task/verifier-issue**, rubric all PASS except one `near_miss` FAIL, failures
stratified with no shared root cause. `pass2_suggestion` skipped. This is the
first head in this repo to clear pass@2 on its first try.

The same repo's previous task ([[dynamo-reconstruction-mold-hit-its-ceiling]],
[[dynamo-recovery-tasks-are-bimodal]]) spent 23 heads oscillating between "2/2
solved in 40 min" and "all timeouts", because inference difficulty and
inference *time* are the same axis and pass@2 pins the agent at 3600s.

**Why:** in a repair task, being wrong is *cheap and fast*. The agent finishes
in 20 minutes and fails on byte-level exactness, so it lands in the only
outcome the gate counts — finished and wrong — instead of skipping from
"solved" straight to "no output".

The two measured failure modes were exactly the designed ones:
- an unsound early-exit (`if not journal and not staging: return`) that fired
  on the three held-out stores with neither directory;
- running the program twice on the live store, spending the evidence and
  overwriting the report with all-zero counters, *after* acknowledging the
  instruction's warning not to.

**How to apply:** when a recovery/reconstruction task keeps solving or keeps
timing out, stop tuning it. Port the subject matter to a repair mold: hand over
a complete written contract (nothing to infer), put the failure surface in
exactness and irreversibility, and make one graded copy the only copy.
See [[dynamo-c1fed49-chartvault-all-green]] for the mold this replaced.
