---
name: dynamo-security-network-forensics-playbook
description: "PLAYBOOK Security / Network Forensics — ALL-GREEN dragnet-restitch mold; pass@5 1 solved / 3 stratified good-valid / avg@5 0.200; the relay window + built convergence knots are what finally converted solvers."
metadata:
  type: project
---

**Category:** Security · **Subcategory:** Network Forensics
**Repo:** `handshake-project-dynamo/dynamo-2d0d4c3-security` · PR #1 ·
**ALL-GREEN on `646d13b`** (2026-08-23), run `32613614960`.
Earlier delivered task in this subcategory: `dynamo/tapline-recut` (`dynamo-6bb0151`).

## The mold

**Repair-in-place with a complete contract, difficulty in graph shape.**
`dynamo/dragnet-restitch`: a flow-correlation appliance died mid-fold. The agent
writes `/app/dragnet_restitch.py`, which sifts packed `segments/` and an unfolded
`inbox/` against six ordered rejection causes, folds operations in `seq` order
(files numbered in *flush* order), merges co-observations, re-takes every check
value, repacks under two segment bounds, rebuilds a byte-offset index, walks the
contact graph forward into `REACH.tsv` and backward into `PIVOT.tsv`, files
refusals with collision ordinals, spends the evidence and writes 35 counters.
`DRAGNET_CHARTER.md` (317 lines) states everything.

## Measured on the accepted head

| gate | result |
|---|---|
| pass@2 | **0 solved · 1 valid-fail · 1 in-progress-timeout**, Rerun Recommended: NO |
| pass@5 | **1 solved · 3 good-valid-fail · 0 soft-timeout · 1 in-progress-timeout · avg@5 = 0.200** |
| cosine | passed 24 consecutive times across the whole PR |
| everything else | green on the same head, first time all 17 jobs passed together |

## What actually drew the valid fails — the most reusable fact

The three failures were **stratified, not shared**, and the analyser's line about
the second is the whole thesis of this playbook:

1. **Edge-case trap** (`task__nFjUpZR`) — the tool passed the live dragnet and the
   simpler held-out ones, and failed on webbed / stalled / crowded / deep / quiet /
   noinbox / noscratch / brimful, on three separate bugs: per-segment byte-offset
   restart, a segment-packing boundary, and over-zealous sieve refusals.
   *"All bugs were invisible on the quieter live dragnet."*
2. **Analytical failure** (`task__oqbJ2aW`) — applied `duplicate_id` to inbox
   *amend/retract* as well as admits. **This is the exact rule a QC C3-exec finding
   had forced me to witness two heads earlier** — planting the witness to satisfy
   QC is what turned the rule into a converter.
3. **Operational** (`task__TWmobpg`) — algorithmically correct (45/48, all 13
   held-out pass); ran the tool twice on the live dragnet without restoring from
   the spare, and was cut off planning the restore-and-rerun.

## The lever that broke the ceiling: built convergence knots

Four heads solved 2/2 or 3/5 with a *stated* crux. What converted solvers was
**multi-arrival convergence, constructed rather than hoped for** — the platform's
own pass@2 difficulty suggestion named it:

> *"adding multi-arrival convergence points (multiple trails landing the same host
> at different times within a relay window) … The goal is a held-out corpus where
> the agent's first correct-looking implementation fails."*

Mechanism: a **relay window** (`RELAY_WINDOW = 380000`) caps how long a host holds
what a contact brought it, so a trail may only continue on a contact opening within
the window of its arrival. That single clause destroys the greedy scalar: an
earlier arrival can lapse before an onward contact opens that a later one is still
standing for, so arrivals stop being ordered by usefulness and must be carried as a
**set**, forward and backward. Then the forge *builds* the knot: hold the early
arrival, move the late one forward by a window plus a margin, and open an onward
contact inside the late arrival's window only.

Blindness table (patch the reference one line, grade the whole corpus):

| misreading | before knots | after |
|---|---|---|
| keeps only the earliest arrival | 10 of 13 | **12 of 13** |
| ignores the relay window (forward) | 12 of 13 | **13 of 13** |
| ignores the relay window (backward) | 12 of 13 | **13 of 13** |
| window exclusive above (forward) | 8 of 13 | **12 of 13** |

14 of 21 plausible readings stay byte-identical on the shipped dragnet.
**Build the gap by moving the LATE arrival forward.** Pushing the early one
backwards ran 51 real flows to a negative `first`, which is refused as malformed —
the knot silently deletes a share of itself. See
[[dynamo-plant-the-deep-knot-do-not-search-for-it]].

