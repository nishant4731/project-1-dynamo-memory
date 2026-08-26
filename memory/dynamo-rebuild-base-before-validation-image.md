---
name: dynamo-rebuild-base-before-validation-image
description: The manual Harbor fallback stacks a validation image on the env image; rebuilding only the top layer grades new tests against stale fixtures and fails the oracle.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78170f0c-ffe4-4520-83b2-fd6ece737755
  modified: 2026-08-14T20:04:39.412Z
---

The laptop's manual oracle/nop fallback is two images: `dynamo-<task>-env:dev` built from
`task/environment`, then a throwaway `FROM <env>` that COPYs `solution/` and `tests/`
(needed because Docker Desktop here cannot bind-mount `~/Documents`).

After regenerating fixtures, rebuilding **only** the validation image left the env layer
holding the previous `environment/data`, so the oracle ran against the old shipped window
while `/tests` computed expected values from the new generator. Result: a single failing
test (`test_published_files_for_the_shipped_window`) and `ORACLE_REWARD:0` that looks like
a real task defect and is not.

**Why:** `FROM dynamo-<task>-env:dev` resolves to whatever that tag currently points at;
nothing in the top-layer build invalidates it when `environment/data` changes.

**How to apply:** any time `dev/materialize.py` (or whatever regenerates
`environment/data`) runs, rebuild **both** images in order before trusting the reward —
env first, then the validation image. When an oracle fails right after a fixture change,
check the image staleness before touching the task. Related:
[[dynamo-fixtures-must-survive-the-image]].
