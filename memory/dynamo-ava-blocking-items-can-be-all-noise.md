---
name: dynamo-ava-blocking-items-can-be-all-noise
description: "On dynamo-63f2f80 all 12 AVA blocking items were self-agreeing paraphrase; the only real finding was an advisory naming importlib, and a subprocess rewrite cleared the gate."
metadata:
  type: feedback
---

AVA blocked with **12** `verifier_coverage` items. Every one filled the template
`expected X … but the verifier would instead Y` with **X == Y**: "matching
required", "solution keeps them since markers precede additions", "solution
byte-sort produces same", "solution hashes the same text streams it writes". No
acceptance-boundary gap existed behind any of them.

The single real finding was in the **advisory** block: `dynamic module load via
importlib.spec_from_file_location`. The mutation sweep imported each mutated
oracle into the verifier's own interpreter.

**The fix that cleared the gate** followed the playbook's rule — remove the
flagged pattern, do not substitute a same-family one. `_mutant_table.script` now
appends a `__main__` driver to the mutated source and the sweep runs it as an
ordinary subprocess, comparing one digest per stack; `importlib` and `uuid` left
the tests tree entirely. AVA passed on the next push, along with deep review,
tier1 and all three QC stages.

**How to apply.** Count how many blocking items restate the code as their own
"expected" — if all of them do, do not change grading. Hand-verify, fix whatever
the advisories name for real, and say so on the PR with the quoted evidence.
Confirms and extends [[dynamo-ava-real-finding-hides-in-advisories]].
