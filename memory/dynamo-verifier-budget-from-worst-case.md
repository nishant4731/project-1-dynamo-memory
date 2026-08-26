---
name: dynamo-verifier-budget-from-worst-case
description: "Never size [verifier].timeout_sec from the oracle — a wrong submission costs far more; cap each run AND give all runs a shared budget."
metadata:
  type: feedback
---

Sizing `[verifier].timeout_sec` from a **clean-oracle** measurement is a trap that costs a
whole pipeline run. On `dynamo-2a4ed10` I cut it 2400 → 900 because the oracle took 58 s.
A pass@2 trial then **finished correctly on the shipped instance** and scored 0 anyway,
because the verifier hit 900 s and wrote *nothing* — no `ctrf.json`, no `reward.txt`.

**Why the oracle is the wrong yardstick:** the oracle is right, so every graded run is fast
and every comparison short-circuits. A *wrong or slow* submission is the expensive case.
Here 13 graded checkouts + 5 double-runs = 23 subprocess invocations at `RUN_TIMEOUT = 300`
= 6900 s worst case, before the mutation sweep even starts.

**Fix, both halves — the per-run cap alone is not enough:**
1. Cap each run of the handed-in program at a small multiple of the reference's cost
   (`RUN_TIMEOUT = 60` where the reference takes <1 s is ~500× headroom).
2. Give *all* the runs a shared ceiling (`RUN_BUDGET`), and once it is spent fail the
   remaining checkouts immediately instead of letting each wait out its own timeout.
   Without this, 23 × 60 = 1380 s is still unbounded-ish as the corpus grows.

Measured after the fix: a submission that sleeps for ever and one that sleeps 30 s per
checkout both leave the suite finishing in **~500 s with a reward written**, against a
2700 s budget. Add both as adversarial cases — a hanging submission is a case you must
test, not assume.

**Corollary:** the `pass2_suggestion` sticky reached the same diagnosis independently from
the trial detail, which is a good sign the reasoning generalises. See
[[dynamo-in-progress-timeouts-need-plumbing]] and [[dynamo-timeouts-anchor-nothing]] for
the agent-side twin of this failure mode.
