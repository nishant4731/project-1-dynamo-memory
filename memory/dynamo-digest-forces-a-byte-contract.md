---
name: dynamo-digest-forces-a-byte-contract
description: "Grading bytes (or digesting them) makes the serialization a graded rule — state the exact spacing, or pass@2 blocks it as a task/verifier problem."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2098be54-4cd9-4510-8d3a-c5cdde339a1a
  modified: 2026-08-13T14:13:59.636Z
---

Measured 2026-08-13 on `dynamo-9b8a04d`. A pass@2 trial recovered all 26 hidden
policy constants, matched every count, and still scored 0: it serialized with
`json.dumps(..., separators=(",", ":"))` while the verifier compared the
delivered bytes. The gate did not call that a valid failure — it called it
**"task/verifier problem — a sound, permitted approach was defeated"**, which
blocks the PR and wastes the draw.

**Why:** the moment a deliverable is compared byte for byte, or a digest is taken
over it, the *serialization* is a graded rule, not an implementation detail.
`sort_keys=True` is not enough: separators, spacing after `:`, trailing newline
and key order are all part of the contract, and Python's defaults are a choice
the spec has to make out loud.

**How to apply:** when a graded artifact is bytes, write the exact form into the
agent-visible contract — keys ascending, `", "` between members, `": "` after
each key, newline-terminated — and show one real line from the shipped fixture as
a worked example, regenerated from the frozen fixture so it cannot drift. The
alternative is to compare parsed JSON per line and drop the digest; you cannot
keep the digest and leave the encoding unstated. Contrast the *fair* version of
the same rule: once disclosed, a compact-JSON submission still fails, and that is
a legitimate failure.

Same trial exposed a second defect worth the same care: the log's isolating rows
were named `layers-`, `context-`, `cache-`, `mark-`, `share-`, and the agent
found them by name. A fixture row's identifier must say nothing about why it is
in the fixture — shuffle and number them uniformly. See
[[dynamo-do-not-narrate-the-trap]]: this is that lesson in data rather than prose.
