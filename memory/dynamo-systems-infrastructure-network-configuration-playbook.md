---
name: dynamo-systems-infrastructure-network-configuration-playbook
description: "PLAYBOOK Systems Infrastructure and Operations / Network configuration — ALL-GREEN on ONE push; pass@2 1/2, pass@5 0 solved / 3 good valid / 2 in-progress timeouts, avg 0.000."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6feeec0b-9eaa-4b71-b4d1-76c0eadbedab
  modified: 2026-08-22T17:46:39.747Z
---

**Category:** Systems Infrastructure and Operations · **Subcategory:** Network configuration
**Repo:** `handshake-project-dynamo/dynamo-07ecbf9-systems-infrastructure-and-operations`
· PR #1 · head **`1030da4`** · **ALL-GREEN and `accepted` on the FIRST substantive
push** (2026-08-22). Related: the earlier Systems Infrastructure task
`Signal Relay Recovery` needed three heads; this one needed none.

## The mold

**Repair-in-place with a complete contract**, ported from
[[dynamo-security-authentication-and-authorization-playbook]] (`warrantbook-reissue`)
into a fresh subcategory — the [[dynamo-port-the-mold-to-a-fresh-subcategory]]
lever, third confirmation.

`dynamo/fabric-recompile`: a fabric compiler died mid-recompile. The agent writes
`/app/fabric_recompile.py <fabric_dir>` which sifts packed `plan/` bundles and an
unapplied `pending/` queue against six ordered refusal causes, applies changes in
`seq` order (files numbered in *flush* order), merges coincident sessions on a
five-part key, re-takes SHA-256 digests, repacks under two bundle bounds, rebuilds
a per-bundle byte-offset index, settles the advertisement scope into `SCOPE.tsv`,
files refusals with collision ordinals, spends the evidence and writes 38
counters. `RECOMPILE_RULES.md` states everything in twelve sections — which is
what keeps QC **B5** green.

## The crux: put the state variable in the state, not on the node

A route class travels as a state `(router, allowance)`. A zone border seeds its
own classes at `BUDGET_CEILING = 5`; an active session of relay allowance `r`
takes a state of allowance `a` to `min(r, a - 1)`, carrying a `(cost, hops)`
label relaxed to a least fixed point. **The allowance is part of the state**: the
cheapest chain into a router may arrive with nothing left to relay while a dearer
chain is the only one that carries on. `carriers` is a *second* walk over the same
product graph — backwards over tight steps from every landing that attains the
keystone's least label.

**Why it is invisible on the shipped fabric:** one uplink per router (a tree, so
one chain and one state per router), every session at the relay ceiling (so
`min(r, a-1) == a-1`), no chain long enough to spend its allowance (so
`installs == adverts` on every row), nothing back-dated, and no equal-cost pairs
(so `carriers == hops + 1`).

## Measured on the accepted head

| gate | result |
|---|---|
| cosine | instruction **0.6468**, verifier **0.8681**, fingerprint **0.7966** (threshold 0.9) |
| Dynamo eval | 30 PASS / 1 N/A / **0 failures** |
| duplicate | UNIQUE (closest TB3 lexical 0.059) |
| validation | Docker ✅ Oracle ✅ Nop ✅ |
| **pass@2** | **1 solved · 1 valid-fail · 0 timeouts**, "Rerun Recommended: NO" |
| ava / deep_review / tier1 | PASS, PASS (3 advisories), PASS |
| qc_eval / qc_exec / qc_gate | **37 checks passed on the first push**, empty `QC-FIXES-B64` |
| **pass@5** | **0 solved · 3 good-valid · 0 soft-timeout · 2 in-progress-timeout · avg@5 0.000** |

**Blindness table before the push: 15 of 26 plausible misreadings left the
shipped fabric byte-identical and were wrong on 15–20 of 20 protected fabrics.**
The headline (collapsing the state to the router) was blind on the shipped fabric
and wrong on **20/20**.

