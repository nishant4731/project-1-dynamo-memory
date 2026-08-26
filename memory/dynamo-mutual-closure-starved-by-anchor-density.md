---
name: dynamo-mutual-closure-starved-by-anchor-density
description: "Define two graded sets as a mutual least fixed point, then ship a sample whose evidence density resolves it in one sweep — the naive single pass is byte-identical there and wrong everywhere else."
metadata: 
  node_type: memory
  type: project
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-16T22:01:00.643Z
---

Built for dynamo-65cf2ab (residue-mill-salvage, 2026-08-17). The charter defines the recoverable
per-channel masks and the recoverable batch values **together**, as the smallest pair of sets
closed under three rules (anchors give values; two agreeing quotients pin a mask; five unmasked
shards pin a value). It never says "iterate" — the closure is a definition, so the task stays
fair and QC B5-clean.

The starve is evidence *density*, not a hidden clause. The shipped sample publishes ~11 anchors
per era, so anchors → masks → values reaches the fixed point in one sweep; the protected mills
publish 4–6 and need three. Measured against the reference: a single-pass mender is
**byte-identical on the sample** and wrong on every protected mill — 9–11 of 27 counters, 7–21
payload files, and the whole lane audit. It fails silently: unpinned pairs just drop shards below
the `need` floor, so some rows come back "undetermined" and the output is still well-formed.

Why this shape beats the recovery ceiling ([[dynamo-reconstruction-mold-hit-its-ceiling]],
[[dynamo-self-verifiable-recovery-never-commits]]): there is no checksum over a recovered value,
so an agent holding the wrong reading cannot see it is wrong. It finishes, commits, and is
counted — instead of looping until the budget runs out.

This is the concrete form of [[dynamo-withhold-an-algorithm-not-a-clause]] and
[[dynamo-starve-a-ranking-rule-with-graph-shape]]: starve the shipped instance's *shape* so the
cheaper algorithm coincides there, and state every rule plainly.
