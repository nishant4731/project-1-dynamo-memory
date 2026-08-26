---
name: dynamo-9b8a04d-rebuild-wave-dispatch
description: "Container Builds task — three evaluated heads measuring what does and does not move the difficulty band, with every soundness gate green throughout."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2098be54-4cd9-4510-8d3a-c5cdde339a1a
  modified: 2026-08-13T07:37:27.090Z
---

`dynamo-9b8a04d-build-dependency-and-release-management` (`dynamo/rebuild-wave-dispatch`,
Build Dependency and Release Management / Container Builds), PR #1. A container build farm
gets a base-image advisory; the agent writes `/app/yard_dispatch.py`, which stales the fleet,
condenses cyclic groups into single units, prices them, routes each to a builder class and
packs them into waves under seats, budget and a per-wave contention premium.

**Every soundness gate went green on the first substantive head and stayed green**: static
25/25, Dynamo eval 31/31, duplicate UNIQUE, Harbor validation, deep review, Ava, tier1,
qc_eval, qc_exec and qc_gate. Only the difficulty band ever blocked. Cosine passed on all
three heads (`0.697/0.762/0.795` → `0.711/0.776/0.801`) despite local joined word-cosine of
**0.97** between heads 1 and 2 — see [[dynamo-inflight-heads-not-indexed]].

| head | design | result |
|---|---|---|
| `ac3fd36` | complete normative standard; 6 starved branches (cycles, capacity, diamond span, ceil-vs-floor, clamps, inclusive limit) | **pass@2 2/2 solved**, 14 and 39 min of 60 |
| `cc85fa3` | + charge model moved out of the prose into a per-yard ledger (10 integers fitted at runtime); + wave-internal contention premium; 9 starved branches | pass@2 1/2; **pass@5 3/5 solved, 2 valid fails, avg 0.600** |
| `a2572f4` | + `wave_trace.tsv`, one exactly-graded row per placement (seat, charge, warmup, premium, admission, budget left) | pass@2 1/2; **pass@5 5/5 solved, 0 fails, avg 1.000** |

| `eac7c01` | trap-narration stripped from the prompt (see [[dynamo-do-not-narrate-the-trap]]) | AVA blocked before trials |
| `2009c3a` | AVA fixes: harness asserts root, superset-delivery no longer counts as a refusal, unenforceable float clause dropped | **pass@2 2/2 solved**, 27 and 29 min |

**The decisive tally: across 16 evaluated trials there were zero algorithmic failures.** Every failure ever observed on this task — 5 of them — was a
`cat > file << 'EOF'` heredoc wedging the PTY. The per-trial *reasoning* failure rate is
indistinguishable from zero, and the observed fail rate is just the wedge rate (~30%), which
makes a redraw a poor bet: P(≥3 of 5) ≈ 0.16. Adding the sixth graded artifact moved the draw
the wrong way (3/5 → 5/5), which is variance, not a regression.

