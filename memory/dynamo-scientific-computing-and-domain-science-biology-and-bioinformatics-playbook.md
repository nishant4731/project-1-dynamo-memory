---
name: dynamo-scientific-computing-and-domain-science-biology-and-bioinformatics-playbook
description: "PLAYBOOK — Scientific Computing and Domain Science / Biology and bioinformatics: dynamo/blightline-typing ALL-GREEN, pass@5 2 solved/3 good valid/avg 0.400; the complete-spec pipeline solved 2/2 until an optimum was asked for twice."
metadata:
  type: project
---

`dynamo-0e75ffc-scientific-computing-and-domain-science` · PR #1 · heads
`7d11f99` → **`e8104dd` ALL-GREEN** (2026-08-25). Task `dynamo/blightline-typing`.

## The mold

Rebuild-the-lost-program over a read-only run directory with a complete house
protocol. The agent writes `/app/blightline_type.py <run_dir> <out_dir>`, which
settles one week of SNP typing off a plant clinic's sequencers into three
byte-graded TSVs and a 51-counter JSON manifest. `BENCH_PROTOCOL.md` states all
sixteen sections, so `task_specification` was unanimous PASS and QC B5 never
came up. Difficulty lives entirely in the shape of the shipped instance and in
one rule that is cheap to state and expensive to obey.

`bench_intake.py` ships in the image: it reads the run directory into plain
values and its four writers lay down the exact bytes. Handing the plumbing over
is what kept solve times at 12–46 min instead of turning the task into typing.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `7d11f99` | **2 solved · 0 valid — BLOCKED, "too easy"** | never ran |
| `e8104dd` | 1 solved · 1 valid · "Rerun: NO" | **2 solved · 3 good valid · 0 timeouts · avg 0.400 — PASS** |

Cosine passed on both pushes (commit 2 changed `tests/test_outputs.py` and not
`instruction.md`; the in-flight head was not in the corpus, as
[[dynamo-inflight-heads-not-indexed]] says). Dynamo eval 31/31, duplicate
UNIQUE (closest TB2 lexical 0.126), AVA PASS, deep_review PASS, tier1 PASS,
qc_eval/qc_exec/qc_gate PASS, validation Docker/Oracle/Nop ✅.

## What drew the fails — quoted

> All three failures share **a single root cause**: brute-force exhaustive
> enumeration (`itertools.combinations`) for minimum panel selection timed out
> on the first held-out run.

> **Convergent across all five trials:** … For panel selection, every agent used
> `itertools.combinations` over sorted marker IDs, iterating k = 1, 2, … This
> convergence across all five independent runs is strong evidence of a shared
> training-data pattern for minimum-set-cover in Python.

> The training run, with a panel of only 3 markers from 34 retained, completed
> in negligible time regardless of algorithm — masking the deficiency, exactly
> as the task author anticipated.

The crux is therefore **an optimum whose idiomatic implementation is correct
and too slow, over a shipped instance small enough to hide that**. Not a
misreading — a complexity wall. Both passing trials also wrote
`itertools.combinations` and got lucky on panel widths.

## The 2/2 → 1/2 ratchet, in one commit

Head 1 was a complete, five-subsystem pipeline with eight starved branches and
it was solved 2/2 in 15 and 23 minutes. The analyser's verdict named the
problem exactly: agents "independently implemented … the fixed-point peel and
bounded panel search", because §6 and §10 *told them* to. Three changes:

