---
name: dynamo-in-progress-timeouts-need-plumbing
description: "pass@5 0/5 avg 0.000 still BLOCKS when 3 of 5 are in-progress timeouts; the fix is handing over the non-discriminating I/O layer, not cutting traps."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26baa8a5-9e75-43c9-b21a-1b948f75e740
  modified: 2026-08-14T22:33:56.034Z
---

Measured on dynamo-4242b2d (exposure-triage-bench, 2026-08-15). Head 1 drew
pass@2 0/2 (1 good-valid + 1 in-progress timeout, `difficulty_crux` PASS on
both) and then pass@5 **0/5 solved, avg@5 0.000 — and still blocked**: the
breakdown was 2 good-valid-fail + 3 in-progress-timeout, and the gate needs
**>=3 counted fails**, which in-progress timeouts are not.

The trial analysis named the cause outright: every agent converged on the right
strategy, none lost on the crux, and three were still making forward progress
at the 3600s cutoff (`low_timeout` FAIL). One trial that *did* finish recovered
all 34 constants and the 10-rung order and failed only on omitting `!` from its
comparator character class — the ideal valid fail.

**Why:** avg 0.000 reads like the best possible band and is not. Read the
breakdown line, not the pass fraction: an agent that runs out of clock is worth
nothing, so a task can be simultaneously "nobody solved it" and "not hard
enough" purely because the work does not fit the hour.

**How to apply:** when the fail reasons say agents converged but ran out of
time, do not add difficulty and do not cut traps. Ship the mechanical half as a
read-only module in the agent image — parsing, canonical serialisation, the
ordering rule, the report counters — everything that no failing trial lost on.
Keep the inference (the recovered policy, the arithmetic with blind readings).
Pin the module by digest and drive it in a child process over the reference's
own rows, asserting byte equality on every graded instance, so the layer the
agent is invited to reuse can never drift from the layer it is graded against;
and assert the module names no policy constant. See
[[dynamo-timeouts-anchor-nothing]] and
[[dynamo-provide-the-plumbing-clears-the-hard-side]].
