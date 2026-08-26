---
name: dynamo-do-not-narrate-the-trap
description: "Measured — a briefing paragraph naming the wrong reading and its symptom took pass@5 from 3 solved/2 valid to 5 solved/0; state the rule, never the mistake."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-14T07:04:30.042Z
---

Measured 2026-08-13 on `dynamo-56ae913`.

| push | briefing | pass@5 |
|---|---|---|
| `22d1a16` | hinge rule stated plainly | 3 solved · **2 valid** |
| `85b0012` | + signed bonus **and** a note explaining the wrong reading | **5 solved · 0** |

The note added with the ratchet:

> reading the bonus as though it had to be positive does not make that seat
> unlocked — it makes it look drifted, silently, with two lanes that fit…

Both agents that failed on the previous push had failed by classifying every seat
`unlocked`. The paragraph names that exact symptom and tells the reader it is the wrong
conclusion. The ratchet and the antidote were the same edit, and the antidote won.

**The distinction that matters:** a *rule* is content and must be complete — QC B5 blocks
anything underdetermined. Commentary about how an implementer might misread the rule is
not content, and it is worth roughly two valid failures. "The bonus is any non-zero integer
in -40..40" is a rule. "…and if you assume it is positive the seat will look drifted" is a
walkthrough of the trap.

Tells that a sentence is commentary, not spec: it names a *wrong* reading; it explains why
an order or boundary matters; it uses words like *silently*, *load-bearing*, *note that*,
*just as well*. Grep the agent-visible files for those before pushing.

**Narration also burns the clock, not just the valid fails.** Measured 2026-08-14 on
`dynamo-137a569`: a pass@2 trial spent 1741 s over eight LLM calls — one of them 861 s of
"deep binary32 arithmetic reasoning" — and never wrote a line of code before the 3600 s cap
fired, scoring `in-progress-timeout`, which counts for nothing. Two texts caused it: the
charter's worked-example section enumerated the starved branches outright ("never exercises
inexact arithmetic, signed zero, subnormals, infinities, `max` ties, strays, empty metrics,
or a decimal literal that needs care") and the instruction restated the arithmetic rule as a
warning that the two readings "disagree… silently, in the last bit". A trap list tells the
agent to be careful, and careful is expensive. So narration costs twice: it converts valid
fails into solves *and* it converts would-be fails into timeouts. See
[[dynamo-volume-overshoots-the-band]] for the other half of that clock.

**How to apply:** write the normative rule, then delete every sentence that explains its
consequence. Disclose the narrowness — "neither runnable pack reaches every rule the charter
states, and agreeing with them is not evidence of a correct fold" — and never the list, which
is [[dynamo-never-hand-the-agent-the-map]] applied to your own worked example. Keep the reasoning in `task.toml`'s difficulty_explanation, which reviewers
read and agents never see. Related: [[dynamo-silent-misread-converts-solvers]] (why the
silent misread is the lever) and [[dynamo-spec-mold-caps-at-80pct-solve]] (never ship a
ratchet and a kill-remover in one push — this is that mistake in its subtlest form, where
both were a single edit).
