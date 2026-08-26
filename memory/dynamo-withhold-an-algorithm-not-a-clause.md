---
name: dynamo-withhold-an-algorithm-not-a-clause
description: "A documented spec whose every branch fires in the shipped job gets self-audited to correctness; starve the shipped sample and make the withheld part an algorithm."
metadata:
  type: feedback
---

Measured across ~10 pushes on `dynamo-56ae913` (2026-08-13). Every variant of a
fully-documented spec was solved, and the trial transcripts show exactly how: the agent
copies the shipped job to `/tmp`, runs its program, audits the output against the briefing,
fixes what it finds, repeats. Two independent `deepseek-v4-pro`/terminus-2 runs each did
this and each landed reward 1.0.

That loop works **because every rule fires in the job the agent is handed**. The shipped job
is a complete self-test. Ratcheting rules cannot beat it:

| lever | effect |
|---|---|
| more volume (rows, artifacts) | solve time 19→47 min, solve rate unchanged |
| more stated rules | transcribed |
| an inference step with a wrong natural reading | **+2 valid failures** (the only thing that worked) |
| …then describing that trap in the briefing | back to 5 solved / 0 |

**What to build instead:** withhold an *algorithm*, and starve the shipped sample so the
wrong algorithm is byte-identical there. On this task, chit placement went from "the digest
names one cell" (a lookup) to "claims register against a bench, compete for the open cells,
and the run must seat the greatest number and then the smallest sequence" — maximum bipartite
matching plus a lexicographic tie-break. The shipped job's register **never contends**, so
greedy emits identical bytes there and fails only on held-out jobs.

Make it an invariant, not a hope: `self_check` asserts that on every contended job, each
plausible shortcut changes the output bytes, so a seed where the trap does not bite cannot be
built. Then keep a blindness table — for each wrong implementation, which jobs notice — and
require SHIPPED-SAFE plus caught-on-held-out.

Four ways a trap like this is silently fake, all hit once each:
- slots keyed without the item, so unrelated claims wrongly competed;
- filler/idle rows leaving spare capacity that dissolves the contention;
- the contested cells voiding on a quorum rule, so no difference reaches the grid;
- a tie-break invisible because a **stable** sort already reproduces it.

**How to apply:** ask "what in the shipped job would have to be absent for the wrong program
to look right?" and remove it. See [[dynamo-starved-branches-need-algorithmic-depth]] (starve
algorithms, not clauses), [[dynamo-silent-misread-converts-solvers]], and
[[dynamo-do-not-narrate-the-trap]].
