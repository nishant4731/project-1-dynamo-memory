---
name: dynamo-state-an-optimum-not-an-algorithm
description: "Nine heads of stated rules all solved 2/2; replacing greedy placement with a stated optimum drew 4 good valid fails. State WHAT is best, not HOW."
metadata:
  node_type: feedback
  type: feedback
---

On `dynamo-d8a8539` nine consecutive heads added stated rules — a fixed-point
thinning, a ladder-raise closure, a margin that narrows the plot, raises carrying
across passes — and **every one measured 2/2 solved**. Blindness grew from 32/57
to 55/82 invisible misreadings with no effect at all. A strong agent implements
whatever the spec says, however deep the interaction.

What worked was changing *what kind of thing* was specified. Instead of "settle
each candidate in turn, first free anchor wins", the standard says: **the strip
takes the allowed placement that labels the most candidates**, with a total
tie-break so exactly one qualifies. Determined, so QC B5 is satisfied. But the
natural implementation — any sweep — is wrong wherever two candidates want the
same room, and greedy differed from the optimum on **26 of 29** graded networks
while agreeing byte-for-byte on the shipped one. pass@5 went to **4 good valid
fails**, all of them here.

**Why:** an agent transcribes a procedure accurately. It cannot transcribe an
optimum — it has to *derive* an algorithm, and the obvious one is wrong. The
shipped sample being uncrowded means nothing local ever contradicts the obvious
one.

**How to apply:** find a step currently specified as a procedure and ask what it
is trying to achieve. Specify the objective plus a total tie-break instead.
Check three things: (1) the naive procedure diverges on most held-out fixtures,
(2) it agrees on the shipped one, (3) an exact solution is genuinely cheap for
you — here conflicts reached only ±2 candidates, so a bounded-window DP is
milliseconds while agents reach for O(5^n) DFS.

Pair it with [[dynamo-bound-a-wedged-submission]] — agents will write the
exponential version, and unless you bound it their failure is scored as your
infrastructure problem. See
[[dynamo-data-science-and-reporting-data-visualization-playbook]].
