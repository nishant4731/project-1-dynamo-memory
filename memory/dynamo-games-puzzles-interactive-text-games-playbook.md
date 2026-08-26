---
name: dynamo-games-puzzles-interactive-text-games-playbook
description: "PLAYBOOK Games Puzzles and Interactive Simulation / Interactive text games — ALL-GREEN puzzle-progression restage mold; pass@5 0 solved / 3 good valid, all five failures on the route crux."
metadata:
  type: project
---

**Category:** Games Puzzles and Interactive Simulation · **Subcategory:** Interactive text games
**Repo:** `handshake-project-dynamo/dynamo-568d798-games-puzzles-and-interactive-simulation` ·
PR #1 · heads `d122117` → `52bbfa6` → `cb22ad0` → **`df461d2` ALL-GREEN** (2026-08-23).
Four heads, one PR, no reskin ever needed.

## The mold

**Repair-in-place, with the crux in a puzzle-progression fixed point.**
`dynamo/lanternfall-restage`: a parser game's world build died mid-fold; the
agent writes `/app/lanternfall_restage.py`, which sifts packed `warren/`
passages and an unapplied `revisions/` against six ordered refusal causes,
applies moves in `seq` order (files numbered in *flush* order), fuses twins on a
five-part key, re-takes marks, repacks under two leaf bounds, rebuilds a
byte-offset index, walks the progression into `PROGRESS.tsv`, files refusals
with collision ordinals, spends `revisions/` and `drafts/`, and writes 39
counters. `STAGE_CANON.md` states everything.

**The crux — new, and the most portable thing here.** A **mutually recursive
least fixed point over scenes and tokens**: a way is walked only once its `head`
has been stood in AND every token in its `keys` is in hand, and it lands the
walker in its `tail` `cost` turns after the **latest** of those moments. Two
further columns are different computations over the same structure:
`route` (how many distinct scenes lie on *some* run to a scene — a union over
runs) and `linchpin` (the lowest token a scene cannot be reached without,
answered by striking every way demanding a code and re-walking).

**The starve is graph shape.** The shipped playhouse is one act, every way one
turn, every key in hand before the way that wants it, exactly one run into each
scene. On it a single sweep in packed order settles every turn,
`route == depth + 1`, and the lowest key demanded on the way *is* the linchpin.

## Measured on the accepted head

| head | pass@2 | notes |
|---|---|---|
| `d122117` | 0 solved · 0 valid · **2 timeout** | crux PASS, low_timeout FAIL ×2 |
| `52bbfa6` (ship the I/O plumbing) | **1 solved · 1 valid · 0 timeout** | agents finished at 49 and 57 min of 60 |
| `cb22ad0` | 0 solved · 0 valid · **2 timeout** | one trial lost 774 s to a single LLM call; another had one streaming call in flight **57 minutes** |
| `df461d2` (ship the sieve too) | **0 solved · 1 valid · 1 timeout — PASS** | |

**pass@5 on `df461d2`: 0 solved · 3 good-valid-fail · 0 soft-timeout · 2
in-progress-timeout · avg@5 0.000 — "Difficulty OK".**

Rubric across all five trials: `task_specification`, `reward_hacking`,
`difficulty_crux`, `near_miss`, `refusals`, `approach_validity` **all PASS 5/5**;
only `low_timeout` FAIL ×2.

Cosine passed all four pushes: instruction **0.634 → 0.632**, verifier
**0.856 → 0.803**, fingerprint **0.801 → 0.778**. Dynamo eval 30 PASS + 1 N/A on
push 1. Duplicate check UNIQUE every time.

## What actually drew the valid fails — quote this

> *"Every failure lands exactly on the route/PROGRESS.tsv crux the task author
> identified."*

Two independent misimplementations, and the first is the whole lesson:

1. **Backward dependency closure for `route`** (2 trials) — build `dep[i][j]`,
   BFS from passages whose tail is the target, accumulate heads/tails.
   *"On the live playhouse (one act, trivially linear runs) this happens to
   coincide with the reference. On complex held-out playhouses with multiple
   acts, key detours, and back-walks, the closure either over- or under-counts."*
2. **Exponential DFS for `route`** (2 trials) — semantically correct recursive
   enumeration of all valid passage sequences; one agent *explicitly logged the
   O(n!) risk at step 27 and submitted anyway*. Fine on the small shipped house,
   120 s subprocess timeout on 17 held-out runs. **A performance trap is a free
   second discriminator when the shipped instance is small and the held-out ones
   are not** — "Ours is a small, quiet house. Theirs are not" earned this.
3. Two trials never reached the live house at all.

## The lever that decided this task: cut volume by MEASUREMENT

Both timeout heads were the "hard side" signature from
[[dynamo-provide-the-plumbing-clears-the-hard-side]]: `difficulty_crux` PASS +
`approach_validity` PASS + `task_specification` PASS + `low_timeout` FAIL. The
fix is to remove budget without removing difficulty, and the way to pick *what*
to remove is to count lines per function in the intended solution:

