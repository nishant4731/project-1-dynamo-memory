---
name: dynamo-reconstruction-beats-specification
description: "Measured end-to-end on dynamo-d44c669: three specification heads solved 2/2; rebuilding as policy-reconstruction-from-a-log gave 0/5 with 3 valid fails and an all-green gate."
metadata:
  type: feedback
---

One repo, one day, four heads, all other gates green throughout:

| head | difficulty lever | pass@2 |
|---|---|---|
| starved branches (14 of them, blindness 21/22) | specification | 2/2 solved, ~10 min |
| + bespoke order-dependent settlement (blindness 25/27) | specification | 2/2 solved, 21 / 27 min |
| + policy induced from a 28-row calibration corpus | specification-ish | 2/2 solved, 19 / 33 min |
| **rebuilt: recover the policy from a 376-row decision log** | **reconstruction** | **0/2, then 2/2 valid fails** |

Final: **pass@5 0/5 solved, 3 good valid fails, avg@5 0.000, `difficulty_crux` PASS on
all five, `gate` green.**

**The rule.** A complete normative contract is something the reference pair *reads and
types*, no matter how many interacting subsystems it carries or how thoroughly the
shipped sample is starved — three measurements, ratchets bought solve time (10 → 24 → 26
min) and zero failures. A policy that exists only in logged outcomes has to be
*searched for*, and search is the one thing that consumes the hour without converging.
Every trial that failed did so on the intended crux; the analyser said so explicitly and
in the same breath said it was "not a specification or verifier problem".

**Why the calibration-corpus head still failed:** 28 clean rows with isolating sweeps are
cheap to verify a candidate against, so an agent that guesses wrong catches itself. See
[[dynamo-oracle-corpus-solve-or-timeout]]. What works is a log that is **large and
jointly varying** — no column moves alone, so constants must be separated rather than
read off — with the decisive evidence deliberately thin: a threshold fixed only by the
rows either side of it, and a precedence pair visible only where both checks fire on one
request.

**Make fairness provable, because QC will ask.** Ship the B5 answer as executable tests:
enumerate every transposition of two neighbouring rungs and require each to contradict
the log; perturb every constant both ways and require that anything the log fails to
contradict also fails to change a graded answer. Both returned empty. A third test —
that the notes name no constant and do not list the reason codes in application order —
caught a real leak in my own first draft.

**The QC block to expect:** C3 on *unreachable report branches*. Fallback values
("-1 when nothing is granted", "0 for an empty batch") described in the notes but reached
by no graded batch let a mutant return anything. Fix by making the cases real — an
all-denied queue with a generator-side assert, and empty queues — and by hoisting the
fallbacks into named constants so the sweep can mutate them.

Related: [[dynamo-blind-sample-branch]], [[dynamo-spec-mold-caps-at-80pct-solve]],
[[dynamo-recovered-constants-are-still-transcription]].

**Counter-measurement (2026-08-15, `dynamo-c1fed49`).** The same engine, ported
to medical-and-clinical workflows, was solved 5/5 at pass@5 and 2/2 twice at
pass@2, in 15–50 minutes, across four heads that each added a documented lever.
See [[dynamo-reconstruction-mold-hit-its-ceiling]] for the table and for the
three levers that measured as ineffective there. Treat this memory's 0/5 result
as a property of d44c669's specific instance, not of the mold.
