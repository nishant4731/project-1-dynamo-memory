---
name: dynamo-starve-execution-not-rules
description: "Measured across four heads of one repo — starving a readable rule never produced a pass@2 failure; starving an execution property (bit-exact binary32) produced one on the first try."
metadata:
  type: feedback
---

One repo, `dynamo-137a569`, four evaluated heads, same starvation discipline throughout:

| head | what was starved | pass@2 |
|---|---|---|
| roll-up v1 | 8 readable rules (hold windows, fallback scope, tie-break, gap exclusion) | 2/2 solved, 9.5+15 min |
| roll-up v2 | + constants absent from the charter, recovered from calibration rows | 2/2 solved, 19+20 min |
| roll-up v3 | + which *model* generated the evidence (one or two hinges) | 2/2 solved, 16+34 min |
| **metricshard fold** | **the arithmetic itself — step-wise IEEE binary32** | **1 solved, 1 valid fail** |

In every roll-up head the misreadings were *measured* blind on the visible pack (8/8, then 12/12,
then 14/14 byte-identical) and caught on 3-6 held-out packs. The agents cleared them anyway; the
trial analyses said they "derived these from the charter's normative text". **Blindness of the
sample is not the lever. Derivability of the answer is.** A rule you can read is a rule you can
implement, however carefully you hide the witness.

The fold task states its rules just as plainly, but the decisive one is not a rule you apply — it
is a property of how your language computes. Python is binary64; folding with `+` and narrowing
once obeys every sentence except "each step is itself a binary32 operation". Measured as a whole
program, not a mutation: byte-identical checkpoint on the visible pack, rejected on 9 of 9
held-out packs. The failing trial's two bugs were exactly that shape — `struct.pack('<f', x)`
raising `OverflowError` instead of yielding infinity, and float64 arithmetic used to *detect*
inexactness so a subnormal addend vanished below double's ULP.

**How to apply:** when picking the crux, ask "can a careful reader be right first time?" If yes,
no amount of witness-starving will buy a failure. Reach for properties the language, not the
contract, decides: bit-exact float semantics, accumulation order, signed zero, subnormals,
overflow, double rounding of decimal literals. Prove it the same way — write the naive program in
full and require it byte-identical on everything the agent can run. Related:
[[dynamo-blindness-table-before-pushing]], [[dynamo-spec-mold-caps-at-80pct-solve]],
[[dynamo-starved-branches-need-algorithmic-depth]].
