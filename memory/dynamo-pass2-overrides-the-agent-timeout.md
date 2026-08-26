---
name: dynamo-pass2-overrides-the-agent-timeout
description: "pass@2 pins the agent run to 3600s via override_timeout_sec regardless of task.toml; the trials stage honours the configured value, so the two stages must be calibrated separately."
metadata:
  type: feedback
---

Measured on `dynamo-379e527` (2026-08-14). The pass@2 trial analysis said it outright:

> The root cause is structural: `override_timeout_sec=3600` in `result.json` for both
> trials, while `task.toml` specifies `agent.timeout_sec=7200`. Both agents were given
> half the time the task author intended.

**Two corrections to what I had written down.**

1. `[agent].timeout_sec = 7200` is **valid config** — `review / review` passes it, and the
   static "timeouts within the cap" check does not reject it. My note that "raising above
   3600 does nothing" was half right: it does nothing *for pass@2*, which overrides the
   run, but the `trials` (pass@5) stage honours it. The platform's own difficulty
   suggestion recommends 5400–7200, and the repo README's remedy for a still-making-
   progress timeout is "raise the agent timeout".
2. Therefore **the two gates need separate calibration.** pass@2 asks "is this failable in
   one hour"; pass@5 asks "is this failable in `timeout_sec`". A reconstruction task sized
   for the larger budget will keep drawing in-progress timeouts at pass@2, and those are
   *not countable* — the breakdown line separates `valid-fail` and `soft-timeout-fail`
   (both count) from `in-progress-timeout` (does not).

**The trap this creates:** tuning the task down until pass@2 yields countable failures
de-tunes the stage that actually decides acceptance. Across 11 trials here the split was
2 solved, 2 countable fails, 7 in-progress timeouts — the timeouts, not the difficulty,
were the binding constraint. When every draw says `Rerun Recommended: YES` and
`difficulty_crux`/`approach_validity` are unanimously PASS, the draw is variance: redraw
with a difficulty-neutral push (a README note outside `task/` never enters the agent
image) rather than cutting the crux again. Related:
[[dynamo-operational-passat-failures]], [[dynamo-spec-mold-caps-at-80pct-solve]].
