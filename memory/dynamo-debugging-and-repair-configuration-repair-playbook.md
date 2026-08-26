---
name: dynamo-debugging-and-repair-configuration-repair-playbook
description: PLAYBOOK Debugging and Repair / Configuration Repair - ALL-GREEN on a bent-score recovery mold, pass@5 0 solved / 3 good valid.
metadata:
  type: project
---

**Debugging and Repair / Configuration Repair.** Repo
`dynamo-9c93375-debugging-and-repair`, PR #2, accepted head `6d81de3`.

## The mold that worked

A complete normative contract with exactly ONE subsystem withheld, recovered from
a log of past decisions, graded byte-exact and differentially on 9 unseen fields
plus one shaped from the submission's own SHA-256. The difficulty is entirely in
the withheld subsystem; everything bolted onto execution measured zero.

**The crux is that the withheld score is NOT LINEAR.** One term earns at a full
rate up to a threshold and a reduced rate above it. Measured over the reachable
offer space (10731 ordered pairs): no straight-line reading is order-identical to
it anywhere (so it is recoverable and fair), while the closest straight line
agrees on **96.84%** of pairs — close enough that a fit converges and is
believed. It is wrong on **4 of the 10** graded fields and RIGHT on the visible
one, so the only self-check a solver can run passes.

## Measured on the accepted head

- **pass@2** 0 solved / 2 valid-fail / 0 timeouts.
- **pass@5** 0 solved / **3 good-valid-fail** / 2 in-progress-timeout, avg@5 0.000.

Trial analysis, quoted: *"All five failures trace to inability to recover the
bent (capped) non-linear scoring function... The task's difficulty crux —
intended by the author — is the direct cause in every case."* Agents
independently reported converging on *"a linear best that matches ~96.84% of
ordered pairs (matching the task.toml-predicted failure rate exactly)"*.

## Hurdles, per gate, in the order they blocked

1. **ava_review `sound_verifier`** — the stray-file scan walked only the staged
   tree, so a submission writing to a hard-coded `/tmp` path scored 1.0. Fix:
   snapshot the shared writable roots around the child run.
2. **deep_review `no_brittle_time_dependence`** — that snapshot then failed a
   CORRECT solution because the Daytona daemon appended to
   `/tmp/daytona-daemon.log` mid-run. Fix: record `st_uid` and charge only
   entries owned by the user the child ran as. See
   [[dynamo-privilege-drop-false-rejection]] for the same class of error.
3. **pass2 too easy (2/2 solved)** — the score was linear, so z3/perceptron/LP
   cracked it in ~34 min. Fix: bend it. See
   [[dynamo-z3-collapses-joint-integer-fits]].
4. **qc_gate C3** — §5 said an int normalising to zero is written `0` with no
   sign, and no graded field ever contained one, so the rule was inert. Fix:
   plant a setting whose only offer spells `-000`, on 7 of 10 fields but NOT the
   visible one. Verify by replaying qc_gate's own probe, not by rebuilding.
5. **trials 0/5 with 3 uncounted timeouts** — nobody delivered. Fix: ship the
   non-crux I/O in the image and ask for an artifact early.
6. **trials 0/5 with 4 uncounted timeouts** — two trials crashed on
   `KeyError: 'age'`, because the log pre-populates `age` while a case carries
   `stamp`. Two of my own files disagreed about the shape of one object. Fix:
   `read_case` returns offers carrying the derived age.
7. **trials, final** — agents never HYPOTHESISED a bend, so they searched linear
   forms until the clock stopped. Fix: §7.3 stopped promising the score climbs at
   the same rate across the range. That converted 2 uncounted timeouts into
   countable valid fails and cost **zero** solves.

## Levers measured NOT to work here

- **Widening the implementation surface.** A re-key of backing to the station's
  class, wrong on 9 of 10 fields under a naive reading, drew **0 of 5** failures.
  Agents implement stated rules correctly. See
  [[dynamo-widening-implementation-surface-measures-zero]].
- **Naming the wrong reading.** Saying the choice was "not an order imposed on
  them" took pass@5 from 2 solved / 3 valid to **4 solved / 1 valid**. See
  [[dynamo-naming-the-wrong-reading-costs-passat5]].
- **Sample-starving a stated rule** — the visible field misses the branch, but a
  general implementer still writes it correctly.

## The gate-vs-gate tension, and how it resolved

QC B5 and C3 demand every rule be stated and witnessed; stating a rule is what
lets pass@2 solve it. The resolution here: state EVERYTHING except one
subsystem, and make that subsystem's *shape* — not its parameters — the thing
that is hard to guess. Disclosing the shape class (**"not necessarily a constant
rate"**) cost 0 solves and bought 2 countable fails; disclosing a wrong reading
("not an ordering") cost 2 valid fails. **Disclose the hypothesis class, never
the dead end.**

## Operational

pass@2 in-progress-timeout (cut off mid-fix) and a pass@5 analytical wedge (full
budget on analysis) are DIFFERENT objects — the second can score a good valid
fail. `[agent].timeout_sec` is capped at 3600 and
`expert_time_estimate_hours` far above that reads as timeout-assisted
difficulty; keep them within ~2x.
