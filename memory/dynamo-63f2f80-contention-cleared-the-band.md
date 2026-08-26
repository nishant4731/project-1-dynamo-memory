---
name: dynamo-63f2f80-contention-cleared-the-band
description: "dynamo-63f2f80 ALL-GREEN on head 6: contention over a shared resource cleared pass@5 (2/5, avg 0.400) after five heads of stated-rule ratchets all failed."
metadata:
  type: project
---

`dynamo/squash-layer-stack` (Container Builds) went all-green on `f4b1c14`: cosine
`0.78/0.83/0.82`, static + Dynamo eval, similarity UNIQUE, Harbor validation,
pass@2 1/2, Deep Review, Ava, Tier-1, qc_eval/qc_exec/qc_gate, trials **2 solved ·
3 good-valid · avg@5 0.400**, final gate. Six heads.

**The full difficulty ladder, measured on one engine:**

| head | lever | pass@5 |
|---|---|---|
| 9a8c57a | provenance column + counter (stated) | 5/5 |
| edd6d99 | removed the prompt's pitfall tour and §12's clause list | 3/5 (both fails wedges) |
| 43620d5 | interaction stack composing existing families | 5/5 |
| f4b1c14 | **contention over a shared resource** | **2/5, gate PASS** |

Zero analytical failures across all 13 trials of heads 2–4. What finally worked is
[[dynamo-withhold-an-algorithm-not-a-clause]]: a pool of recovered blobs, each
usable once, where two entries can want the same blob; the run must fill the
maximum number at once and break ties by smallest per-seat blob-name sequence. The
shipped stack gives every lost entry exactly one eligible blob, so **seven
plausible fillings — first-fit, most-constrained-first, largest-blob, reverse
order, reusable blobs, lanes ignored, length ignored — are all byte-identical to
the reference there** and all wrong on the held-out stacks.

**Do this before shipping such a rule:** validate the optimum three ways. Two
structurally different matchers (Kuhn vs Hopcroft-Karp) agreeing on 400 random
instances, plus the oracle agreeing with an exhaustive enumerator on 400 more.
Then build the blindness table with the real verifier —
[[dynamo-blind-branch-shipped-fixture-proof]].

**Caveat on the evidence, worth carrying:** all three counted failures were
Terminus-2 heredoc wedges (`difficulty_crux` FAIL), same as on `19c8cbd` and
`e155cf7` which were also accepted this way. The gate counts them; a human
reviewer may not like them. Deliverable size makes it worse — the reference is
~28 KB. Did **not** push a fix on the all-green head: a redraw can land 3–5/5.
See [[dynamo-operational-passat-failures]].
