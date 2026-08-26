---
name: dynamo-aggregate-evidence-pins-curves
description: "Sparse per-input samples never identify a quantised transfer curve; band sums do — and report the function, not the parameters."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 589469b6-5088-434c-a2be-3e8b63665d9f
  modified: 2026-08-11T19:22:05.427Z
---

When a Dynamo task asks the agent to recover a quantised integer response
`clamp((gain*u + bias)//D, 0, 255)` from calibration evidence:

- **Per-input samples on a sparse grid do NOT identify the curve.** Measured on
  `dynamo-0a072a0`: every-3rd/5th/7th/11th/17th sampling of `u` left 2–200
  admissible `(gain, bias)` pairs whose 256-value curves *differed*, i.e. the
  graded answer was genuinely ambiguous (QC B1/B5). Dense sampling fixes the
  ambiguity but hands the agent a lookup table, killing the inference.
- **Aggregate band sums fix both.** Ship `total = sum(response(u) for u in low..high)`
  over bands partitioning `0..255`. Measured: 6–16 bands left 1–2 admissible
  pairs and, critically, **all of them induced the identical 256-value curve**.
  The agent still cannot read values off the folio, so the fit is real work.
- Band sums are **monotone in bias**, so the reference/referee can binary-search
  the bias interval per gain (fast) while a naive full scan of the parameter box
  is still tractable — probe the *narrowest* band first, or a naive solver blows
  its per-run budget.
- Because several pairs can share one curve, **grade the curve, not the pair** —
  or disclose a canonical choice ("smallest gain, then smallest bias") and assert
  the whole admissible set induces one table, so the fixture proves its own
  determinacy on every generated seed.

Also add a redundant-rule caveat: a `toe` cut-off parameter is redundant with a
negative bias plus the low clamp, and makes the family unidentifiable. Drop it.

See [[dynamo-forge-records-answer-key]] for the forward-construction rule.
