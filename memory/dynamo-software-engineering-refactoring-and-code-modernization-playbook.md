---
name: dynamo-software-engineering-refactoring-and-code-modernization-playbook
description: "PLAYBOOK Software Engineering / Refactoring and Code Modernization — ALL-GREEN slipway-port codemod mold; pass@5 0 solved / 5 good valid / avg 0.000; the whole fight was finishability, not difficulty."
metadata:
  type: project
---

**Category:** Software Engineering · **Subcategory:** Refactoring and Code Modernization
**Repo:** `handshake-project-dynamo/dynamo-2a4ed10-software-engineering` · PR #1 ·
heads `547efac` → `ca52895` → `99cea09` → **`4848934` ALL-GREEN** (2026-08-25).

## The mold

**Write the codemod, not the patch.** `dynamo/slipway-port`: the agent writes
`/app/slipway_port.py <project_dir>`, which ports a plugin package across releases of
an invented host SDK and leaves a `ported/` tree plus `edits.tsv`, `deferred.tsv`,
`surface.tsv` and `port_report.json`. `SLIPWAY_PORTING.md` states all sixteen sections;
**nothing is withheld**, which is why qc_eval/qc_exec/qc_gate and AVA passed clean on
every head that reached them and B5 never came up.

Difficulty lives entirely in the **degeneracy of the shipped checkout**. Benchtop's own
package has no aliases, no re-exports, no star imports, no `__all__`, no shadowing, no
nested calls, no collisions, and a plan window crossing exactly one release — so the
natural implementation of every stated rule is byte-identical there and wrong on the
twelve held-out packages. Measured: **20 of 25** plausible misreadings byte-identical on
the shipped checkout and wrong on up to 10 of 12 held-out ones.

Refactoring/modernization is an unusually good fit for this mold, because the *natural*
code for a codemod (regex or a plain `ast.Name` match) is exactly right on a tidy package
and exactly wrong on a real one.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `547efac` | 0 solved · 0 valid · 1 in-progress timeout · **1 verifier stall** — BLOCKED | — |
| `ca52895` | 0 solved · **1 valid** · 1 in-progress timeout — PASS | 0 solved · **1 good valid** · **4 in-progress timeouts** · avg 0.000 — BLOCKED |
| `99cea09` | 0 solved · 0 valid · **2 in-progress timeouts** — BLOCKED | never ran |
| `4848934` | 0 solved · **1 valid** · 1 in-progress timeout — PASS | **0 solved · 5 good valid · 0 timeouts · avg@5 0.000 — PASS** |

Cosine passed **4/4** (instruction `0.67`, verifier `0.76` on head 1, never near 0.9).
Dynamo eval 31/31. Duplicate UNIQUE. deep_review, tier1, ava_review, qc_* all clean.

## The one fact worth carrying: this task never once failed for want of difficulty

`difficulty_crux` is **PASS on all 13 trials across four heads**, as are
`task_specification` and `approach_validity`. Every block was operational:

- **7 of the first 9 trials were in-progress timeouts.** An agent that does not finish
  produces no countable evidence, and the pass@5 gate wants ≥3 *counted* fails.
- pass@2 pins `override_timeout_sec = 3600` **whatever `[agent].timeout_sec` says**.
  Raising it 5400 → 7200 did nothing at pass@2; it only helps pass@5.

So the entire arc from head 1 to head 4 is: *give the clock back, never the crux*. On the
final head every trial finished and every trial was wrong.

## What drew the valid fails — quoted

> "Agents implemented fixed-point export iteration, scope-aware name resolution, and
> per-change reanalysis structurally correctly, but each implementation had bugs that the
> Benchtop sample tree (a tidy, single-package, single-release tree) never exercises. The
> gap becomes visible only on held-collide (quarantine propagation through star imports),
> held-nest/held-deep (scope shadowing), held-window/held-mixed (multi-release symbol
> chain replay)."

Five held-out trees failed in **all five** trials: `held-collide`, `held-nest`,
`held-window`, `held-deep`, `held-mixed`. **`held-collide` is the single most valuable
tree in the corpus** — it is also the only thing that beat the strongest agent ever seen
here (39/41 tests, 10/12 trees correct, dead on that one).

## The four cruxes that survived every trim

1. **The export closure is a least fixed point** over a package import graph that may
   contain cycles and star chains. The natural code — recursive resolution with a
   `visiting` set, or one pass in filename order — is right on a tree and only on a tree.