Mutation sweep: **144 probes, 144 built, 0 survivors, 0 caught-by-one**, control
green, 33 s. The same 144 mutants installed as the *submitted* solution and graded
over the whole 14-fabric graded corpus (QC's own method) also had **0 survivors**.

## What actually drew the failures — read this before ratcheting

**The algorithmic crux was the decisive limiter in only 1 of 5 pass@5 trials.**
The analyser's clusters:

- **Cluster A, operational (3 trials).** One agent ran the tool **zero** times on
  the live fabric ("the task was to write the script"); two ran it correctly once
  and then **again** as an idempotence check, which consumed the already-empty
  `pending/`, zeroed the counters and cleared `refused/`. Both would have scored
  40/43 on their first-run state.
- **Cluster B, in-progress timeout at 5400 s (2 trials).** One was at 40/43 with
  two residual bugs — `SCOPE.tsv` allowance propagation on deep relay chains, and
  `refused/` not created unconditionally. One was at 22/43 debugging a refusal
  ordinal bug and never touched the live fabric.

So **irreversibility fired 3 of 5 here**, consistent with
[[dynamo-security-network-forensics-playbook]] and
[[dynamo-security-authentication-and-authorization-playbook]] and against
[[dynamo-irreversibility-does-not-fire-on-a-careful-agent]]. What makes it fire:
the *report* is a graded artefact that the second run overwrites with an account
of a recompile that had nothing left to do — a redundant re-run is
self-destructive, not merely wasteful.

AVA flagged this before pass@5 ran: *"the pass@5 difficulty gate may lean on the
narrow operational trap rather than the algorithm."* It was right about the ratio
and wrong about the outcome — the gate passed comfortably.

## Levers that mattered here, with numbers

- **Two bundle bounds that each bind on their own.** With ~235-byte records,
  `(11, 2740)` made the two bounds cut at the same place: `bundle_limit_binds`
  survived on 6 of 7 sweep fabrics. A joint search over
  `limit ∈ [9,15) × bytes ∈ [2500,3400)` scoring "count-removal changes packing"
  and "byte-removal changes packing" independently found **`(13, 3335)`** — 4 and
  5 of 7. Do this search; do not pick the pair by eye.
- **Seed-searching brimful fabrics.** A bundle landing on *exactly* the byte bound
  has measure ~1/230 per bundle; ~200 seeds each found two hits for
  `held-brimful`, `sweep-f`, `sweep-g`. Needed in **two** sweep fabrics (or the
  `>=` mutant reads as caught-by-one) **and** one graded fabric.
- **The diamond plant for `carriers`.** Duplicating a session with equal weight
  does *not* produce equal-cost chains — the three `carriers` misreadings were
  wrong on **0/20** until I planted an explicit diamond: one border, two fresh
  intermediates, one fresh tip, weights chosen so `w1+w3 == w2+w4`, and the two
  last hops at **different relay allowances** so the tip is reached at two
  distinct optimal states. That one construction lit up all three (16/20 each).
- **`weight` merged by `min`, not `max`.** A domain-native inversion of the ported
  mold, and blind on the shipped fabric (20/20 held-out).

## Traps this build actually hit

1. **A merge can produce an invalid record.** `classes` is the ascending *union*
   of the group, capped at 8 by the schema; an `amend` that replaced one member's
   classes pushed a union to 9, and the *second* recompile then refused its own
   output — `held-brimful: not idempotent`. Fix: restrict amend/contend targets to
   sids whose merge key is nobody else's. **Always assert that every packed record
   passes the sieve** (`session_cause(rec, zones, set()) is None`) in the xcheck;
   idempotence depends on it and no mutation sweep sees it.
2. **A padding helper that overshoots.** `while len(text) + 13 <= width` while
   appending a **14**-character group produced tags of `LIMIT + 1`, so the
   "exactly at the tag limit" witness count was silently **0**. Same family as the
   trailing-separator bug in the auth playbook — check the witness *counts*, never
   just "the planting code ran".
3. **Unbounded state under mutation.** Deleting `if budget < 1: continue` makes
   the allowance go to −1, −2, … and the worklist never terminates; the probe
   burns the full 240 s timeout. Write that mutant as `if budget < 0:` instead —
   it is still a real semantic change (a spent allowance relays once more) and it
   halts.
4. **A provably-redundant guard is an unkillable probe.** `if state[2] < 1:
   continue` inside the backward walk could never change the answer (a budget-0
   state's successor is never in the state set), so its mutant survived. Delete
   the guard and the probe — [[dynamo-inert-rules-are-c3-holes]] applied to the
   reference rather than the spec.
5. **Inert *contract* clauses.** "keeping the groups in the order their first
   member stands" and "the order sessions stand in after this pass is …" were both
   immaterial once the packing sort is total. Reworded as set statements before
   pushing, so C3 has nothing unobservable to find.
6. **Docker Desktop on macOS cannot bind-mount `~/Documents`.** Stage
   `solution/`, `tests/` and `logs/` into `/tmp` and mount from there.

## Gate tensions

Same B5-vs-pass@ tension as the two security playbooks, resolved the same way:
**state everything, and put the difficulty in the shape of the shipped
instance.** Dynamo eval's `unambiguous` and QC's B5 both passed first try because
`RECOMPILE_RULES.md` has no gaps; pass@ still converted because settling
`(router, allowance)` states is expensive to *compute*, not hard to *know*.

The new tension: **the operational trap now carries more of the gate than the
algorithm.** Do not read that as "drop the algorithm" — the timeouts in Cluster B
were agents who had the algorithm 93% right and ran out of clock, so the algorithm
is what makes the operational trap reachable at all.

## Operational

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1800`. The suite runs
  **113 s under `--cpus=2 --memory=4g`** (Dynamo eval flagged the runtime as the
  one place timing could be tight — measure it at the manifest's CPU count, not on
  your laptop's core count).
- Solve times: the pass@2 solver finished in 19 steps / ~50 min of 90; the pass@5
  timeouts were at steps 19 and 30. There is no spare budget to spend on more
  volume — [[dynamo-volume-overshoots-the-band]] applies if this is ever ratcheted.
- Mutation sweep batched 3-wide: 144 probes × 7 fabrics in 33 s.
- `ctrf.json` was absent in **all seven** trials across both gates; the analyser
  fell back to `test-stdout.txt` every time. Harmless, but do not rely on ctrf.
