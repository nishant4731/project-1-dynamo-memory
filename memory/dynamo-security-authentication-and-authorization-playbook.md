---
name: dynamo-security-authentication-and-authorization-playbook
description: "PLAYBOOK Security / Authentication and authorization — ALL-GREEN delegated-authority reissue mold; pass@5 0 solved / 4 genuine, all five on the intended crux."
metadata: 
  node_type: memory
  type: project
  originSessionId: f484379e-e0c7-4cc9-9f11-b299c0ea870c
  modified: 2026-08-20T02:08:02.926Z
---

**Category:** Security · **Subcategory:** Authentication and authorization
**Repo:** `handshake-project-dynamo/dynamo-e320824-security` · PR #3 ·
heads `40a056f` → `365fcde` → **`b9a47ff` ALL-GREEN** (2026-08-20).

Two earlier PRs on this repo by other authors were closed: #1
`entitlement-snapshot-seal`, #2 `recover-guard-semantics` (blocked on QC **B5**,
"a rival rule reproduces all 13 disclosed demo answers"). Read them before
starting here — this subcategory attracts reverse-engineer-the-oracle molds, and
QC kills them for underdetermination.

## The mold

**Repair-in-place with a complete contract.** `dynamo/warrantbook-reissue`: an
access broker's reissue died mid-fold; the agent writes `/app/warrant_reissue.py`
which sifts packed `book/` leaves and an unapplied `intake/` against six ordered
rejection causes, applies operations in `seq` order (files numbered in flush
order), fuses co-issues on a five-part key, re-takes seals, repacks under two
leaf bounds, rebuilds a byte-offset index, resolves **delegated authority** into
`AUTHORITY.tsv`, files refusals with collision ordinals, spends the evidence and
writes 38 counters. `WARRANT_PROTOCOL.md` states everything — which is what keeps
QC B5 green where PR #2 died.

**The crux is the closure, starved by graph shape.** Per principal and power:
the fewest warrants that let it *exercise*, the fewest that let it *pass on*, the
greatest **carry** (a delegation budget, `min(tier, c-1)`, so a chain dies when
spent), and an **exposure** count of the principals on any conferring chain. The
shipped warrantbook is a depth-3 tree, one issuer per holder, every live warrant
at the tier ceiling, nothing back-dated — so open == pass on every row,
`exposure == span + 1`, first-found == shortest, and a single pass in packed
order already settles it.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `40a056f` | 1 solved · 1 valid-fail (Rerun: NO) | **3 solved · 1 good-valid · 1 infra · avg 0.600 — BLOCKED** |
| `365fcde` | 0 of 2 failed genuinely (partial, errored harbor job) | never ran |
| `b9a47ff` | **2 genuine of 2** — "Hard enough" | **0 solved · 4 genuine · 0 soft-timeout · 1 timeout — PASS** |

- Cosine passed every push: instruction **0.643 / 0.651 / 0.655**, verifier
  **0.811 / 0.808 / 0.805**, fingerprint ~0.77. Threshold 0.9.
- **qc_eval + qc_exec + qc_gate passed clean on the FIRST push**, empty
  `QC-FIXES-B64`, 37 checks. AVA PASS with no findings. deep_review PASS with two
  advisories. tier1 PASS. This is the payoff for a complete contract plus
  planted witnesses on both sides of every bound.
- Blindness table on `b9a47ff`: **16 of 22** plausible readings byte-identical on
  the shipped book and wrong on **8 to 19 of 19** protected ones.
- Mutation sweep: 143 probes, 0 survivors, none caught by a single sweep book,
  no-op control green. Verifier suite runs in ~10 s in-container.

## What finally converted the solvers

On the accepted head all five trials failed, `difficulty_crux` **PASS on every
one**, and all five landed on the intended crux. The analyser's own words:
*"The shipped live warrantbook is a simple tree that masks the bug, so the
agent's own self-testing passed, but the verifier's held-out corpus exposed
it."* The five sub-bugs, which is the most reusable list in this file:

1. missing `| {holder}` in the exposure set — the holder not counted as a member
   of its own chain;
2. a backward-only walk with no carry-state threading;
3. one exercisable map mirrored into the `pass` column (`open == pass` on every
   row) — the shipped book's exact degeneracy;
