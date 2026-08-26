---
name: dynamo-withheld-clause-gets-induced
description: "Measured on dynamo-9df6709: withholding a naming rule and shipping 64-member labelled precedent instead was solved 2/2 — agents infer shallow rules from precedent as readily as they read them."
metadata: 
  node_type: memory
  type: project
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-13T09:37:06.697Z
---

Withheld the stored-name rule from the order sheet entirely and shipped
`naming_precedent.tsv` per vault instead: the sheet disclosed only the rule's *shape*
(6 axes → 64 candidates) and the precedent left exactly one standing. The intent was a rule
an agent cannot write its own test for, because inventing a test case means knowing the
answer first.

**Measured 2/2 solved.** The rubric named the mechanism directly: one agent was
"dynamically inferring naming rules from `naming_precedent.tsv` rather than hardcoding".
`task_specification` PASS both trials. Solve times 30 and 40 min of 60.

**Why it failed as a lever:** the withheld thing was a *clause*, not an *algorithm*. Fitting
64 candidates against a table is a loop an agent writes in a minute — cheaper than reading
the paragraph would have been. This is the same result as
[[dynamo-stated-optimum-gets-solved]] (7/7 cracked a 64-subset joint optimum): 64 is not a
search, and induction over a small labelled space is not difficulty.

I already had this written down as [[dynamo-starved-branches-need-algorithmic-depth]] —
"12 unobservable one-line rules still solved 2/2 in 7 min; starve algorithms, not clauses" —
and built a one-line rule anyway, because *unwritten* felt stronger than *unobserved*. It
isn't. Unwritten and unobserved are the same axis; depth is the other one.

**How to apply:** before withholding anything, ask what the agent must *build* to recover it,
not what it must guess. If recovery is "enumerate the stated family and filter", the lever is
already spent — the disclosure of the family hands over the search space. Spend the cycle on
a branch whose correct implementation is expensive to reach instead.

**Confirmed again, and it cost a whole head.** `dynamo-137a569`, 2026-08-14. I withheld an
*algorithm* rather than a clause — the reduction tree a `psum` kind folds on — stating only its
recursive form and pointing at an archive of eight historic runs from which the split table
`s(n)` for n = 2..10 was uniquely recoverable. Well-posed, blind on every runnable pack, and a
program with perfect arithmetic that assumed the obvious `n // 2` was byte-identical on the
visible pack and rejected on nine of ten held-out packs. It still drew **2/2 solved**: both
agents wrote a script, ran the induction, and read off "largest power of two below n" within a
handful of steps, finishing in 37 and 47 minutes of the hour.

**The rule this sharpens:** a recoverable table with a small, well-posed search space is not
difficulty, it is a five-step subroutine — agents are *better* at mechanical induction than at
careful reading. "Withhold an algorithm, not a clause" is still right, but the algorithm has to
be expensive to *reach*, not merely unstated. What finally moved that task was
[[dynamo-sampling-point-counters-beat-the-ceiling]], which adds no search at all.