## Keeping the shipped instance blind

`parents=1` (a forest: one contact into each host, so a set *is* a scalar),
`span=8000` with 45000–60000 ms sessions so every wait falls in [334268, 358159],
inside the window — both naive readings invisible. `merge_agree=True`,
`contend=1`, `seq_tie=0`, `reclaim=0`, `edges=0`, `converge=0`, `window_edge=0`.
**Agent-visible surface never grew**: across four heads the charter went 315→317
lines, instruction stayed 59, the live dragnet stayed byte-identical. All the
difficulty lives in 3,188 lines of held-out corpus the agent never sees, so it
cannot lengthen the agent's work.

## Hurdles, per gate, in the order they blocked

1. **pass@2, repeatedly — the clock, not difficulty.** Two draws of
   `AgentTimeoutError` ×2 with `low_timeout` FAIL 0/2 and *"no signal of a task or
   verifier problem"*. Cause was mine: the instruction claimed the live dragnet was
   the only copy, so agents rationally deferred the single run until certain, and
   certainty does not fit in 3600 s. One trial had a working tool at 33 min and
   spent the remaining 25 re-reading its own code. Fixed by shipping
   `/app/data/dragnet.spare.tar` and asking for an early first pass —
   [[dynamo-irreversibility-costs-the-clock]]. Both trials finished next draw.
2. **pass@2 "too easy"** — 2/2 solved once the clock was fixed. Answered by the
   relay window, then by the knots.
3. **qc_exec C3-exec.** A mutation stopping an inbox `admit` from claiming its fid
   survived: every planted twin duplicated a *segment* record. Reproducing QC's
   method locally (mutate the **submitted solution**, grade through the verifier)
   found **12 survivors of 107**, six real — see
   [[dynamo-witness-must-be-load-bearing-per-path]]. After fixing: 0 of 105.
4. **qc_gate B5.** §5 enumerated provenance for every merged field except `label`,
   and no merge group anywhere disagreed about one, so a rival rule was
   indistinguishable. Fixed by stating it **and** making contending twins draw a
   different label — either half alone is the next gate's finding.
5. **trials.** 3 solved/1 valid → **1 solved/3 valid** with the knots.
6. Cosine, review, similarity, validation, ratelimit, AVA, deep_review, tier1,
   qc_eval: never blocked on the final lineage.

## Levers measured NOT to work here

- **A fewest-contacts (`hops`) column** over the same frontier: the corpus is
  layered, so hop count is forced by depth — naive reading agrees **13 of 13**, and
  still 10 of 13 after adding band-skipping contacts. Inert.
- **A "moments stood" column**: separates one variant, 11 → 12 of 13. Not worth it.
- **Breadth of blind branches**: 14 of 21 readings blind and agents still solved
  3/5. Confirms [[dynamo-widening-implementation-surface-measures-zero]].
- **Raising `[agent].timeout_sec`**: pass@2 caps at `min(timeout_sec, 3600)`, so
  nothing above 3600 reaches it; and at pass@5 the timed-out trial was mid
  restore-and-rerun, so more clock converts a *failure into a solve*.
- **Contention density alone** (`contend` 2→6, `seq_tie` 1→4, `merges` 8→13, etc.):
  did not move the blind surface (14 of 21 before and after). Kept because it is
  free, but it was the knots that moved the band.

## Gate tensions

**QC B5/C3 versus pass@**: B5 demands every rule be stated, and a stated rule gets
transcribed — *"No trial failed due to algorithmic deficiency"* on the pre-knot
head. Resolution is the whole mold: state **everything**, and put the difficulty in
the **shape of the shipped instance**. The knots satisfy both — the rule is fully
written, and the instance the agent can check structurally cannot exercise it.

Second tension: **C3 wants every bound witnessed, and every witness moves every
record**, which destroys the measure-zero byte-budget witnesses (a segment landing
exactly on 3450, and a boundary one over). Re-found by hand four times before
scripting it. Automate that re-search as a `reseed` step, and make sure two sweep
slots do not get pinned to the *same* seed.

## Operational

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1200`; suite runs ~20 s.
- pass@2 lost a trial to clock or infra on **four consecutive draws** — expect ~50%
  of pass@2 samples to be uncounted on a task this size, and re-run rather than
  re-tune ([[dynamo-timeouts-anchor-nothing]]).
- `docker cp dir container:/tests` **nests** when `/tests` exists; several
  measurements were silently taken against stale code —
  [[docker-cp-into-existing-dir-nests]].
