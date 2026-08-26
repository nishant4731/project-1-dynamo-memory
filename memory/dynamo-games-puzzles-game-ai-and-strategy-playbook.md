---
name: dynamo-games-puzzles-game-ai-and-strategy-playbook
description: PLAYBOOK Games Puzzles and Interactive Simulation / Game AI and Strategy — ALL-GREEN on ONE push; pass@5 2 solved / 3 good valid / avg@5 0.400; all failures on ascending-value cost settlement over a cyclic AND/OR graph.
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ba94501-4a7e-49b6-bdeb-3286ad99659d
  modified: 2026-08-25T03:23:16.617Z
---

**Category:** Games Puzzles and Interactive Simulation · **Subcategory:** Game AI and Strategy
**Repo:** `handshake-project-dynamo/dynamo-8865ada-games-puzzles-and-interactive-simulation` ·
PR #1 · head **`c50bd48` ALL-GREEN on the FIRST substantive push** (2026-08-25).

Third Games subcategory delivered with the repair-in-place mold, after
`dynamo/trumpline-reckon` (board-and-card) and `dynamo/lanternfall-restage`
(interactive-text). The mold ports cleanly; what is new here is the crux.

## The mold

**Repair-in-place with a complete contract, plus the mechanical half shipped.**
`dynamo/ashfen-resolve`: an archive of a two-sided siege duel died mid-build.
The agent writes `/app/ashfen_resolve.py`, which sifts packed `folios/` and an
unapplied `amendments/` against **seven** ordered discard causes, applies what
stood in sequence order, fuses the sorties two scribes drew twice on a five-part
key, re-takes marks, repacks under a record **and** a byte bound with a
per-folio byte-offset index, **solves the duel** into `VERDICTS.tsv`, files
discards with collision ordinals, spends `amendments/` and `scratch/`, and
writes **47** counters. `ASHFEN_RULES.md` states all of it in fifteen sections,
which is what keeps QC B1/B5 green.

`/app/data/wardwork.py` ships as an importable `wardwork`, **sliced out of the
reference by name** (`_ward_split.helper_source`) so the two cannot drift: the
schema, the mark, the seven causes in order, the rendering, the packing, the
writers, the discard filing, the readers and the spending. It holds no part of
sections 6–11. Intended solution: **487 lines** (crux ~175, driver ~218, report
~55).

## THE CRUX — the single most reusable fact

**Weighted retrograde game solving.** Not the verdict fixed point — the *cost*
settlement. Quote the analyser:

> *"The failures are stratified in severity but share a single conceptual root:
> all three agents failed to implement the iterative ascending-value
> (Dijkstra-style) fixed-point cost settling required by ASHFEN_RULES.md
> Section 9/10. No trial shows a different primary root cause."*

The board is an AND/OR graph. `verdict ∈ {host, hold, stall}` is the game value
with draws, stated as a least fixed point. `tempo` and `plies` are the **same
duel valued twice** — once counting a sortie as its `spend`, once as one. The
side the stance is settled *for* minimises and the other maximises, so:

- a stance its owner **wins** takes the **least** over the sorties that keep the
  win;
- a stance its owner **loses** takes the **greatest** over **every** playable
  sortie — which needs *all* its tails settled first.

Over weighted edges that is a **priority-queue sweep, not BFS and not DFS**: a
stance's cheapest winning sortie can be one that only settles later. Both the
verdict fixed point *and* the cost settlement must be iterative, because a
memoised recursion cannot tell a drawn position from one it is in the middle of
visiting.

**Two of three pass@5 failures reached for memoised recursive DFS
independently.** The analyser's read is worth carrying:

> *"The independent convergence on DFS across two trials strongly suggests this
> is a training-data-influenced default for 'cheapest path' problems, not a
> first-principles misreading."*

That is the lever: **pick a computation whose textbook default is wrong on your
instance class.** Shortest-path-shaped problems pull agents to DFS/BFS; make the
graph adversarial (min/max asymmetry) and cyclic and the default silently breaks.

## Measured on `c50bd48`

| gate | result |
|---|---|
| pass@2 | **0 solved · 1 good-valid · 1 in-progress-timeout** — "Rerun Recommended: **NO**" |
| pass@5 | **2 solved · 3 good-valid · 0 soft-timeout · 0 in-progress-timeout · 0 task-issue · avg@5 = 0.400 — "Difficulty OK"** |