**Removing the trap narration did not slow anyone down either.** The prompt had been naming the
starved branches outright ("dependency cycles that this morning's fleet does not", "tight enough
that most candidates wait") — a real defect worth fixing on its own terms, and the fix was
correct, but solve time went *down* (38 min → 27 and 29 min). Both agents hit genuine bugs (output
clearing order; counting warmup pairs from trace rows instead of `(wave, class)` pairs) and
debugged their way out with ~30 minutes to spare.

**Conclusion for this shape.** Six subsystems, an inferred ten-constant model, nine starved
branches, six graded artifacts and twenty exact counters produce a per-trial *reasoning* failure
rate of zero against Opus-4.8 + Terminus-2. The only observed failure mode is the heredoc wedge at
~25%. Reaching 0-2/5 with ≥3 valid fails needs a different concept, not another increment — and
crucially, one where the agent cannot check its own answer, which a ledger that fully determines
its constants can never be.

## Second concept, same result: `dynamo/gate-policy-replay`

Rebuilt from scratch as the reverse-engineering shape — a build-farm admission
policy with 26 integer constants that exist only in a decision log, different on
every graded farm, so frozen constants score 0 on the first unseen one (verified
by patching the reference).

| head | change | pass@2 |
|---|---|---|
| `a2ddd61` | first build of the concept | 1/2, but the fail was **my** defect: byte-compared rulings with the spacing undisclosed — see [[dynamo-digest-forces-a-byte-contract]] |
| `a09eda5` | byte form disclosed; fixture rows de-labelled | **2/2**, ~28 min |
| `339739a` | log rebuilt so **no two rows differ in a single weight-bearing field** — constants only come out of one exact 12-unknown integer system | **2/2** |

That last head is the platform's own highest-leverage suggestion implemented
exactly ("shift the task from diff adjacent rows to solve a constrained
system"). It did not move the result.

## ALL-GREEN on `4fb2b1a` — what finally worked

**pass@5 1/5 solved, 3 good-valid fails, avg@5 0.200, final gate green**, with
every other check green too. The failures were *stratified* — four distinct root
causes, not one wedge repeated: a brittle interval-narrowing recovery that found
zero or multiple solutions on two farms; two agents that never cleared the output
directory; a staleness limit inflated from 90 to 365 by counting rows already
refused at cascade step 1; and an agent that recomputed the weight floor/ceiling
from the batch instead of keeping the policy constants.

**The lever that broke a nine-head deadlock: put the hard part where the shipped
evidence cannot reach.** Everything before it was checkable against the log —
recover the constants, replay every row, know you are right — which is exactly
why every rule got implemented correctly first try. So the morning became a
*batch* that acts on itself: a fixed number of seats, and a share that grows by
`share_step_pct` for every request of the same owner already admitted, worked in
decreasing weight with ties on the request name. The log records decisions taken
one at a time, so it witnesses none of it, and no expected output ships for the
batch. Fully stated in the guide, so fair; completely untestable by the agent,
so lethal. It decided 22 of 144 rulings.

Generalisation: **fair ⇒ the evidence determines the answer ⇒ the agent can
self-check ⇒ solve-or-timeout.** The escape is not to hide a rule but to state
one whose *inputs the shipped evidence structurally cannot contain* — here,
per-request history versus a whole-batch settlement.

**Two QC C3 rounds, both real, both about fixtures rather than difficulty.**
(1) A refusal fixture that crashes instead of being refused hides whether the
check exists: `attempt=9` indexed past the retry table, so three of five
refusals were enforced by accident. Use values the engine can still evaluate.
(2) A two-sided range needs a fixture on *each* side, or half the check is
ungraded. Verify both the way QC does — mutate the **reference**, not the
referee, and require reward 0.

**Running total before that head: two fundamentally different task shapes, nine
evaluated heads, ~24 trials, and zero genuine reasoning failures.** Every
failure ever recorded was a heredoc terminal wedge or a defect of mine. Levers
spent: nine starved branches; constants recovered from evidence; 26 constants
instead of 10; forced simultaneous solving; wave-internal state; an orthogonal
exactly-graded artifact; removing trap narration; per-instance constants.

**How to apply:** when a repo reaches this point — every soundness gate green,
several distinct concepts measured, no failure that is not agent tooling — stop
ratcheting and escalate with the trial record. The remaining ideas are all
variations on something already measured, and each costs a three-hour pipeline.

**The two things this repo measured that are worth carrying.**

1. **Starving a textbook branch buys nothing** — the correction now recorded in
   [[dynamo-blind-sample-branch]]. Six disclosed-but-unsampled branches, all standard CS
   patterns, produced zero algorithmic failures.

2. **A calibration corpus that fully determines the hidden constants adds solve *time*, not
   wrong answers.** The ledger pins all ten integers uniquely (proved by sweeping both
   structural constants over their full range and the other eight over a wide band, on every
   graded yard). That uniqueness is what makes it fair — and it is exactly what lets the agent
   fit, replay all 230 rows and *know* it is right. pass@5 showed `difficulty_crux` PASS
   wherever it could be graded. Compare [[dynamo-calibration-blind-corpus]]: the corpus has to
   be narrow enough that the *graded* rules stay unverifiable, which this one was not, because
   the model applies identically to ledger rows and fleet images.

**The anti-hardcode lever did work and is cheap to reuse:** give every graded yard its own
constants, so a submission that freezes what it fitted on the shipped yard scores 0 on the
first unseen one. Verified directly by patching the reference to return frozen constants.

**pass@5 failure taxonomy, again:** both failures were terminal heredoc wedges on a ~300-line
deliverable — `cat > file << 'EOF'` leaving the PTY in PS2 for the remaining ~45 minutes.
The platform counts these as good-valid fails, but `difficulty_crux` reads FAIL and no
algorithmic content is reached. Same wedge that carried `dynamo-e155cf7` and `dynamo-19c8cbd`
into the accepted band. Read the taxonomy, not the headline —
[[dynamo-operational-passat-failures]].