4. a fixed-point relaxation that settles on the wrong carry (43 vs 51);
5. **BFS/queue propagation instead of iterative relaxation — "correct on trees,
   diverges on non-tree graphs"**.

Every one of those is the *natural code*, not a misreading of the prose. That is
the whole lesson: a stated rule converts nobody, but a stated rule whose natural
implementation coincides with the correct one on the shipped instance converts
everybody.

## What the failures were about on the earlier heads

**Every single agent failure across both gates was operational, never the
closure.** pass@2: an agent wrote a fully correct program (34/42 tests green) and
*never ran it on the live book* — it read "assessed in whatever state you leave
it" as a warning against touching production. pass@5's one graded failure ran the
tool **twice** on the live book "to verify idempotence", wiping `rejected/` and
overwriting the report. The analyser's words: *"the author's intended crux was
not the failure point at all."*

So in this subcategory the irreversibility lever fires and the algorithmic one
does not — consistent with
[[dynamo-security-network-forensics-playbook]] and against
[[dynamo-irreversibility-does-not-fire-on-a-careful-agent]]. Making the report a
graded artefact the second run overwrites is what makes a redundant re-run
self-destructive rather than merely wasteful.

## Levers measured NOT to move solve rate here

- **Stating a harder closure.** A least-fixed-point with attenuation, a tier
  gate, shortest-chain counts and 11 blind misreadings still solved 3/5.
  Confirms [[dynamo-stated-algorithms-are-transcription-too]]: agents implement
  what section 7 says, however intricate, so long as it is *said*. What broke
  the ceiling was **a second, different computation over the same structure**
  (a forward/backward walk over principal-and-carry states) rather than another
  rule — and one whose naive answer, `span + 1`, is exactly right on the shipped
  tree.
- **Raising the density** of dead ends, relays, back-dating, loops and second
  chains across the graded corpus (the
  [[dynamo-contention-count-is-a-difficulty-dial]] lever): both trials that
  finished on that head still solved it.
- Adding volume: never tried, and the trials finish in 24–50 min of a 90-min
  budget, so there is no timeout pressure to trade against.

## The `harbor / pass@k` infra wedge — cost an hour, twice

Exactly the signature in [[dynamo-harbor-passk-status-never-posted]]:

- job log `the platform's 'harbor / pass@k' status did not finish within 60 minutes`
- analyser `pass@2: no valid agent failure (0 of 0 runs failed genuinely)`
- `GET /commits/<sha>/status` returns an **empty** `statuses` array
- the pass@2 sticky is **stale** — same trial ids and same golden values as the
  previous head ([[dynamo-sticky-timestamps-separate-infra-from-content]])

Close/reopen did schedule it — but the evaluation then came back
`error: The evaluation did not finish. Re-run it.` with only 2 of the runs
graded, twice, on two different harbor job ids. **New fact: a reopened
evaluation can error partway and the analyser will read the partial evidence as a
difficulty verdict (`0 of 2 runs failed genuinely`, `infra_only: false`).** Do
not read a `0 of N` verdict off an errored harbor job as "too easy" without
checking the status description and whether the sticky refreshed.

## Gate tensions

QC **B5** is the wall in this subcategory (it closed PR #2). The resolution is
the same one the vulnerability-analysis playbook reached: state *everything*, and
put the difficulty in the shape of the shipped instance rather than in what is
withheld. The cost is that the algorithmic crux stops converting solvers — which
is exactly what the pass@5 analysis said. Resolved by keeping the contract complete and adding a
quantity that is expensive to *compute* rather than hard to *know* — B5 stays
green because `exposure` is fully defined, and pass@ converts because the walk
that produces it is where implementations diverge.

## Operational notes

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1800` (suite ~10 s;
  the 465 s and 690 s runs I measured early were local Docker contention from
  other sessions' containers, not the suite).
- Batch the mutation sweep with a 3-thread pool inside the rig: 143 probes × 7
  books in ~8 s.
- `_exact_label(w)` style padding helpers emit a **trailing separator** when the
  remaining width is exactly 1 — that silently made a generated fixture line
  invalid and cost a debugging round.
- Randomise staged directory basenames by digest, not by slot: deep_review flags
  a program that could branch on `basename(argv[1])`.
