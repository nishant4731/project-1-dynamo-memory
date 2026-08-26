---
name: dynamo-block-replacement-swallows-earlier-edits
description: "Replacing a whole spec section deletes clauses added to it in earlier commits; grep for the term proves nothing, grep for its definition."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T04:35:58.925Z
---

On dynamo-65cf2ab (2026-08-17) I added a `margin` definition inside charter §7 rule 3, then a
later commit replaced the whole of §7 with a rewritten numbered procedure. The replacement
swallowed the definition. I "verified" the edit by grepping for `margin` and seeing hits — but
every hit was in §8, which only says "`margin` is the lane's margin … or `-` when the lane has no
margin". Circular. Two pass@2 agents each invented a different formula, both defensible against
the charter's only worked example, and the trial analyser correctly scored one trial
`task_specification: FAIL`.

**Why:** the correct formula existed only in `task.toml`'s `difficulty_explanation`, which is not
agent-visible. Metadata prose is not a spec.

**How to apply:** after any whole-section replacement in a normative document, re-derive the
checklist of terms that section is supposed to define and grep for each **definition**, not the
term. A term appearing in a usage sentence is the failure mode, not the evidence. Cheapest
mechanical guard: for every field name in the output-format section, assert that the word appears
somewhere *outside* that section too.

Related: [[patch-scripts-need-readback]], and the same task's independent finding that a graded
field whose value only the withheld engine can compute is an undisclosed convention
([[dynamo-name-the-column-what-it-means]]).
