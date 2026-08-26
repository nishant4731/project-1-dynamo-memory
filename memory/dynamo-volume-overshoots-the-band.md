---
name: dynamo-volume-overshoots-the-band
description: "pass@2/pass@5 can fail from the HARD side as in-progress timeouts; the fix is cutting non-crux volume, not difficulty."
metadata: 
  node_type: memory
  type: project
  originSessionId: e307434b-d33f-4bea-929c-c49841bc266d
  modified: 2026-08-14T05:40:50.081Z
---

A task can miss the accepted band from the *hard* side, and it does not look like
difficulty — it looks like `in-progress-timeout`. On dynamo-137a569 the trajectory
was 4/5 solved (too easy) → ratchet → 1/5 solved, 2 valid fails, **2 in-progress
timeouts** → 0/2 at pass@2, both in-progress timeouts. In-progress timeouts count
for nothing: the gate needs ≥3 counted fails with ≥1 valid, and a trial that was
still making progress at the buzzer is neither a solve nor a fail.

The pass@ analysis names the cause precisely. Read it. Ours said one trial burned
1426 s across three consecutive `effort:high` reasoning calls and never wrote a
file, and the other reached 21/29 tests, identified its own bug at step 38, and
was killed mid-fix. The pipeline's stock advice is "raise `[agent].timeout_sec`",
which is useless once you are at the 3600 s cap.

**Why:** the budget is spent on total work — spec reading plus typing plus
debugging — while the difficulty only lives in the crux. Volume and difficulty are
independent axes, and volume is the one that produces timeouts. This is the
converse of [[dynamo-spec-mold-caps-at-80pct-solve]] (volume raised solve time
19→47 min but produced no extra failures): if volume does not buy failures, it can
only buy timeouts.

**How to apply:** when trials time out while progressing, cut the non-crux volume
and keep every trap. The clean lever is to *provide* the tedious part as a
read-only module in the agent image — for us `/app/mshio.py` with both file
formats, the output byte layout, JSON conventions and the digest, i.e. three of
the charter's six sections — so the deliverable drops (486 → 376 lines) and two
spec sections become skimmable, while the exact-arithmetic crux is untouched.
Cross-check the cut against the last pass@5 fail reasons: every genuine failure
there (always-zero counter, 1-ULP fold, transposed fma argument, decimal exponent
loop) must still be reachable, or you have cut difficulty instead of volume.

Stage the provided module into each graded run from the verifier's own protected
copy so a submission is graded against what it was given; say so in the
instruction and the module docstring and enforce it with 0444, otherwise an agent
that extends the module fails for a non-crux reason. Leave writing your own I/O
viable — the naive-program probe of [[dynamo-blind-branch-shipped-fixture-proof]]
does exactly that, which is also the proof it stays viable.

**Outcome (2026-08-14).** The volume cut was necessary but not sufficient, and the full arc on
`dynamo-137a569` is the useful record — five heads, each blocked for a different reason:

| head | change | result |
|---|---|---|
| 1 | full volume, trap narrated | 1/5 solved, 2 valid, **2 in-progress timeouts** |
| 2 | counters 19 → 10 | 0/2, **both in-progress timeouts** |
| 3 | byte-level I/O provided as a module | 1/2, 1 timeout |
| 4 | trap narration removed | **2/2 solved** |
| 5 | + withheld algorithm recovered from an archive | **2/2 solved** |
| 6 | + three sampling-point counters | **1/5, 4 valid fails, ALL-GREEN** |

Heads 1–3 are the timeout side, head 4–5 the too-easy side. The band is narrow because
transcription-under-a-clock is bimodal: an agent either finishes a stated charter correctly or
does not finish. Volume moves *which* of those two happens and never produces the third outcome.
Only [[dynamo-sampling-point-counters-beat-the-ceiling]] produced finished-and-wrong.
