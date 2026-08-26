---
name: dynamo-model-training-and-ml-infrastructure-fine-tuning-playbook
description: "PLAYBOOK Model Training and ML Infrastructure / Fine tuning — ALL-GREEN skein-blend mold; pass@5 1 solved / 4 good valid / avg 0.200; the dated-settlement lever and the plumbing that converted a timeout."
metadata:
  type: project
---

**Category:** Model Training and ML Infrastructure · **Subcategory:** Fine tuning
**Repo:** `handshake-project-dynamo/dynamo-7aea78b-model-training-and-ml-infrastructure`
PR #1 · heads `e575ff4` → `82c1376` → `3c898a6` → `d8aae8e` → **`2b131ee` ALL-GREEN** (2026-08-25).

Earlier delivered task in this exact subcategory on this account: `dynamo/lora-replay`
(`dynamo-ee83fbf`) — deterministic LoRA replay plus counterfactual influence. Repo
already deleted, so treat it as **in the cosine corpus**: stay away from adapters,
optimizer replay, influence/Shapley, and bitemporal `(effective_tick, revision,
ingest_tick)` record selection. Cosine passed 5/5 here without a reskin.

## The mold

**Compile-a-deliverable from a sharded corpus, complete contract, difficulty
entirely in the degeneracy of the shipped instance.** `dynamo/skein-blend`: the
agent writes `/app/skein_blend.py <blend_dir>`, which compiles a supervised
fine-tuning *blend* out of `protocol.json`, `sources.json`, `notices.jsonl` and
`shards/*.jsonl`, and writes `admissions.tsv`, `lineage.tsv`, `quota.tsv`,
`blend.tsv` and `blend_report.json` back beside them. `SKEIN_PROTOCOL.md` states
all 16 sections — which is why qc_eval/qc_exec/**qc_gate** and B5 were never an
issue on content.

The domain is genuinely fine-tuning: licences and takedown notices over training
data, provenance back to human-authored seeds through synthetic derivation, near
duplicate clustering, and a per-stage token mixture policy.

## Measured, head by head — the whole point of this file

| head | ratchet added | pass@2 | pass@5 |
|---|---|---|---|
| `e575ff4` | first substantive push | 0 solved · **2 task/verifier** | — |
| `82c1376` | §2 fix + carry between domains | 1 solved · 1 valid | **4 solved · 1 valid · avg 0.800 — BLOCKED** |
| (next) | domain ceiling + source ceiling + cross-stage carry | pass | **5 solved · 0 valid · avg 1.000 — BLOCKED** |
| `3c898a6` | **per-stage settlement day** | 1 solved · 1 valid *on the new crux* | never ran (qc_gate B1) |
| `d8aae8e` | licence terms + lifted notices | 1 solved · 0 valid · **1 in-progress timeout** — BLOCKED | never ran |
| `2b131ee` | **shipped I/O module** + authored-on rule | 0 solved · 1 valid · 1 timeout — PASS | **1 solved · 4 good valid · 0 timeouts · avg 0.200 — PASS** |

## The two findings that actually moved the needle

**1. Stated rules are transcription; a dimension the instance is constant in is
not.** Adding three fully-stated subsystems (a per-stage domain ceiling, a
per-source ceiling, a carry across domains and stages) took pass@5 from
**4/5 → 5/5 solved**. The trial analysis said it outright: *"the specification is
unambiguous enough that the implementation is effectively determined by the spec
once read correctly."* What worked instead was making sections 4–8 settle **as of
a day**, with every stage carrying its own `stage_on`: licences have terms and can
lapse and be re-granted, notices have `lifted_on`, so the refusals, the removal
closure, the lineage graph, the strains, the anchors and the cluster election are
all functions of the day and move in **both directions**. The shipped blend
settles every stage on `compiled_on`, so one global settlement is right there and
wrong for every stage of every other blend. `stage_reads_its_own_day` measured
BLIND on the shipped blend and wrong on **21 of 21** protected blends. This is the
SQL-playbook "dated outages" shape ported, and it is the only thing that produced
valid fails here.

**2. An in-progress timeout is a plumbing problem, and the fix is measurable.**
Head `d8aae8e` lost its only valid failure to the clock: the agent had a real
`held_back` bug, localised it at step 26, broke its own file patching it at step
28, recovered at 29, and re-ran **53 s** before the 3600 s override fired. Fix was
**not** difficulty and **not** `[agent].timeout_sec` (pass@2 pins its own 3600 s
override regardless): ship `/app/skeinio.py`, a read-only module that reads the
blend directory and writes the four tables and the report in the exact shape, so
no parsing, spelling or digesting is the solver's problem. Next head: **0
in-progress timeouts and 4 counted valid fails.** Generate it at freeze time out
of the reference's own fenced "portable region" so the two cannot drift, pin its
digest, and have the rig stage its **own** copy beside the handed-in program so
editing the image copy buys nothing.

## What drew the four valid fails — the most reusable list

Stratified, no shared root cause:

1. **§5 severance fixed point** — `status[pid]` read before the `pid not in
   samples_by_id` guard → `KeyError: 's9001'` on every held blend that names a
   parent the corpus does not hold. The shipped blend has no dangling parent, so
   the path never runs there. One line; crash → full pass.
2. **§9–10 apportionment, broadly wrong** — leftover tie-break, multi-round
   ceiling-freeze pool re-adjustment, carry-across-stage initialisation and
   source-ceiling capping all wrong at once; 16 of 42 tests over 10 held blends.
3. **near-miss** — `blend.tsv` on `held-sparse` only; a spill/carry/source-ceiling
   edge invisible on the shipped blend. 40 of 42 passed.
4. **near-miss** — `verdicts_moved` **+4** on `held-wide`, triggered only by
   heterogeneous `stage_on` dates. 40 of 42 passed.

Sections 9–10 are implicated in three of four. `difficulty_crux` PASS on all four;
`task_specification`, `approach_validity`, `reward_hacking` PASS on all five.

## Hurdles, per gate, in the order they blocked

1. **pass@2 "task/verifier problem" (both trials).** §2 of the contract still
   *guaranteed* parents appear earlier in corpus order after I had made the
   fixtures arbitrary. Both agents implemented §2 literally and crashed.
   `difficulty_crux` PASS but `approach_validity` FAIL — the graders read this
   correctly as my bug. Fix: drop the guarantee **without** saying "topologically
   sort", and plant a child-before-parent pair in the shipped blend so the
   requirement is discoverable from the agent's own data.
2. **pass@5 too easy, twice** (4/5 then 5/5). See finding 1.
3. **qc_gate B1, early-exit with 20 checks deferred.** `verdicts_moved` was
   defined over a sample's *verdict*, but §11 fixes `verdict` as exactly
   `admit`/`refuse` while the reference compared the *cause*. Two defensible
   answers. Any counter defined over a term the spec formally defines elsewhere
   must say which reading it means.
4. **pass@2 in-progress timeout.** See finding 2.
5. cosine, static review, duplicate, validation, AVA, deep_review, tier1:
   **never blocked, on any push.** Cosine passed 5/5 with no reskin — an in-flight
   PR head is not in the corpus.

## Levers measured NOT to work here

- **More stated rules.** Three whole subsystems → pass@5 got *easier* (4/5 → 5/5).
- **Folding the drift cap into the removal closure.** Looked like a deep mutual
  fixed point; measured **inert** — strain is monotone along edges, so
  `{strain > cap}` is already closed downward and removing those nodes changes
  nothing for survivors except one `depth` in two blends. Dropped before pushing;
  it would have been a QC C3 hole. *Measure a "closure" before shipping it.*
- **Raising `[agent].timeout_sec`** to cure a pass@2 timeout — pass@2 pins 3600 s
  whatever `task.toml` says.

## Operational notes specific to this build

- **Engineered edge witnesses are the last thing you pin.** The exact landings
  (`size == spare`, `drawn + size == room`, a term opening exactly on a stage day)
  are measure-zero and every forge change reshuffles them. I re-ran the seed
  search four times. Do the forge first, freeze it, *then* search seeds.
- **Guarantee a tie-break is decisive by construction, not by luck.** The
  strain tie-break stayed thin until the builder made one member a seed and the
  other two drifts away *from that member*, with the lighter one given the later
  authoring day.
- Verifier suite ~15–25 s in-container for 42 tests incl. 130 mutation probes over
  7 sweep blends; `[verifier].timeout_sec = 1800` is ample.
- `[agent].timeout_sec = 5400`; pass@5 trials ran 30–58 min with the plumbing in.
