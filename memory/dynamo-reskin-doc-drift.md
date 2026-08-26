---
name: dynamo-reskin-doc-drift
description: A mechanical Dynamo reskin silently drifts input filenames and mutation anchors away from the hand-written contract; oracle validation stays green.
metadata:
  type: feedback
---

Applying an ordered string-substitution reskin to code files escapes in two ways that a green oracle run does NOT catch:

1. **Renamed mutation anchors silently no-op.** Caught only by asserting the sweep's **build count** (matched 41 of 42 here), never by "0 survivors".
2. **Input filenames drift from the contract.** A chained rule rewrote `standing_pins.json` → `standing_fastenings.json` in code and fixture, while the hand-written protocol still said `standing_pins.json`. Oracle scored 1.0 because code and fixture agreed with each other — only the agent-visible document disagreed. This is the drift that blocks Dynamo eval `unambiguous` / `test_instruction_alignment`.

**How to apply:** add a doc-vs-code check that enumerates the shipped input directory and asserts every filename appears in both the contract and the code, and that every file literal named in the docs exists in the code. Checking only output keys and receipt counters misses it.

**Ordering:** on a post-cosine push, run the substitution FIRST and hand-write the contract AFTER, then run the cross-check. Writing the contract from memory before the rename lands is how they disagree. See [[dynamo-cosine-change-the-question]].
