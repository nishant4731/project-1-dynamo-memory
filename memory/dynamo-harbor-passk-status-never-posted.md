---
name: dynamo-harbor-passk-status-never-posted
description: "review / pass2 failing with '0 of 0 runs' means the harbor pass@k platform status was never posted — infrastructure, cleared by close/reopen, never by a task change."
metadata:
  type: reference
---

`review / pass2` can go red for a reason that has nothing to do with difficulty.
The tell is in the job log, not the sticky:

```
##[error] the platform's 'harbor / pass@k' status did not finish within 60 minutes
##[error] pass@2: no valid agent failure (0 of 0 runs failed genuinely).
```

**`0 of 0 runs` is the diagnostic.** A real "too easy" verdict says `2 of 2`
solved. Zero-of-zero means the external Harbor service never scheduled the
trials, so the analyser had nothing to read. Corroborating signals, all cheap:

- `pass2_suggestion` logs `pass2-output artifact unavailable — skipping suggestion`
- the pass@2 sticky is **stale** — identical trial ids to the previous run
  (see [[dynamo-sticky-timestamps-separate-infra-from-content]])
- `gh pr checks` shows **no `harbor / pass@k` row at all**

**Measured on `dynamo-2d0d4c3-security` PR #1, twice:** a `synchronize` (push)
event failed to get pass@k scheduled; a `gh pr close` + `gh pr reopen` scheduled
it within a minute both times, and the gate then returned a real verdict
(0 solved / 2 valid fails). Each wasted attempt costs an hour of wall clock.

Do **not** change task bytes, difficulty, or timeouts on this evidence — there is
no evidence in it. Post a comment recording the log line, close, reopen, and wait
for the single new run ([[dynamo-finding-a-defect-is-not-a-reason-to-cancel-a-run]]
still applies: one event at a time, or `cancel-in-progress` eats the run).