2. **Bindings are re-derived before every *change*, not once per step.** A change names
   its symbol by where the table holds it *now*, so `emit → send → (moves module) → resig`
   is a three-hop chain no one-shot matcher follows.
3. **Quarantine propagates.** A `name_collision` or `retired` name stops being exported,
   so modules that received it through the package silently stop holding it too.
4. **Nested calls are rewritten innermost-first**, with the outer call carrying the
   already-rewritten argument text.

## What was safe to hand over, and what it bought

Everything below moved into a shipped, read-only `/app/data/portkit.py` across heads 2–4.
None of it is judgement; all of it was costing agents their hour:

| handed over | why it was not difficulty |
|---|---|
| `read_project`, `write_*`, `splice`, `line_starts`/`span_of` | serialisation |
| `release_key`, `ordered_steps`, `planned_steps` | ordering |
| `start_symbols`, `advance` | replaying a stated table |
| **`top_imports`** | one trial read `node.module`/`node.level` off the AST instead of reassembling `.core` and silently dropped *every* intra-package import |
| **`tally_call`** | one trial took `calls_reordered` to mean an argument's *text* changed |
| **all 29 counters** | 29 definition coin-flips, none of them the subject |
| **`module_uses`, `top_level_binders` (§3b scope walk)** | ~160 lines of faithful Python-scoping AST enumeration; **two consecutive heads had agents die mid-fix here** |

The §3b call was the judgement call of the task: the difficulty suggestion listed §3b
*among the cruxes to preserve*, and I moved it anyway, on the measured evidence that it is
where the clock ran out twice. It was right — the next head went 5/5 good valid fails.
**Heuristic: if two consecutive heads show agents spending their last hour on the same
mechanical sub-problem, that sub-problem is volume, not difficulty, however clever it
looks.**

## Levers measured NOT to work here

- **Raising `[agent].timeout_sec`.** 5400 → 7200 changed nothing at pass@2 (pinned 3600)
  and did not save head 2's pass@5 (4 timeouts at 5400).
- **A complete, intricate spec on its own.** All 16 sections were stated from head 1;
  every gate liked it and agents still could not finish.
- **Trimming contract prose.** 449 → 408 lines moved nothing measurable. What moved the
  needle was cutting what the agent must *implement*, not what it must *read*.

## Hurdles, per gate, in the order they blocked

1. **pass@2 — verifier stall (head 1).** An agent finished correctly and scored 0 because
   the *verifier* hit its 900 s budget and wrote nothing. See
   [[dynamo-verifier-budget-from-worst-case]]: I had sized that budget from a 58 s
   **clean-oracle** run, forgetting a wrong submission costs far more (23 subprocess runs
   × `RUN_TIMEOUT` 300 = 6900 s worst case). Fixed by capping each run at 60 s **and**
   giving all runs a shared 480 s budget; measured worst case then ~500 s against 2700 s.
2. **pass@5 — 4 of 5 in-progress timeouts (head 2).** Fixed by handing over the counters,
   the replay, `top_imports` and `tally_call`.
3. **pass@2 — 2 of 2 in-progress timeouts (head 3).** Fixed by handing over the §3b scope
   walk and the binder counting.
4. **cosine, similarity, validation, review, tier1, ava_review, deep_review, qc_eval,
   qc_exec, qc_gate: never blocked, on any head.**

## Reusable machinery

- `dev/blind.py` — patch the reference into N plausible misreadings; report
  byte-identical-on-shipped vs wrong-on-held-out **and** how many sweep trees each kills,
  which doubles as a pre-check that every mutation probe will have ≥2 witnesses. Three
  rounds of corpus enrichment driven by that table took 143 probes to 0 survivors and
  0 caught-by-one.
- A `sheet` project built by the forge purely so §16's worked example is **generated**,
  with an audit test that its quoted rows obey the table specs — it can never drift.
- The pinned-bytes helper audit — see
  [[dynamo-shipped-helper-must-be-pinned-and-proven]]. Mandatory once you ship plumbing.
- Two adversarial cases for verifier stalling (a submission that sleeps for ever, one that
  sleeps 30 s per tree) and one that appends a line to the shipped helper.

## Gate tension

The usual B1/B5-versus-pass@2 pincer never fired, because nothing is withheld. The only
tension was **difficulty versus the clock**: the task was hard enough to be unfinishable,
and an unfinished trial is not evidence of anything. Resolve it by moving transcription
out, never by weakening a rule — the blindness table and the mutation sweep are the proof
that you have not.
