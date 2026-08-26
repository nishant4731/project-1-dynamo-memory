---
name: dynamo-timeouts-anchor-nothing
description: "pass@ gates need agents who finish and are wrong; in-progress timeouts count for nothing, so adding work makes the gate harder to pass."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7110d418-8520-45e1-942a-0fd9ba7507cb
  modified: 2026-08-14T12:25:23.439Z
---

The pass@5 gate needs >=3 counting failures with >=1 "good valid fail" (finished,
wrong, sound approach). `in-progress-timeout` counts for **nothing** and
`soft-timeout-fail` can only fill, never anchor.

**Why:** measured on dynamo-7e6bfa7 across many heads — 2/5 solved with 3
in-progress timeouts is *blocked*, while 1/2 solved with one genuine analytical
failure *passes*. Trial analyses repeatedly said agents "never created the
executable", spending the whole hour reverse-engineering.

**How to apply:** budget the task so agents finish inside 3600s (a hard cap —
raising `[agent].timeout_sec` does nothing). Give away recovery work that only
costs time (flat constants, step orders, anchor pairs); withhold only what
separates careful from hasty. Adding difficulty that adds *work* pushes toward
timeouts and makes the gate harder, not easier. See
[[dynamo-starve-one-rule-not-the-evidence]] and [[dynamo-do-not-narrate-the-trap]].
