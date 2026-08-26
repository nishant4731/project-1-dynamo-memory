---
name: dynamo-forge-records-answer-key
description: Dynamo verifiers should forge fixtures forward (encode a designed session) so the answer key is recorded by construction, not read back from the decoder.
metadata:
  type: feedback
---

For Dynamo task verifiers, build graded fixtures with a *forward* forge that encodes a designed session and records the expected report by construction, then assert an independently written decoder reproduces it. Wire that agreement check into a verify-time `self_check()` alongside coverage assertions (every status witnessed, every counter non-zero, boundary fixtures present).

**Why:** a key derived from the same decoder the task grades proves nothing, and QC/AVA ask for exactly this evidence. On `dynamo-6f5dee5` (2026-08-11) this arrangement cleared cosine, Dynamo eval, validation, pass@2, Deep Review, AVA and QC on the first commit.

**How to apply:** (1) forge intent, protected oracle and shipped reference must agree over hundreds of seeds before pushing; (2) run an AST pass for unreferenced functions — an "independent oracle" nothing calls at verify time makes `verification_explanation` false; (3) finish the mutation sweep with a real container run, because a sweep comparing in-process return values misses every serialization rule. See [[dynamo-cosine-similarity-self-match]].
