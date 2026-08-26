---
name: dynamo-shipped-helper-must-be-pinned-and-proven
description: "A plumbing module you ship to the agent is both an attack surface and a drift risk — pin its digest, never import it from the reference, and prove it agrees."
metadata:
  type: project
---

Handing the agent a read-only helper under `/app/data` is the best lever there is for
converting in-progress timeouts into counted fails (see
[[dynamo-in-progress-timeouts-need-plumbing]]). It carries two hazards that must both be
closed, or it costs more than it buys.

**1. The reference must never import it.** It is agent-writable, so importing it from the
verifier lets a submission rewrite the thing that grades it —
[[dynamo-verifier-must-not-import-agent-paths]]. Keep the reference self-contained even
though that duplicates code.

**2. It can silently disagree with the reference and fail every honest solver.** If the
helper computes a counter one way and the graded reference another, an agent that does
exactly what the brief told it to do fails. This is a fairness bug that no oracle run
catches, because the oracle does not use the helper.

**The test that closes both**, in this order inside one function:
1. verify the file's digest against the frozen pin;
2. load it *from those verified bytes* into a scratch namespace (`exec(compile(...))`),
   not by importing the path;
3. compare every function it offers against the reference over the whole graded corpus —
   on `dynamo-2a4ed10` that is the starting symbol table, the step window, the reading of
   every module's imports, the per-call tally and all twenty-nine counters.

Add an adversarial case that appends one comment line to the helper: it must score 0, and
it should fail on the pin test *and* the agreement test.

**What is safe to hand over:** reading inputs, ordering, replaying a stated table, parsing
a syntax form the contract already fixes, accumulating counters, serialisation. **What is
not:** any judgement the contract asks the agent to make. On `dynamo-2a4ed10` the helper
grew to ~190 lines of transcription and 29 counter definitions while the cruxes — the
fixed-point closure, scope resolution, per-change re-analysis, quarantine cascade,
innermost-first rewriting — stayed entirely with the agent, and pass@5 still measured
0 solved / avg 0.000.
