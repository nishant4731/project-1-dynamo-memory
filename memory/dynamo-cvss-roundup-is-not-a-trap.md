---
name: dynamo-cvss-roundup-is-not-a-trap
description: CVSS v3.1 base scores never expose the Roundup-vs-naive-ceil divergence — swept all 2592 metric combinations, zero disagree.
metadata:
  type: reference
---

The CVSS v3.1 specification defines `Roundup` as "the smallest number with one
decimal place >= x", implemented on integer-scaled input because the float
products can sit a hair above a tenth. That looks like a ready-made exactness
trap for a security task, since most people write `math.ceil(x * 10) / 10`.

**It is not available for base scores.** Swept every combination of the eight
base metrics (AV 4 × AC 2 × PR 3 × UI 2 × S 2 × C/I/A 27 = 2592 vectors): the
naive ceil and the specification's Roundup agree on all of them. The products
that feed a *base* score never land exactly on a tenth, so the two definitions
never part. The divergence only shows up in environmental and temporal scoring,
where a previously-rounded value can re-enter the arithmetic.

Also worth pinning while here, because it is easy to misremember:
`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:L` is **3.8**, not 3.9 — raw
3.706374936. Ten published reference vectors verified against the implementation
in `dynamo-4242b2d`'s `_mend_engine.py`.

**How to apply:** use CVSS base scoring for realism and as a transcription
surface (an agent can still mistype 8.22 or the 0.915 clamp), never as the thing
a task is supposed to kill on. Build the kill levers out of the surrounding
mechanics instead — see [[dynamo-recovery-tasks-are-bimodal]] for what does and
does not convert solvers.
