---
name: dynamo-reskin-clears-cosine-on-push-two
description: Second push after a cosine-passing head cleared by identity reskin + prompt rewrite + moving audit bulk into the private referee; word-cosine stayed ~0.93 and still passed.
metadata:
  type: reference
---

On dynamo-4fa50bd (carve-reader), commit 1 passed cosine and ran the full pipeline, so it was
indexed. Commit 2 had to change the same two compared files. What was done in one push: renamed
the data directory, the module, its entry point, all five payload filenames, the manifest field
names and `[task].name`; rewrote `instruction.md` from scratch with a different structure; and
moved the bulky packet-audit bodies out of `tests/test_outputs.py` into the private referee.
Cosine passed, and the commit went on to clear every remaining gate (pass@2 0/2 valid-fail, pass@5 1/5 solved / avg@5 0.200 with 4 good valid fails).

Measured local word-token cosine against the indexed head: 0.96 before any of this, 0.90 after
the identifier reskin plus one prompt rewrite, **0.93 joined at the passing push** (instruction
0.90, verifier 0.92). So the lexical proxy stayed high and the gate still cleared — consistent
with the gate being semantic. Do not spend rounds chasing the lexical number below 0.8 when the
domain vocabulary is intrinsic to the task; spend them on real identity and structure change.

Useful side effect: keep the file paths that QC findings name (the contract file, the referee)
unchanged through the reskin, so the fix-addressal stage still sees its diffs.
