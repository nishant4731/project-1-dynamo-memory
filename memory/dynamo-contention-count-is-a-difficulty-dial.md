---
name: dynamo-contention-count-is-a-difficulty-dial
description: "On dynamo-9df6709 the number of contended-evidence groups per vault behaved as a continuous difficulty dial: 1 group = 4/5 solved, 3 groups = 0/5 solved with 4 valid fails and a green gate."
metadata: 
  node_type: memory
  type: project
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-13T19:15:49.736Z
---

The first thing on this task that was **tunable rather than a coin flip**. Same rule
throughout (see [[dynamo-9df6709-allotment-lever]]): evidence is contended, the mend must take
the allotment filing the most rows, and the shipped vault carries no contention at all.

| contended groups per vault | realm files | pass@5 |
|---|---|---|
| 1 | ~57 | 4/5 solved, 1 valid fail — blocked, too easy |
| 3 (+2 sacrifice groups) | 70–81 | **0/5 solved, 4 good valid fails, avg@5 0.000 — gate green** |

**Why it moves:** the correct rule admits a cheap implementation (contention is local, so the
problem decomposes into independent groups) and an expensive one (global search over the whole
realm). At one group the naive version still finishes; past ~70 realm files it cannot. All five
trials wrote `combinations × permutations` with the size check *after* generation, plus an
unpruned backtracking allotment search, and every one wedged at 300 s during pytest collection
with 0 tests run.

**The caveat to carry:** all five failed with the *same* root cause, and nobody solved it. That
clears the gate (0–2 solved, ≥3 valid fails) but it is a uniform speed failure, not diverse
algorithmic error, and the sweet spot is probably 2 groups — 1–2 solved with 3–4 valid fails.
If a future head needs to look less like a resource artifact, turn the dial down rather than
inventing a new mechanism.

**How to apply:** when a rule has a cheap correct form and an expensive correct form, the
instance size is the difficulty dial, and it is continuous where every other lever measured
here was binary. Verify the reference stays fast at every setting (mine settles in <1 s at 81
files because it decomposes), and keep the shipped instance at zero contention so the naive
version stays byte-identical there.
