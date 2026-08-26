---
name: dynamo-rival-values-witness-window-rules
description: A CRT/window admissibility rule is unwitnessable by random corruption; construct a rival congruent on a shared submodulus to land it in any decade you choose.
metadata: 
  node_type: memory
  type: project
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-16T22:00:48.657Z
---

On dynamo-65cf2ab (residue-mill-salvage, 2026-08-17) the mutation sweep found that
`window_low`, `window_high` and `exactly one admissible value` all survived: with 5 prime
moduli near 10^6 (product ~10^30) and a 20-digit window, a randomly corrupted shard's CRT
result lands in the window with probability ~10^-10, so no random damage ever exercises the
bound. The rules were stated and unwitnessed — a textbook C3 hole.

The fix is a construction, not more damage. For a band of 7 with `need = 5`, split it 3 shared
/ 2 crafted / 2 kept. Any rival `W = V + k·(p_a p_b p_c)` agrees with the 3 shared shards for
free; write the 2 crafted shards to `W`'s residues and `W` now satisfies exactly 5, as does `V`
(3 shared + 2 kept). Since the shared product is ~10^18 and the window is 10^19–10^20, small `k`
places `W` in whichever decade you want:

- one decade **below** the declared length → witnesses the lower bound,
- **inside** it → two admissible values, so the row must be left undetermined; witnesses "exactly one",
- one decade **above** → witnesses the upper bound.

Same trick for a "one candidate recurs and no other does" rule: random corruption never makes a
second candidate recur, so plant a stretch of one lane written under the other era's mask, and
publish anchors on those rows so the stale quotient certainly recurs. Otherwise the lane pins
the stale secret silently, which is a contract defect, not a trap.

General rule: when a stated rule's discriminating region has measure ~0 under the damage model,
witness it by solving for an instance, and assert the intended outcome in the generator's
self-check. See [[dynamo-inert-rules-are-c3-holes]] and [[dynamo-mutation-sweep-finds-witness-holes]].