| region | lines | share | ever decided a trial? |
|---|---|---|---|
| sieve (6 causes + shape predicates) | 97 | 22% | **never** |
| walk / route / linchpin | 145 | 33% | every failure |
| restage body (read, apply, fuse, pack, count) | 204 | 46% | once (a newline) |

Two cuts, in this order, took the intended solution **685 → 564 → 416 lines**:
ship the byte-layout I/O, then ship the sieve. Neither touched the crux.

**`[agent].timeout_sec` is honoured at pass@5 but NOT at pass@2** — pass@2 pins
3600 s regardless (confirms [[dynamo-pass2-overrides-the-agent-timeout]]). So
size the cut to clear 3600 s; pass@5's 5400 s then gives agents room to finish
and be wrong, which is what a countable valid fail requires.

## How to ship a plumbing module safely

- **Slice it out of the reference by name** (`ast`, a declared name list) at
  freeze time, so the shipped module *is* the reference's own code and cannot
  drift. A hand-maintained copy would.
- **Stage the verifier's own copy into every graded run** (`sys.path[0]` is the
  scratch dir, so it shadows site-packages). Editing or replacing the shipped
  module then buys nothing.
- **The oracle must import it** — that is what proves the wiring.
- Install it into `sysconfig.get_paths()["purelib"]` so `python3 -s -E` still
  finds it (`-E` kills `PYTHONPATH`; `-s` only kills the *user* site dir).
- **`chmod 0444` does not stop the agent** — it runs as root. Pin the digest of
  both the readable copy and the installed copy instead, and say in the
  instruction that the module is graded as it shipped, so an agent who splits
  their code into it fails for a stated reason rather than a surprise.
- Guard the invariant **structurally**: assert the module defines exactly the
  declared function list. A blunt word-blacklist false-fires on column names
  (`depth`, `route`, `linchpin` all appear in `PROGRESS_COLUMNS`).

## Hurdles, per gate, in the order they blocked

1. **pass@2, twice** — in-progress timeouts, both times. See above.
2. **qc_gate B1 + B5 (one round).** Real defect, mine. §8 said a run is a
   sequence in which every passage's `head` is *"an act's opening or the tail of
   an earlier passage"*. A passage whose head **is** an opening satisfies that
   **at any position**, so an unrelated passage could be parked at the front and
   its scenes would count toward `route`. The reference never computed that.
   Fix: define a run in four numbered parts, the fourth being that every passage
   other than the last is one a later passage needs (its `tail` is a later
   `head`, or its `drop` is a later `key`). See
   [[dynamo-support-definitions-admit-padding]].
3. **qc_gate E5 (amber).** Four audit functions opened files under `/app/data`
   directly. Every audit read now goes through the symlink walk, plus a
   whole-tree refusal.
4. cosine, static, Dynamo eval, duplicate, validation, deep_review, ava_review,
   tier1, qc_eval, qc_exec: **never blocked, on any push.**

## Levers measured NOT to work here

- **Raising held-out density on its own.** Back-walk/braid/cost density up on 8
  held-out houses moved the blindness table not at all (13 of 24 both before and
  after) and did not change the pass@2 outcome. It costs the agent nothing —
  they never see those houses — so it is safe to pair with an ambiguity fix, but
  it is not what converts.
- **Two probes were provably unkillable, not unwitnessed:** a `(seq, file, line)`
  sort tie-break (Python's stable sort already yields line order) and preserving
  twin-group insertion order (a later sort erases it). Both were **deleted from
  the engine and the canon**. An inert clause QC C3 can mutate for free is worse
  than no clause.

## Gate tensions seen here

QC B1/B5 demand every rule be pinned precisely, and a precise rule is one the
agent can implement. Resolved the same way the security playbooks resolve it:
state everything, keep the difficulty in the **shape of the shipped instance**,
and pair the ambiguity fix with a shape-only ratchet that costs no reading. The
`route` definition ended up *more* precise than before and still defeated 5/5.

**Prove the wording against the computation.** `dev/runcheck.py` brute-forces
the canon's four-part run definition over **every subset** of the open passages
of two small hand-built houses (one braided with a key detour, a back-walk and a
locked wing; one where two acts share a token pool) and asserts it reproduces
the reference's `route` column. That is what turns "I think the prose matches the
code" into a checked fact, and it is cheap — do it for any definition stated as
an enumeration.

## Operational

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 2700`; in-container
  suite ~2–4 min (47 tests, 168 probes over 7 sweep houses, 3-thread pool).
- `expert_time_estimate_hours = 6` drew a note in the trials analysis that
  90 min is "structurally tight" — it did not block, but keep the two within ~2x
  if you can.
- Corpus: 1 shipped + 12 held-out + 1 salted (keyed to the submission digest) +
  7 sweep + 1 format-sheet, all from one seeded builder.
