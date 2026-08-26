---
name: dynamo-build-dependency-and-release-management-ci-cd-pipelines-playbook
description: "PLAYBOOK Build Dependency and Release Management / CI/CD pipelines — ALL-GREEN on push 1 with the early-cutoff cutover mold; pass@5 1 solved / 3 good valid / avg 0.200."
metadata:
  node_type: memory
  type: project
---

**Category:** Build Dependency and Release Management · **Subcategory:** CI/CD pipelines
**Repo:** `handshake-project-dynamo/dynamo-6459436-build-dependency-and-release-management`
· PR #1 · head **`5300911` ALL-GREEN on the first substantive push** (2026-08-22).

## The mold

**Repair-in-place with a complete contract, ported from
[[dynamo-security-authentication-and-authorization-playbook]].** `dynamo/gantry-cutover`:
a monorepo build gantry's overnight *incremental* cutover died mid-pass. The agent
writes `/app/gantry_cutover.py` taking a pipeline directory, and must sift a flushed
`spool/` against five ordered causes, apply a `queue/` of `enlist`/`revise`/`retire`
amendments **in sequence order** (files are numbered in flush order) judged against the
state at that instant, prune dead edges, resolve fingerprints and surfaces, compute
critical seconds, time the rebuild against per-suite runner slots and gate exclusivity,
and write `CUTOVER.tsv`, `plan.ndjson`, `refused.tsv`, a repacked/resealed `spool/`
and 31 counters. `CUTOVER_HANDBOOK.md` states **everything** — which is what kept QC
B5/C3 green on push 1.

**The crux is early cutoff, starved by the shipped pipeline's shape.** A target's
*fingerprint* folds its files' `body` digests with the **resolved surface** of each
dependency; it runs when that differs from its recorded stamp. Its *surface* folds its
files' exported `face` digests with the surfaces of the dependencies it **re-exports**
(`carries ⊆ deps`), and a **cached target keeps the surface it already had**. So a
body-only change rebuilds a target and leaves everything below it cached — the real
ABI-hash/early-cutoff behaviour of Bazel/Buck, and the thing a plain cone invalidation
gets wrong.

## What made the shipped pipeline blind

Five deliberate degeneracies in the fixture the image ships (all measured, all zero in
`dev/traits.py`), each disclosed only as "ours is a small, quiet estate; theirs are not":

1. target ids already run in dependency order → `for tid in sorted(held)` is correct there;
2. every target re-exports **all** its dependencies → the surface fold and the
   fingerprint fold read the same list;
3. every revised file moves its `face` as well as its `body` → the rebuild set is
   exactly the downstream closure, i.e. what cone invalidation gives;
4. the roster has runner slots to spare → nothing ever queues and the priority rule
   never decides anything;
5. no two targets share a gate.

`dev/blind.py` measured **12 of 32 plausible misreadings byte-identical on the shipped
pipeline and wrong on 8–16 of 22 protected ones**: cone invalidation (13/22), folding
`deps` instead of `carries` into the surface (13/22), resolving in tid order (9/22),
recomputing a cached surface (9/22), three readings of the slot budget (13/13/14),
two of the gate (9/13), two of the priority (11/16), and reading a retire's `void`
test off `carries` (8/22). The other 20 misreadings **are** caught on the shipped
pipeline on purpose — sieve, queue ordering, byte layout and counters all give honest
local signal, which is what keeps the task fair.

## Measured

| gate | result |
|---|---|
| cosine_similarity | instruction **0.6607**, verifier **0.8382**, fingerprint **0.7608** (threshold 0.9) |
| static | 25 of 25 ✅ |
| Dynamo eval (rubric) | **PASS**, all criteria |
| duplicate | **UNIQUE** (closest TB3 `production-planning`, lexical 0.083) |
| validation | Docker ✅ Oracle ✅ Nop ✅ |
| **pass@2** | **1 solved · 1 valid-fail · 0 timeouts — "Rerun Recommended: NO"** |
| ava_review | PASS, no findings |
| deep_review | PASS, 0 blocking, 3 advisories |
| tier1 / qc_eval / qc_exec / qc_gate | PASS, **37 checks clean, `QC-FIXES-B64:W10=` (empty) on push 1** |
| **pass@5** | **1 solved · 3 good-valid · 0 soft-timeout · 1 in-progress-timeout · avg@5 0.200** |

## Which crux drew the valid fails — quoted

Only **one** of the three was the algorithmic crux, and the analyser named it:

> "All 9 complex held-out pipelines failed; the 3 simplest passed — a signature of
> the fingerprint/surface shape trap the author identified as the intended crux."

That trial (`task__SxoZzhu`) classified **every** target as `cached`
(`bundles_run` 0 vs 4) — the fingerprint payload composition or the carries-subset
surface fold was wrong, and its own testing on the shipped pipeline could not show it.

**The other two valid fails were operational, exactly as in
[[dynamo-security-authentication-and-authorization-playbook]]:**

