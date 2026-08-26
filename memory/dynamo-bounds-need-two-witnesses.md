---
name: dynamo-bounds-need-two-witnesses
description: "QC C3 checks a bound from both directions: an accepted record sitting exactly on it and a refused line one step outside it. Witnessing only one side leaves the other free."
metadata:
  type: feedback
---

QC's C3 probe mutates the **submitted solution** and asks whether grading still
rejects it. For any bound the contract states, that means two independent
mutations — tighten it and loosen it — so a bound needs **two** witnesses:

- an **accepted** record sitting exactly on the edge (kills tightening:
  `PORT_LOW = 1` → `2`, `last <= first` → `<`)
- a **refused** line one step outside it (kills loosening:
  `PORT_LOW = 1` → `0`, `LABEL_LIMIT` → `+1`)

**Why:** measured on `dynamo-2d0d4c3-security` across two consecutive QC rounds.
Round 1 flagged `last <= first` → `<` on an incoherent-amend test, because no
planted amend landed *exactly* on the boundary. Round 2 flagged `PORT_LOW = 1`
→ `0` on the very next push — the fix had planted a flow *on* every bound and
nothing *past* any of them. Same family, two rounds, two hours.

**How to apply:** enumerate every numeric constant, comparison and pattern the
contract states, and for each write down both witnesses before pushing. Then
prove it the way QC does, not the way your own reference sweep does: patch the
**solution** with single-token changes (`1`→`0`, `1`→`2`, `<`→`<=`, `{16}`→`+`,
`[0-9]`→`[0-9a-z]`), install each as the graded deliverable, and run the whole
graded corpus. A reference-side mutation table will not find these — it tests
whether *grading* discriminates, not whether the *corpus* contains the row that
makes the discrimination possible. See
[[dynamo-inert-rules-are-c3-holes]] and [[dynamo-c3-needs-a-clause-sweep]].

Corollary: if a comparison's two readings are **provably identical** (writing the
same value twice), do not try to witness it — rewrite it so the comparison is
gone (`min(...)` instead of `if x < seen`). An unkillable probe is a permanent
C3 finding waiting to happen.
