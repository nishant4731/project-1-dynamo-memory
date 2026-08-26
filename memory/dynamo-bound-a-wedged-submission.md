---
name: dynamo-bound-a-wedged-submission
description: "A submission that hangs your verifier is scored infra/setup-timeout — your fault, not theirs. Bound each graded run and refuse the rest once one wedges."
metadata:
  node_type: feedback
  type: feedback
---

A reward-0 trial on `dynamo-d8a8539` had **every rubric column PASS** —
task_specification, reward_hacking, difficulty_crux, near_miss, refusals,
low_timeout, approach_validity — and was still thrown away, booked as
`infra/setup-timeout`. The agent's exponential DFS hung the renderer; the
per-run timeout was 300s and there were 32 graded runs, so it consumed the whole
900s verifier budget **before pytest wrote a single assertion**. A verifier that
produces no output reads as the task's problem, not the submission's.

**Fix, and it is worth real points:**

1. Set the per-run timeout from what the reference actually costs, not from
   caution. Reference: 0.26s on the heaviest network → 30s means "will never
   finish", not "is slow".
2. **Once one run wedges, refuse every remaining run.** A renderer that cannot
   draw one network has already failed; grinding through thirty more only
   converts a plain failure into a verifier timeout.

After this the same failure mode was analysed as "triggers the verifier's
`_WEDGED` guard, cascading remaining tests into instant failure" and counted as
a **good valid fail**. pass@5 finished 1 solved / 4 good valid / **0 timeouts**,
avg 0.200, ALL-GREEN.

Pin it with an attack probe: a renderer that loops for ever must score 0 *and*
the suite must finish well inside budget (ours: 184s, not 900s).

Related: [[dynamo-state-an-optimum-not-an-algorithm]] (which makes agents write
the hanging code in the first place), [[dynamo-timeouts-anchor-nothing]].
