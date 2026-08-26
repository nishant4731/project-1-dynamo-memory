---
name: dynamo-verifier-must-be-idempotent
description: "QC A1 \"oracle fails its own verifier\" with validation green means your verifier can only run once — stash the reference, don't delete it."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7110d418-8520-45e1-942a-0fd9ba7507cb
  modified: 2026-08-11T21:45:51.795Z
---

QC's A1 probe invokes `tests/test.sh` **more than once in the same container**. A delete-oracle that `os.remove`s `tests/_reference.py` before the first candidate run therefore makes run 2 raise `FileNotFoundError` in every test and score reward 0, while Harbor `review / validation` (single run) scores the oracle 1.0.

**Why:** "validation green + qc_gate A1 red" is never a reference defect — it is a harness-reuse bug in your own verifier.

**How to apply:** reproduce with two consecutive `bash /tests/test.sh` calls in one container before pushing. Keep the hardening but make sealing reversible-by-lookup: move the reference into a root-only stash (`/var/lib/<task>-sealed`, mode 0700) and have the bench find it in either home. The candidate still runs as uid 65534 against a 0700 `/tests`, so delegation is refused as before. Assert the stash mode alongside the `/tests` mode. See [[dynamo-reskin-clears-post-index-cosine]].
