---
name: dynamo-complexity-wall-beats-a-stated-rule
description: "Measured on dynamo-0e75ffc: eight starved branches and a fully stated optimum solved 2/2; the same optimum asked twice, so the idiomatic itertools.combinations goes past the run cap, gave 3 of 5 valid fails."
metadata:
  type: feedback
---

`dynamo-0e75ffc` (`dynamo/blightline-typing`), 2026-08-25, two evaluated heads.

| head | what it was | pass@2 |
|---|---|---|
| `7d11f99` | five interacting subsystems, 38 of 80 misreadings byte-identical on the shipped instance, §10 already stating "the smallest sufficient set" | **2 solved, 0 valid** — 15 and 23 min |
| `e8104dd` | same, plus a second optimum over the same graph, §6 restated as a property, nine sampling-point counters | 1 solved / 1 valid, then pass@5 **2 solved / 3 good valid / avg 0.400** |

**The finding.** Starving the sample does not beat a careful reader of a
complete spec: head 1's blind branches covered per-record lot windows,
repeat-plate supersession, the lead factor, comparability and opaque pairs, and
both agents implemented every one of them correctly from the prose. What
converted three of five was not a rule they could misread but a rule they could
not afford:

> every agent used `itertools.combinations` over sorted marker IDs, iterating
> k = 1, 2, … This convergence across all five independent runs is strong
> evidence of a shared training-data pattern for minimum-set-cover in Python.

That enumeration is *correct*. It finds the lexicographically smallest minimum
cover. It fails only on time, and only on instances the shipped week does not
contain — the shipped panel is 3 markers of 34, where every algorithm finishes.

**How to build one.** Ask for an optimum whose textbook implementation is
polynomially hopeless, then (a) make the shipped instance small enough that the
hopeless implementation looks fine, and (b) raise the held-out cost until it
does not — here by asking the same question a second time of the markers the
first answer left, which doubles the search and compounds a wrong first answer.

**The harness half is not optional.** A wedged submission has to be scorable.
Cap each graded run (30 s against a reference that settles the heaviest run in
under one) and latch: once one run wedges, refuse the remaining thirty-odd. All
three valid fails here were wedges; without the latch one hanging submission
spends the 900 s verifier budget and the trial is discarded as
`infra/setup-timeout`, which reads as the task's fault. See
[[dynamo-bound-a-wedged-submission]].

**Corollary on wording.** §6's iterative filter was solved because the protocol
said "in rounds … until a round marks nothing". Restating it as *the largest
pair of sets that support each other*, with a uniqueness argument, kept QC's
determinability happy and put the one-pass reading back on the table — 8 of 31
graded runs separate the two. Prefer a property to a procedure whenever both
are equally determinate. See [[dynamo-do-not-narrate-the-trap]] and
[[dynamo-b5-vs-pass2-determinability-pincer]].
