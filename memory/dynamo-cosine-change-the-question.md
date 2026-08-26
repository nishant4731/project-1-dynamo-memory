---
name: dynamo-cosine-change-the-question
description: "Repeat Dynamo subcategory clears enforced cosine on push 1 when the task asks a different question than the delivered sibling, not when it renames nouns."
metadata: 
  node_type: memory
  type: project
  originSessionId: d0dbd568-34b9-46db-9c5f-cf121220beaf
  modified: 2026-08-11T19:59:44.041Z
---

Dynamo task `dynamo-19c8cbd` drew "Dependency and lockfile resolution" while delivered sibling `dynamo-5b7b599` already did semver + peers + closure under capacity limits in the same category. It cleared enforced `review / cosine_similarity` on the **first** substantive push (2026-08-12).

**Why:** the two tasks answer different questions. The sibling *selects a feasible set under resource limits and partitions it into phases*; the new one *reproduces a package manager's incremental resolver* minimising change against an existing lockfile — different inputs, different core trap, different output contract. Shared nouns (ledgers, semver, JSON receipt, TSV table) did not matter.

**How to apply:** before writing anything in a repeat category, state the delivered sibling's question in one sentence and confirm yours is a *different sentence*. If only the nouns differ, expect a block and redesign rather than reskin. This is prevention — it does not rescue an already-poisoned lineage (see [[dynamo-cosine-similarity-self-match]]).

Companion trick that kept a fully-disclosed spec hard: grade a **stated global optimum** over a lexicographic objective whose first term rewards leaving prior state alone, then arrange the shipped fixture so the natural greedy resolver agrees with the optimum there and only diverges on held-out packs. Self-checking teaches the agent nothing.
