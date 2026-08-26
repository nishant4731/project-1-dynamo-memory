---
name: dynamo-invisible-volume-is-load-bearing
description: "Measured both directions on dynamo-d8fab40: trims that no failure taxonomy blamed still took pass@2 from 0/2 to 2 solved. Trim volume only when trials time out before writing anything."
metadata:
  type: project
---

**Measured 2026-08-25 on `dynamo-d8fab40-file-and-media-operations`.**

Head `b0f3ed7` measured pass@2 **0/2 with two valid fails** and pass@5 2 solved
/ 2 valid / 1 timeout. I then trimmed twice, each time reasoning "no trial has
ever failed on this":

| head | trim | pass@2 |
|---|---|---|
| `b0f3ed7` | — | **0 solved · 2 valid** |
| `a45494f` | −6 per-cause report counters | 1 solved · 1 timeout |
| `e48003b` | − the `settled` column as well | **2 solved — too easy** |
| `b71c68a` | both reverted | 1 solved · 1 valid → pass@5 **3 good valid, ALL-GREEN** |

**The `settled` column never appeared in a single failure taxonomy and was
still load-bearing.** It did not cause failures; it occupied the stretch of the
hour agents otherwise spend finding the crux bug. Remove it and they find and
fix the bug instead.

**The rule.** "No trial failed on X" does not license removing X. Read the
taxonomy for *where the clock ran out*:

- trials **time out before writing any artefact** → trim volume, or nudge the
  agent to write early ([[dynamo-inprogress-timeouts-need-an-early-write-nudge]]);
- trials **finish and solve** → volume is what is holding difficulty; adding
  starves is the lever, never trimming.

Corrects the naive reading of [[dynamo-volume-overshoots-the-band]] and
[[dynamo-in-progress-timeouts-need-plumbing]], which say to cut volume on
timeouts — true only for the first case. Related:
[[dynamo-file-and-media-operations-audio-and-music-processing-playbook]].