1. **Stop narrating.** §6 stopped describing a procedure ("in rounds … until a
   round marks nothing") and instead stated the property — *the largest pair of
   sets that support each other*, with a two-line uniqueness argument. Same
   content, no map. The reading it rules out (count each isolate and marker
   once against the whole roster) is now byte-identical on the shipped week and
   different on 8 of 31 graded runs. See [[dynamo-do-not-narrate-the-trap]].
2. **Ask the optimum twice.** After the screening panel, a *confirming* panel:
   the smallest sufficient set drawn from the markers the screen did not take,
   empty where what is left cannot meet every demand. It roughly doubles the
   search, compounds a wrong primary, and adds a genuine "no answer" case
   (12 of 31 runs). This is the ML-playbook lever — a second minimum over the
   same graph.
3. **Sampling-point counters, nine of them**, per
   [[dynamo-sampling-point-counters-beat-the-ceiling]]. Two are *the crux
   counted rather than tabulated*: `isolates_short`/`markers_short` are the
   one-pass reading of §6 reported beside what the property actually keeps, and
   they agree on our own week and on almost nothing else.

Also added: a `private` column in `types.tsv` (fixed markers whose call no
retained isolate outside the type carries). That one drew the pass@2 valid
fail — an agent indexed "outside the type" by DFS discovery order after sorting
the types by date, so it was right whenever the two orders coincided.

## Levers measured not to work here

- **Starved branches alone.** Head 1 shipped 38 of 80 single-rule misreadings
  byte-identical on the shipped week — per-record lot windows, repeat-plate
  supersession, the lead factor, comparability, opaque pairs — and was solved
  2/2 anyway. A careful reader does not need the sample to check a rule that is
  written down. Cf. [[dynamo-sample-starving-does-not-beat-a-general-implementer]].
- **Volume.** Solve times were 15–23 min against a 60 min budget on the head
  that failed the gate; there was never a clock problem to exploit.
- **Stating the optimum plainly.** §10 said "smallest possible size" from the
  first commit and both head-1 agents implemented a bounded search. What
  converted them was not the rule but its *cost*, once the confirming tier and
  wider held-out panels put the idiomatic enumeration past 30 s.

## Hurdles, gate by gate

- **cosine_similarity** — passed both pushes, 1m10s–1m21s. No reskin was
  needed or attempted.
- **review / rubric** — 31/31 PASS on head 1. One advisory: the reviewer could
  not confirm `[task].description` against the Harbor schema and graded PASS
  conservatively. Left as is.
- **validation** — green first try. `bench_intake.py` must live at
  `/app/bench_intake.py`, not `/app/data/`: the oracle installs the program at
  `/app/blightline_type.py`, and `sys.path` gets the script's own directory, so
  a helper under `data/` is unimportable. Cost one Docker round-trip.
- **pass2** — the whole story above.
- **ava_review / deep_review / tier1 / qc_*** — all passed on the first head
  that reached them, with zero blocking items. Nothing to report, which is
  itself worth knowing for this subcategory.
- **trials** — 55 min, passed.

## Operational findings worth reusing

- **Cap the graded run and latch after the first wedge.** `RUN_SECONDS = 30`
  per settling plus a latch that refuses the remaining thirty-odd is what made
  this task's crux *scorable*: all three pass@5 failures are wedges, and each
  was read as a **good valid fail** rather than a verifier timeout. Without the
  latch a single hanging submission eats the 900 s budget and the trial is
  discarded as `infra/setup-timeout`. This is the single most load-bearing
  piece of harness in the task.
- **Give the probe control its own deadline.** With one deadline for both,
  `PROBE_SECONDS = 8` was fine locally and failed the control in-container
  (slower CPU) — the behaviour-preserving edit was "caught" by a timeout and
  the whole suite went red on a green oracle. Split them:
  `PROBE_SECONDS = 10`, `CONTROL_SECONDS = 90`.
- **Stop the mutation sweep at two catches.** The test only asks for ≥2 graded
  runs per probe. Early exit took the sweep from 466 s to 74 s; ordering the
  sweep list richest-first helps again.
- **Demand-domination pruning + branch on the most-constrained demand.** A
  plain include/exclude walk over markers hit 65 s on one seed; dropping
  demands another demand already forces, then settling the size by branching on
  the demand with the fewest covering markers with an antichain lower bound,
  brought the worst graded run under 0.6 s. Needed for the reference, and it is
  exactly what the agents did not write.
- **Any forge change invalidates a chosen seed set.** Seeds were picked by
  scanning 470 candidates for panel width, search time and witness coverage;
  two later forge edits shifted every run. Freeze the forge, *then* pick seeds.
- **`peel_rounds` had to go** when §6 stopped being a procedure — a counter
  that only exists inside the wording you removed is a spec inconsistency.

## The tension, and how it resolved

QC and the rubric want every rule stated precisely (`unambiguous` PASS,
`decisive_rule_disclosed`); pass@2 punishes exactly that, because a stated rule
is a transcribed rule. The resolution that worked here was **not** to withhold
anything: state the rule as a *property* rather than a procedure, and pick a
property whose obvious implementation is correct but intractable. B5 stays
satisfied — the answer is uniquely determined and the protocol says so — while
the agent still has to invent the algorithm. See
[[dynamo-b5-vs-pass2-determinability-pincer]] for the version of this tension
that could not be resolved by withholding.

## Known limitation left in

The two passing pass@5 trials also wrote `itertools.combinations`; they passed
because their held-out draws happened to need narrow panels. The gate therefore
rests partly on instance variance. Raising the minimum panel width across the
held-out corpus would make the discriminator sharper, at the cost of a slower
reference. Held back: the head is all-green and a redraw is a coin flip
([[dynamo-finding-a-defect-is-not-a-reason-to-cancel-a-run]]).
