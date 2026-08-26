---
name: dynamo-scale-invariant-traps-are-brute-forceable
description: "Making the graded instances too large to brute-force does not hide a trap — agents validate on tiny self-made cases where the same property is checkable, then transfer."
metadata: 
  node_type: memory
  type: project
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T11:31:07.990Z
---

Measured on dynamo-65cf2ab PR #5 (`dynamo/approximant-forge`, 2026-08-17). This was the one lever
my notes said had drawn a valid fail on first try — starve *execution*, not rules
([[dynamo-starve-execution-not-rules]]) — and I measured the trap before building for once:

Best rational approximation under a denominator ceiling. The continued fraction's *convergents*
are not the answer; the semiconvergents between them usually are. Measured against the reference,
a convergents-only tool got 33 of 180 shipped rows wrong and 48–49 of 220 per graded corpus; four
other plausible misreadings cost 21–213 rows each. I set ceilings to fifteen digits **so that no
answer could be checked by trying every denominator**, and shipped no expected output anywhere.

**pass@2 came back 2 solved / 0 valid fails.** The reasoning was not that the agents got lucky:

- one **brute-forced `x = 1/3, N = 2`** during development, saw its convergents-only code fail,
  and fixed it;
- the other used a **Stern–Brocot / Farey binary search**, which enumerates every fraction with
  denominator at most the bound by construction and so never had the gap;
- the analyser noted brute-force validation "appeared independently in both trials".

**The error in my design:** I made the *graded* instances too large to brute-force and concluded
the trap was unverifiable. But the property is **scale-invariant** — convergents-only is wrong at
`N = 2` exactly as at `N = 10^15` — so the agent validates where verification is free and
transfers. Size hides nothing when correctness is checkable at small scale.

**The through-line across every lever measured on this repo** — sample-starved stated rules (7
draws), irreversibility on the one live copy (1 draw, agents deferred the live run), and now
scale-invariant computational subtlety — is the same agent behaviour: **build, self-test against
an independently constructed oracle, fix, commit.** Every trap that a self-made oracle can expose
is exposed.

**What that implies for the next attempt:** a trap only survives if the agent cannot construct an
independent oracle *at any scale*. That means either information it does not have (unfair, blocked
by QC B5) or genuine computational hardness (which yields timeouts, and in-progress timeouts count
for nothing). Before building anything further in this subcategory, state which of those two the
design escapes, and how — do not reach for "the graded instances are too big to check".
