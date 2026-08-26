---
name: dynamo-volume-bound-tasks-oscillate
description: "When a task's difficulty comes from rendering volume, pass@ oscillates between timeouts and 2/2 solves and no amount of volume tuning finds the band."
metadata: 
  node_type: memory
  type: project
  originSessionId: 00684352-c7dd-44b6-bc7c-8ad46b0a358c
  modified: 2026-08-14T10:16:58.346Z
---

Measured on `dynamo-ce5b6ea` (quayside-settle) across seven pass@2 draws and one
pass@5 on one concept:

| shape | outcome |
|---|---|
| heavier (4 artifacts, 33 counters) | pass@2 1 solved/1 valid fail; **pass@5 2 solved, 3 in-progress timeouts** |
| lighter (wave axis cut) | **2/2 solved** |
| middle (class block back) | 1 solved/1 timeout, twice running |
| lighter still (16→12 columns) | **2/2 solved**, both at 57–58 min |

**Why:** the charter stated every rule, so an agent with enough clock gets
everything right. Difficulty was coming from "can you type ~600 correct lines in
an hour", not from reasoning. Tuning volume only moves agents across the
finish-the-hour line: too heavy and they time out (which counts for nothing),
light enough and they finish and solve. There is no volume that lands an anchor
fail, so the search has no fixed point. The blindness table read 20 of 31
misreadings invisible on the shipped fixture and it did not help — blind
branches only catch a solver who *guesses*, and a solver who reads a complete
charter does not guess.

**How to apply:** treat "failures are all in-progress timeouts" and "2/2 solved"
alternating across heads as the signature of a volume-bound task, and stop
tuning volume the second draw it appears. The fix is the one
[[dynamo-starve-execution-not-rules]] names — make one decisive quantity need a
search or construction the agent cannot verify locally — and note that a
recovery bounded by a disclosed grid is not that, because agents brute-force it
in minutes ([[dynamo-z3-collapses-joint-integer-fits]],
[[dynamo-recovered-constants-are-still-transcription]]). Budget the check before
building: if a competent implementation of the whole contract is ~50 minutes of
typing, there is no room left for the crux to bite.
