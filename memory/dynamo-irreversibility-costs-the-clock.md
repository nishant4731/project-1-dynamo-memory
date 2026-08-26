---
name: dynamo-irreversibility-costs-the-clock
description: "Measured on dynamo-2d0d4c3: 'the live artefact is the only copy' made both pass@2 trials time out with correct tools; shipping a restorable spare archive took them to 2/2 finished."
metadata:
  type: feedback
---

`dynamo-2d0d4c3-security` (dragnet-restitch), 2026-08-22. Two consecutive pass@2
draws on head `98771ce` returned `AgentTimeoutError` ×2 with **`low_timeout` FAIL
0/2**, `task_specification` PASS 2/2, `approach_validity` PASS 2/2 and the
analyser's own *"no signal of a task or verifier problem"*. Neither trial wrote a
graded artefact, so neither carried any difficulty signal.

The cost was named exactly: `task__HetnaXo` **had a working tool on a /tmp copy at
step 17, ~33 min into a 60-min window**, then spent the remaining ~25 min
re-reading its own code and was cut off before ever issuing the live command —
*"42% of the available time on post-validation review before a one-command final
step"*. `task__vwbUFJc` wedged on a one-line `TypeError` and was mid-fix at the
wall.

**The instruction caused it.** It said the live store was the only copy and there
was no way to rebuild one, so deferring the single run until certain was the
*rational* play — and certainty does not fit in the budget. pass@2 pins
`min(timeout_sec, 3600)` regardless of `[agent] timeout_sec`, so "raise the
override", which is what the gate itself recommends, is not a lever you have.

**The fix that worked: ship a sealed pristine copy and hand over the restore.**
`/app/data/dragnet.spare.tar`, built in the Dockerfile with
`tar -C /app/data -cf … dragnet`, plus one line of instruction asking for an early
first pass instead of a perfect last one. Next draw: **both trials finished**, one
with the wall firing only after it was already done. An archive, not a directory —
it cannot be mistaken for a second instance to process, and unpacking restores the
shipped modes as well as the bytes (a `cp -a` of a read-only tree restores a
read-only tree the agent's tool then cannot write into).

Grade the abuse routes before shipping it. Measured, all correct: restore-and-stop
0, restitch-then-restore-over-it 0, spare left inside the graded directory 0, spare
deleted afterwards **1**, two restore-and-redo cycles then a clean run **1**.

This supersedes the irreversibility lever in
[[dynamo-security-network-forensics-playbook]] and
[[dynamo-security-authentication-and-authorization-playbook]]: it converts nobody
into a *graded* failure, it only converts them into uncounted timeouts, which
[[dynamo-timeouts-anchor-nothing]] says are worth zero. Related:
[[dynamo-inprogress-timeouts-need-an-early-write-nudge]],
[[dynamo-irreversibility-does-not-fire-on-a-careful-agent]].