pass@5 rubric: `task_specification` 5/5 PASS, `reward_hacking` 5/5 PASS,
`approach_validity` 5/5 PASS, `refusals` 5/5 PASS, `low_timeout` **5/5 PASS**
(31–88 min against the 5400 s budget), `difficulty_crux` PASS on all three
failures (NA on the two solves), `near_miss` 4/5.

- Cosine passed push 1: instruction **0.6512**, verifier **0.8248**, fingerprint
  **0.7885** (threshold 0.9). Duplicate check UNIQUE (best lexical rival 0.104).
- Dynamo eval **30 PASS + 1 N/A**, "Failures: None".
- AVA PASS, **no blocking items at all**. deep_review PASS, "Blocking Issues:
  None". tier1 PASS. qc_eval/qc_exec/qc_gate PASS — **37 checks clean, empty fix
  list `QC-FIXES-B64:W10=`**.
- Blindness table: **23 of 36** plausible readings byte-identical on the shipped
  ward and wrong on **8 to 20 of 20** protected wards.
- Mutation sweep: **162 probes, 0 unanchored, 0 survivors, 0 caught by one ward
  only**, no-op control still accepted.

## The shape starve — what the shipped ward hides

The shipped ward is a "short, quiet siege" and every crux reading is invisible
on it. Seven degeneracies, each an identity that holds **there and only there**:

1. one front;
2. every `spend == 1` → `tempo == plies`, `tempo_total == plies_total`,
   `book_spends == booked_stances`;
3. acyclic → `stalls_open == 0`, a DFS memo agrees with the fixed point;
4. every **losing** stance has exactly one open sortie → max == min,
   `losses_pinned == losses_faced`;
5. every **winning** stance has exactly one *winning* sortie → every book
   tie-break inert;
6. no reached fallen stance has an open sortie → `sorties_behind_fallen == 0`,
   so walking on through a fallen stance changes nothing;
7. nothing named that a duel cannot arrive at → `stances_named ==
   stances_reached`.

pass@2 confirmed the starve directly: *"The live ward, whose graph topology did
not expose this bug, passed byte-for-byte; the harder held-out wards did not."*

## Hurdles, per gate, in the order they blocked

**Nothing blocked on GitHub.** Every gate passed on push 1. The real hurdles
were local, and all of them were mutation-sweep survivors:

1. **First sweep: 19 survivors.** Seven were *provably equivalent* mutations,
   i.e. **inert rules** — remove the clause, not the probe:
   `discard_entry_unsorted` (the entry dict literal was already alphabetical →
   reordered it so `sort_keys` is load-bearing); `folio_never_starts_empty` (a
   record can never exceed the byte budget → deleted the clause from §12 *and*
   the engine); `moves_from_unsorted` (sorting a stance's sorties never reaches
   an answer → deleted the sort); `raise_appends_at_the_end` (fusion + repack
   erase insertion order → deleted the `order` list); `report_lines_discarded`
   (two discard tuples can never be equal); two verdict probes that were exact
   equivalents. The rest named **missing fixtures**.
2. **`folio_record_bound` survived twice.** With capacity 7 and budget 1663 the
   record bound never bound *decisively* — an 8th record could never fit anyway,
   so `>=` → `>` was a no-op. Fixed by **capacity 6 / budget 1279** with
   ~180-byte records, so a 7th record genuinely fits on short-label wards. Both
   bounds must be able to bind, not merely coincide.
3. **`folio_byte_bound` needs a folio landing *exactly* on the bound** in ≥2
   sweep wards — measure-zero, found by seed search.
4. **Book tie-breaks were unwitnessable.** A secondary tie-break on the *other*
   cost column can essentially never fire. Fixed by **splitting the two decided
   classes across the two columns**: class 1 (winning) settles on `tempo`,
   class 3 (losing) on `plies`. Both columns become primary somewhere, every
   probe fires, and the rules got *simpler*.
5. **Verifier runtime.** 162 probes × 7 sweep wards took **17m44s** in-container
   at `cpus=2`. Raising `[environment].cpus` 2 → 4 and
   `ThreadPoolExecutor(max_workers)` 3 → 4 took it to **8m40s**; verifier
   timeout set to 3600 s for ~7× headroom.

## Levers measured NOT to work here

