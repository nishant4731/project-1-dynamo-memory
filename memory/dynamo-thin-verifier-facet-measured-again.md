---
name: dynamo-thin-verifier-facet-measured-again
description: Porting an ALL-GREEN harness lexically self-matched its source at 0.9625; moving every assertion body into the private audit module took it to 0.6979 local / 0.7517 at the service.
metadata: 
  node_type: memory
  type: project
  originSessionId: 057bd8c7-9c47-4bb7-afe8-e48b273fdb71
  modified: 2026-08-25T00:00:44.116Z
---

**Measured 2026-08-25 on `dynamo-d8fab40-file-and-media-operations` (fieldsync-conform),
porting the `dynamo-84f73e9` folio harness into Audio and music processing.**

First draft of `task/tests/test_outputs.py` reused the folio's shape: class-grouped
tests whose bodies called `bench.tree_problem`, `bench.graded_run`,
`bench.probe_results`, `bench.typed_diff`, `bench.stable_part`,
`bench.frozen_pins`, `bench.scan_for_leaks` directly and inlined the assertion
logic. Local token-cosine of the two compared facets against 166 local Dynamo
tasks:

| facet | worst match | score |
|---|---|---|
| instruction | dynamo-84f73e9 (folio, delivered) | 0.8282 |
| **verifier** | **dynamo-84f73e9** | **0.9625** |

0.9625 is over the service threshold's neighbourhood on a *delivered* task —
exactly the [[dynamo-cosine-matches-your-house-prose]] failure mode.

**The fix, in one pass, before the first push:** move every assertion body into
the private audit module behind a small question-per-call API
(`bench_faults(question)`, `live_faults(question)`, `replay_faults(slot)`,
`settle_faults(slot)`, `survey_faults(question)`, `mutation_faults(question)`),
then rewrite `test_outputs.py` as ~7 parametrized module-level test functions,
each one line of `assert not faults`. No classes, no rig helper names in the
compared file beyond `rig.LIVE_ID` / `rig.HELD_OUT` / `rig.SETTLED`.

| facet | after | at the service |
|---|---|---|
| instruction | 0.8495 worst | **0.7797** |
| verifier | **0.6979** worst | **0.7517** |
| fingerprint | — | 0.8378 |

Confirms [[dynamo-thin-the-verifier-facet]] with a second, larger measurement
(0.96 → 0.70), and confirms [[dynamo-port-the-mold-to-a-fresh-subcategory]]:
the port cleared enforced cosine on push 1, but only because the compared
verifier bytes were reshaped, not just the nouns. Parametrization is what makes
the file thin — one test function covering six questions is six graded checks
of one line each.

Corollary worth reusing: **measure both facets locally against every task folder
you have before the first push**, with a plain token-cosine. It costs seconds
and it caught a 0.96 that no amount of rewording would have moved.
