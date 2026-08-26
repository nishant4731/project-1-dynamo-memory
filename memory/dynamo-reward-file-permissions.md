---
name: dynamo-reward-file-permissions
description: Never chmod /logs/verifier/reward.txt — Harbor reads it host-side and a 0600 file fails validation with Oracle ❌ despite a green suite.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-11T23:51:08.928Z
---

Do not tighten permissions on anything under `/logs` in a Dynamo `tests/test.sh`. Harbor parses `/logs/verifier/reward.txt` **from the host** as the runner user, so `chmod 0600` on a root-owned reward file makes `validation` report Oracle ❌ with `PermissionError` in `harbor-output/<job>/task__*/exception.txt`, while the in-container verifier log shows every test passing.

**Why:** the reward file is an interface to the harness, not a protected input; only the container writes it, and the host must read it.

**How to apply:** make the reward fail-closed by writing `0` before pytest and then rewriting it from the pytest status in *both* branches (`if status -eq 0; then echo 1; else echo 0; fi`). That is what actually defeats an agent tool forging `1` mid-run — confirm with a stub planner that writes `1` and emits empty artefacts; it must score 0. See [[dynamo-cosine-change-the-question]] for the surface rewrite the follow-up push then needs.