- **Raising `[agent].timeout_sec` to help pass@2.** pass@2 pins **3600 s**
  regardless — confirmed a further time. One pass@2 trial wrote a fully correct
  resolver (13/13 unseen wards) and was **~2 minutes** from the live-ward run
  when the override fired. pass@5 honours 5400 s and showed **0 timeouts across
  5 trials**, so this is not a volume problem: do not trim, do not ratchet.
- **Trimming volume after the pass@2 timeout.** Explicitly rejected. The
  lanternfall reflex (`provide-the-plumbing-clears-the-hard-side`) applies to the
  signature `difficulty_crux PASS + low_timeout FAIL` **repeated across trials**;
  a single trial at 99% of a *pinned* budget is infrastructure, not evidence.
- **Pushing the advisory cleanup.** Both Dynamo eval and deep_review flagged a
  stray inert module docstring in the generated oracle file, twice, as
  advisory/never-blocking. Not pushed: a push re-runs pass@2 and **redraws
  pass@5** on a head already in the band. Do not redraw an all-green head.

## Gate tensions seen here

**The §9 pointer.** `instruction.md` tells the agent to implement section 9's
*second* (fixed-point) statement — a fairness/B5 guard against reading "stall"
as "not settled yet". Dynamo eval graded it PASS but called it **"Borderline
(instruction_concision / §9 pointer) … a reviewer who reads this as an approach
hint could dock it"**. pass@5 settled the argument empirically: **three of five
agents still failed on exactly that stage**, one of them after quoting the
material. Disclosing the *reading* does not disclose the *algorithm* — the
difficulty is in ascending-value settlement over a cyclic graph, which no amount
of stating the semantics hands over. Keep the pointer.

**Root-privilege dependency.** `require_isolation()` fails the whole grade unless
the verifier runs as root so it can drop to uid 65534. Dynamo eval noted it as
an operational dependency, not a defect ("fail-closed rather than grade an
un-isolated run"). Both ALL-GREEN siblings do the same. Leave it.

## Generator lessons (this subcategory needs a constructive builder)

The quiet-ward guarantees above are **not** reachable by a random graph plus
seed search. Build **verdict-first, in ranks**:

1. Lay every stance down rank by rank with the side it is *meant* to fall to and
   its owner, top rank = the stands, bottom rank = the fallen.
2. *Then* wire: a stance meant to win gets exactly one sortie to a tail already
   settled for its owner plus `fan` losing ones; a stance meant to lose gets
   `wide_loss` sorties, all to tails settled for the other side.
3. Every rank must hold **both** owners and **both** verdicts, or the wiring has
   nothing to reach for.
4. Attach any stance nothing reached under a *winning* parent of the opposite
   owner — one more losing sortie cannot change what the rules say.
5. `prune_unreached` for the shipped ward only, so `stances_named ==
   stances_reached` holds there.

**Then verify the guarantees after the fact and seed-search.** Amendments perturb
the graph — a `strike` can remove the one winning sortie and turn a win into a
stall. Write a `quiet_faults()` checker (acyclic, all spends 1, one sortie per
loss, one winning sortie per win, the six counter identities) and search seeds
until it returns empty; 100/100 seeds passed once the builder was right.

**Pin measure-zero seeds LAST.** Any forge edit re-packs everything and
invalidates an exact-byte-bound seed. This cost three extra search rounds. Do
every content change first, then search, then freeze and stop editing.

See [[dynamo-games-board-and-card-games-playbook]],
[[dynamo-games-puzzles-interactive-text-games-playbook]],
[[dynamo-inert-rules-are-c3-holes]],
[[dynamo-search-the-fixture-for-its-own-edge-witness]],
[[dynamo-pass2-overrides-the-agent-timeout]],
[[dynamo-plant-the-deep-knot-do-not-search-for-it]].

## Operational

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 3600`, `cpus = 4`,
  `memory_mb = 8192`. In-container suite 8m40s; `ctrf.json` present in all five
  pass@5 trials.
- `expert_time_estimate_hours = 5`; solves came in at 49 and 88 minutes.
- Corpus: 1 shipped + 13 held-out + 1 salted (keyed to the submission digest) +
  7 sweep + 1 format-sheet, all from one seeded builder.
- Nine local abuse routes each earn 0 (wrong `plies`, walk through the fallen,
  replayed live answer, edited rules, edited plumbing, crux hidden inside the
  installed module, symlinked folio directory, half-run draft, never run).
