---
name: dynamo-calibration-ledger-not-an-oracle
description: "Recovered constants only remove the local oracle if the calibration cases are historic and self-contained, not drawn from the graded period."
metadata: 
  node_type: memory
  type: project
  originSessionId: 00684352-c7dd-44b6-bc7c-8ad46b0a358c
  modified: 2026-08-13T23:18:49.999Z
---

On `dynamo-ce5b6ea` (quayside-settle, 2026-08-14) the policy the solver must
recover lives in four `calib_*` tables whose rows describe **prior-period**
cases entirely inside themselves — a source tag plus a posting lag plus a
verdict, or a stay length plus a bonus plus the settled figure. They pin the
ten constants and confirm nothing else.

**Why:** if the calibration rows had pointed at this period's own gate reports,
boxes or agreements, the ledger would have doubled as an end-to-end oracle and
neutralised every blind branch behind it — the exact mechanism
[[dynamo-oracle-corpus-solve-or-timeout]] and [[dynamo-8ab540c-rate-chain-all-green]]
recorded. Recovery removes the local oracle only when the evidence is disjoint
from the graded instance.

**How to apply:** when building a
[[dynamo-reconstruction-beats-specification]] task, make the evidence corpus a
separate historic ledger, then prove uniqueness by exhaustive sweep of the
disclosed grids in the verifier, and build the witness structure explicitly:
every pair compared at zero lag to pin an ordering, a value exactly at and one
past each threshold to pin a window, and a curve walked through every regime to
pin the piecewise constants. See also
[[dynamo-blindness-table-before-pushing]] — 16 of 25 plausible misreadings were
byte-identical on the shipped instance here.
