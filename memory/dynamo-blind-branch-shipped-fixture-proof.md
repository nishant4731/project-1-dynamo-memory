---
name: dynamo-blind-branch-shipped-fixture-proof
description: Prove the blind-sample lever before pushing — run a plausible misreading of the spec and confirm it reproduces the shipped delivery byte for byte while failing the held-out stacks.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 166d16b5-ede4-479d-b0ae-5ffb0fd59525
  modified: 2026-08-12T23:42:14.302Z
---

On `dynamo-63f2f80` (`dynamo/squash-layer-stack`, Container Builds) the design bet
was [[dynamo-blind-sample-branch]]: the shipped stack deliberately never exercises
seven stated rule families, so an agent's own testing cannot distinguish a correct
reading from a wrong one.

**The cheap check that turns that bet into evidence:** write the *plausible wrong
implementation* (here: walk each layer archive in order, applying whiteout markers
as you reach them, instead of running all markers before the layer's own entries),
install it as the submission, and run the real verifier. The result you want is
exactly two things at once — the shipped-stack comparisons **pass byte for byte**,
and only the held-out replays fail. That is the blind branch working; if the
shipped comparison also fails, the sample is not blind and the lever is not armed.

**Why:** the shipped fixture is graded too, so it is easy to assume a wrong reading
gets caught there. Measuring it is one container run and it is the only direct
evidence that a self-verifying agent will commit to the wrong answer.

**How to apply:** build the fixture so every trap branch is absent, state that fact
in the contract (a numbered "scope of the shipped stack" section — it is honest, it
pre-empts a "misleading data" finding, and it does not help the agent decide *which*
reading is right), then assert the scope claim in the verifier so the doc cannot
drift from the fixture. Related: [[dynamo-inline-worked-examples]],
[[dynamo-oracle-corpus-solve-or-timeout]].
