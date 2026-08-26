---
name: dynamo-reskin-clears-post-index-cosine
description: A domain reskin + new graded artifact + new mechanics in ONE commit cleared cosine on the push right after an indexed passing commit.
metadata: 
  node_type: memory
  type: project
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-11T20:07:44.595Z
---

Measured on `dynamo-56ae913` (2026-08-12). Commit 1 passed `review / cosine_similarity` and
ran the full pipeline (so it entered the comparison corpus). Commit 2 — pushed deliberately
as a difficulty ratchet — **also passed cosine**, defeating the usual post-index self-match.

What commit 2 changed, all in a single push:
- full **domain reskin**: `bench`/`settle-benchbay` → `arena`/`reconcile-arena`, every
  fixture filename, the contract doc, the output paths, and `[task].name`
- a **third graded artifact** with its own schema (`panel_ledger.tsv`)
- genuinely **new mechanics** (drifting judge lanes; seat order recomputed per stage)
- `instruction.md` and `tests/test_outputs.py` **rewritten from scratch**, with the prompt
  restructured (deliverables-first) rather than paraphrased

Local token-cosine vs the indexed HEAD was **0.829 joined** (instruction 0.815, verifier
0.836) — well above the ≤0.76 "safe" band from [[dynamo-forge-records-answer-key]]-era
notes, and it still passed. Confirms the guard is necessary-but-not-sufficient in BOTH
directions: a mid-range lexical score does not predict a block when the *domain* actually
changed. The service metric tracks what the task is about, not word overlap.

**How to apply:** after a cosine-passing commit, never push a follow-up that leaves the two
compared files alone. Bundle the reskin + a new graded artifact + the real change into one
commit, and do not burn pushes trying to lower lexical similarity by rewording.

Related: [[dynamo-cosine-similarity-self-match]], [[dynamo-pass2-typo-is-not-difficulty]]
