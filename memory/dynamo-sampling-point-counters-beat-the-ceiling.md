---
name: dynamo-sampling-point-counters-beat-the-ceiling
description: "Measured escape from the fully-specified-charter ceiling: adding counters that differ only by WHEN they are sampled flipped a 2/2 draw to 1 solved / 1 valid-fail, without adding any work."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cdcd2dbe-3dc2-46a2-8b7b-9b15206e9e4b
  modified: 2026-08-14T13:09:03.150Z
---

`dynamo-f1e47b1` (`dynamo/shadecast-refit`), 2026-08-13. Four evaluated heads on one concept:

| head | change | solve times | pass@2 |
|---|---|---|---|
| 1 | 8-stage charter, constants from per-quantity logs | 16, 28 min | 1 solved, 0 valid-fail (verifier bug) |
| 2 | + hull coverage with a top-left fill rule, never witnessed by the logs | 16 min | infra-tainted; ratchet **absorbed** |
| 3 | calibration regrouped so the rate model needs a joint integer fit | 24, 60 min | **2/2 solved** |
| 4 | tally split 9 → 16 fields, seven new sampling points | — | **1 solved, 1 valid-fail** |

Heads 2 and 3 are the negative result: a genuinely subtle *stated* algorithm (fill rule) moved
solve time by **zero**, and making constant recovery a joint fit moved time a lot but still got
solved. What flipped it was the cheapest change of the four.

**The signal that told me what to add.** In the 2/2 draw the only mistake either agent made in
the whole trajectory was a counter: one miscounted `demoted` by taking every re-quoted deferred
batch instead of only those whose mip level actually changed — and caught it at **step 69 of
70**. That is the playbook's #2 lever by lethality, and it is nearly free.

**Why it works when volume does not.** Trial 2 of the 2/2 draw used every second of the hour, so
more *work* would have converted it into an in-progress timeout (which counts for nothing and
blocks). Counters add **slip surface without adding work**: one line to compute, a whole careful
reading to get right. Seven new fields = seven independent chances to sample at the wrong stage.

**Confirmed a second time, and it carried the whole task.** `dynamo-137a569`
(`dynamo/fold-metricshards`), 2026-08-14. A bit-exact binary32 fold sat at 2/2 solved through
three different ratchets — trimming volume, removing trap narration, and withholding an
algorithm behind a recoverable archive. Adding **three counters that differ from existing ones
only in when they sample** — `intermediates_subnormal` (every step) against `results_subnormal`
(checkpoint value only), `roundings_tied` (the inexact steps that fell exactly halfway), and
`additions_absorbed` (a third predicate over the same additions) — took it to **pass@2 0/2 with
two valid fails and pass@5 1/5 solved, 4 good valid fails, 0 timeouts, avg 0.200, ALL-GREEN**.
Cost to the agent: three lines. The signal to look for was the same one as last time — the only
genuine fails this task had ever produced were counter bugs, and I had *removed* counters
(19 → 9) to buy clock. Check what the failing trajectories actually got wrong before trimming.

**Caveat from that head:** three of the four valid fails shared one root cause — agents reading a
general "operations on an infinity are not counted" clause as applying only to the inexactness
counters and not to the new one. That is an ambiguity doing the work, and it is fragile: see
[[dynamo-ambiguity-is-the-only-valid-fail]] and
[[dynamo-ambiguity-fix-needs-a-paired-algorithmic-trap]]. Scope each new counter's exemptions
explicitly in the same table row, and get the difficulty from the sampling point instead.

**Third confirmation, and the cheapest one yet.** `dynamo-c31fb12`
(`dynamo/trumpline-reckon`, Games / Board and card games, 2026-08-23) sat at
**2 solved / 0 valid-fail** with every rule stated and eleven natural misreadings
already byte-identical on the shipped instance — the shape starve alone converted
nobody. Splitting the report 33 → 39 took it to pass@2 **0 solved / 1 valid-fail**
and pass@5 **2 solved / 3 good valid / avg 0.400, ALL-GREEN**. The new idea worth
copying: make two of the new counters *the cruxes counted rather than tabulated*,
chosen so each is an identity on the shipped instance and only there —
`lanes_scanned` (entrant-and-table pairs) equals `entrants_placed` exactly when
nobody moves tables, and `knots_reckoned` (groups reckoned apart at every depth)
equals `knots_formed` exactly when every knot settles in one pass. That gives each
crux a second, independent chance to be caught for one line of code, and it does
not weaken QC B5 because each counter is defined precisely in the report table.

**How to apply.** When a draw comes back all-solved with spare budget spent and the analyser
reporting only counter-level bugs, do not add another subsystem — split the report into fields
that differ *only* by which stage has run: counted before any budget decision vs after; the set
the second pass touched vs the subset it changed; one pass's total vs both; the allowance before
spending vs after; an index taken in consideration order vs submission order. Ship a mutation per
field, and assert the graded decks tell each confusable pair apart on ≥3 frames, or reading one
field for the other is never caught. See [[dynamo-z3-collapses-joint-integer-fits]] and
[[dynamo-recovered-constants-are-still-transcription]].