- `task__kjvNxNq` ran **draft scripts on the live pipeline** at steps 8–18, consuming
  `queue/` and `stage/`; its final script was correct (40/42 tests pass) but the live
  pipeline was already spent.
- `task__6cLzeij` built a correct tool, passed all 12 held-out pipelines on `/tmp`
  copies, then at step 32 **explicitly declined to run it on production**, deciding the
  task asked for "the tool, not executing it on the production gantry".

So the irreversibility lever fires **twice as hard as the algorithmic one** in this
family of subcategories. Confirmed now on two consecutive ALL-GREENs. Contradicts
[[dynamo-irreversibility-does-not-fire-on-a-careful-agent]] for repair-in-place molds.

The pass@2 valid fail was neither: a **−3 byte `bytes_written`** undercount, identical
across all 13 failing tests, with `near_miss: FAIL`. `bytes_written` is a reliable
near-miss generator — cheap to state, hard to get exactly right — but it produces
`near_miss` fails, not crux fails. Keep it; do not rely on it.

## Hurdles, gate by gate

**There were none.** Every gate passed on the first push. What bought that:

- **cosine** — a genuinely different domain and a different core trap from the
  lineage's recent heads. Instruction facet 0.66 is the lowest I have measured;
  porting the *mold* while changing the *subject* is what does it
  ([[dynamo-port-the-mold-to-a-fresh-subcategory]]).
- **QC B5/C3** — state every rule, then plant a witness for **every** clause:
  22 spool lines each breaking exactly one field rule, 14 queue lines each breaking
  exactly one op-shape rule, combined-fault records that pin each adjacent pair of the
  cause order, and a settled target sitting on each inclusive bound with a refused line
  one step past it. `dev/sweep.py` (151 probes, **0 survivors, 0 caught by one
  pipeline**) is what proves it before pushing.
- **deep_review / AVA** — the salted pipeline keyed to `sha256(submitted_program)` is
  what AVA cited as closing the precompute bypass.

## Levers measured NOT to work here

- **Making the schedule observable per-lane.** The first design gave each runner a
  *lane id* reported in `CUTOVER.tsv`. That made pick order decide lane assignment even
  with zero contention, so `lane_capacity_ignored` and every priority misreading were
  **DIFFERENT on the shipped pipeline** — the whole scheduler stopped being a starve.
  Replacing lane ids with a **per-suite slot count** and reporting only `start`/`finish`
  turned five schedule misreadings blind at once. *If a rule's only observable effect is
  a value the shipped instance still discriminates, it is not a starve.*
- **A `cost` tie-break in the priority key.** Unwitnessable — no pair of equal-crit,
  unequal-cost contenders arises naturally. Dropped it for `(-crit, tid)`; one fewer
  inert clause. Same for `retire`'s `other != tid` guard (self-deps are already
  refused) and for writing a literal `"0"` in the cached `crit` column (it made
  `crit[tid] = 0` dead code, so the mutation survived).
- **Sample-starving alone.** `[[dynamo-sample-starving-does-not-beat-a-general-implementer]]`
  still holds: 2 of 5 trials implemented the whole spec correctly. What converts is the
  starve **plus** irreversibility **plus** a deliverable large enough to wedge Terminus-2.

## Gate tensions seen here

- **QC C3 wants every clause witnessed; witnesses add clerical volume.** 69 refused
  lines per pipeline is a lot of `refused.tsv`. Resolved by making all of them fall out
  of *one* validation function — volume of data, not volume of reasoning.
- **`near_miss` vs difficulty.** The exactness surface (31 counters, byte layouts) is
  what makes the task gradeable, but it generates `near_miss: FAIL` verdicts. Keep the
  crux failures reachable so the analyser has something better to point at.

## Operational notes

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1800`; the suite runs in
  **35 s** in-container (42 tests, 151 probes on 3 threads). pass@2 took 1h6m, trials
  1h38m.
- The one in-progress timeout was a textbook **Terminus-2 heredoc wedge**: ~40 of 90
  minutes on two LLM calls generating a ~600-line script, both corrupted by heredoc
  artifacts, timing out with a 17-line stub on disk
  ([[dynamo-heredoc-wedge-dominates-large-deliverables]]). A ~600-line reference is the
  ceiling for this agent; do not go bigger.
- **`ctrf.json` was absent in all seven trials** because `test.sh` does not pass
  `--ctrf` (copied from the previous ALL-GREEN task, which also omitted it). Nothing
  failed, but the analyser had to source golden-vs-agent values from
  `verifier/test-stdout.txt`. Add `--ctrf /logs/verifier/ctrf.json` next time — it is
  free and it makes the trial feedback richer.
- `dev/` holds the whole gate: `freeze.py` (fixture + format sheet + pins, idempotent),
  `traits.py` (the five degeneracies, as numbers), `blind.py` (the blindness table),
  `sweep.py` (151 probes), `localrun.sh` (oracle/nop via the manual Docker fallback),
  `attack.sh` (installs a wrong reading as the submission), `tamper.sh`
  (handbook/roster/symlink/double-run).
