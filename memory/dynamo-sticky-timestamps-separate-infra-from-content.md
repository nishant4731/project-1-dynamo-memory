---
name: dynamo-sticky-timestamps-separate-infra-from-content
description: "Fetch PR stickies with updated_at; a job that failed without refreshing its sticky died in infra, not on your content."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T18:25:12.461Z
---

Dynamo stickies are **edited in place**, so a stale sticky reads exactly like a fresh
pass. `gh pr checks` says `review ❌` and the visible sticky says `✅ PASS` — that is not a
contradiction to shrug at, it is the diagnosis.

Always fetch with the timestamp:

```
gh api "repos/$R/issues/$PR/comments" --paginate \
  --jq '.[] | "@@@ \(.updated_at)\n\(.body)"'
```

Then compare each sticky's `updated_at` against the run you care about.

Measured on dynamo-65cf2ab head `6d7c03b`: `review` failed after 3m30s. `Static checks ✅`
was stamped 18:08:14Z (that run), but `Dynamo eval — ✅ PASS` was still 17:16:10Z, from an
earlier head. The `review` job is static checks → Dynamo eval, so it cleared static and then
died **without the eval ever rendering a verdict**.

**Why:** a content rejection always posts a verdict — `❌ FAIL` naming the criteria. A job
that produces no verdict at all did not judge your task. Absence of a fresh sticky is
positive evidence of infra failure, and it is the only evidence available when
`gh api .../actions/jobs/<id>/logs` and `gh run view --log-failed` both 404 (they do,
without upstream write access).

**How to apply:** before editing anything in response to a red job, diff the sticky
timestamps. If the deciding sticky is stale, do not go hunting for a content defect —
you will invent one. Retry instead. And check whether the gate that actually costs you
something is even running: on these heads `pass2` showed `skipping`, so the `review`
failures burned **no** pass@2 draws and retrying was cheap. See
[[dynamo-finding-a-defect-is-not-a-reason-to-cancel-a-run]] for the converse — when checks
are live and green, hold the fix.

Related: [[gh-token-empty-override]] (auth red herrings), and note `origin` is the upstream
repo with `push:false` — pushes go to the `fork` remote.
