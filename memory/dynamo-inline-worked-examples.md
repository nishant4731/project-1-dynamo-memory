---
name: dynamo-inline-worked-examples
description: "Ship a Dynamo worked example as inlined bytes in the contract doc, never as an expected/ directory in the agent image."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 153881bd-5cd7-4300-b32c-84cc025d70b7
  modified: 2026-08-11T19:34:48.834Z
---

A Dynamo task needs a worked example so byte conventions are discoverable, but
shipping it as `environment/data/<pack>/expected/bench_report.json` puts files
named exactly like the graded artifacts, in a directory literally called
`expected/`, inside the agent image. Inline the exact expected bytes into the
agent-visible contract markdown instead, keep only the example *input* on disk,
and hash-pin the contract file.

**Why:** `anti_cheat` (Stage-1 rubric) and QC E1 both hunt for "oracle/expected
values readable by the agent". The information content is identical either way,
but a directory of answer files pattern-matches the failure mode, while quoted
bytes in a spec read as documentation. Inlining also lets a verifier test assert
the quoted example equals what the reference computes, which turns the doc into
a checked artifact rather than a drift risk.

**How to apply:** put the canonical output text in a fenced block in the
contract, add the contract's SHA-256 to the input pins alongside the fixtures,
and add a test that recomputes the example pack and asserts its report and
ledger lines appear verbatim in the contract. Related: [[dynamo-forge-records-answer-key]].
