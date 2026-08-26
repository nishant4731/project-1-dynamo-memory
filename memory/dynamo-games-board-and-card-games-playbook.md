---
name: dynamo-games-board-and-card-games-playbook
description: "PLAYBOOK Games Puzzles and Interactive Simulation / Board and card games — ALL-GREEN season-reckoning mold; pass@2 1 valid fail, pass@5 2 solved / 3 good valid / avg 0.400; sampling-point counters are what broke the 2/2 ceiling."
metadata: 
  node_type: memory
  type: project
  originSessionId: ba6dfb5e-21d8-43c1-ba79-474bdb48c8f7
  modified: 2026-08-22T20:17:22.336Z
---

**Category:** Games Puzzles and Interactive Simulation · **Subcategory:** Board and card games
**Repo:** `handshake-project-dynamo/dynamo-c31fb12-games-puzzles-and-interactive-simulation` ·
PR #1 · heads `a842176` → `eca02ee` → **`8b592c3` ALL-GREEN** (2026-08-23).

Two delivered tasks already sat in this subcategory — `dynamo/veilbound-policy`
(a hidden-world policy optimiser) and `dynamo/calibrate-cairns` (engine-constant
recovery plus a solver). Both are *optimise/recover* molds. The repair-in-place
mold is a third shape here and cleared cosine comfortably on push 1.

## The mold

**Repair-in-place with a complete contract.** `dynamo/trumpline-reckon`: a card
league's season reckoning died mid-fold; the agent writes
`/app/trumpline_reckon.py`, which sifts packed `sheets/` and an unapplied
`pending/` against six ordered refusal causes, applies what stood in posting
order, fuses the hands two scorers wrote down twice on a four-part key, re-takes
the sigils, repacks under a record bound **and** a byte bound with a per-sheet
byte-offset index, reckons `PLACINGS.tsv`, files refusals with collision
ordinals, spends the pending and scratch trees, and writes 39 counters.
`TRUMPLINE_CODEX.md` states all of it in twelve sections — which is what keeps
QC B5 green.

**The crux is the standings, starved by the shape of the shipped circuit.**
Three columns: `crown` (distinct entrants a *run* reaches, where a run chains
loser→winner across hands, each dealt strictly after the one before settled and
carrying a strictly greater stake — so the search state is the **hand**, not the
player); `hold` (longest unbroken winning run at **one** table); and
`place`/`depth`/`lock` from reckoning a knot of equal-points entrants apart
**recursively**, restricting each level to the group it is separating until a
group locks. The shipped circuit gives every entrant exactly one table, deals in
bands so stake and clock rise together along any chain, and knots nothing deeper
than one reckoning.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `eca02ee` | **2 solved · 0 valid-fail — BLOCKED, "too easy"** | never ran |
| `8b592c3` | **0 solved · 1 valid-fail · 1 in-progress-timeout** — "Rerun Recommended: NO" | **2 solved · 3 good-valid · 0 soft-timeout · 0 task-issue · avg@5 0.400 — PASS** |

- Cosine passed all three pushes: instruction **0.651**, verifier **0.825**,
  fingerprint **0.786** (threshold 0.9). Push 2 left *both* compared facets
  byte-identical and still passed — a third confirmation that in-flight PR heads
  are not in the corpus ([[dynamo-inflight-heads-not-indexed]]).
- **qc_eval + qc_exec + qc_gate clean on the first push that reached them**, 37
  checks, empty `QC-FIXES-B64:W10=`. AVA PASS with no blocking items.
  deep_review PASS, "Blocking Issues: None". tier1 PASS. Dynamo eval PASS.
  Duplicate check UNIQUE.
- Blindness table on `8b592c3`: **15 of 40** plausible readings byte-identical on
  the shipped circuit and wrong on **2 to 19 of 19** protected ones.
- Mutation sweep: **172 probes, 0 anchor misses, 0 survivors, none caught by a
  single circuit**, no-op control green. Verifier suite ~20–170 s in-container
  (the spread is Docker contention from other sessions, not the suite).

## What broke the 2/2 ceiling — the single most reusable fact

`eca02ee` solved 2/2 in 41 min and ~60 min of the 60-min cap, with
`task_specification` and `approach_validity` PASS 2/2 and the analyser writing
*"independent convergence on all implementation details — especially the
non-obvious hand-state BFS and per-table hold — suggests deep codex
comprehension or training-data familiarity."* All three cruxes were resolved by
both agents. The advisory `pass2_suggestion` asked to make the cruxes
**inferential**; that was **rejected** — see the gate tension below.

What worked was [[dynamo-sampling-point-counters-beat-the-ceiling]], now
confirmed a **third** time: split the report from 33 counters to 39, six of them
one line each and sampled where their neighbours are not. Two of them are the
cruxes *counted* rather than tabulated, and both are degenerate on the shipped
circuit and only there:

- `lanes_scanned` — entrant-and-table pairs. Equals `entrants_placed` exactly
  when nobody moves tables (16 = 16 shipped; 61–70 vs 30–35 held out).
- `knots_reckoned` — groups reckoned apart **at every depth**. Equals
  `knots_formed` exactly when every knot settles in one reckoning (2 = 2 shipped;
  9–11 vs 4–7 held out).

Four more (`knots_formed`, `knots_locked`, `stake_lifted`, `records_touched`)
sample the recursion, the fusion and the apply pass. Cost to the agent: six
lines. That, plus a second planted knot reaching depth three and raised coverage
floors, took pass@2 from 2 solved / 0 valid to 0 solved / 1 valid.

## Which crux actually drew the valid fails

The three pass@5 failures were **stratified** — the analyser's own word — with
`task_specification` and `approach_validity` PASS on all five trials:

1. **Operational** (`task__R9PWbtF`, `difficulty_crux` FAIL): ran an incomplete
   draft on the live circuit at step 9, consuming `pending/` and `scratch/` and
   crashing mid-run on a crown `TypeError`. *"The finished script is
   algorithmically correct — it passes all 12 held circuits and the fresh-crash
   test — but the live circuit state was destroyed by the premature run."*
   Irreversibility fired here as a **graded** failure, not a timeout.
2. **The intended crux** (`task__bQGvPN6`, `difficulty_crux` PASS): a structurally
   correct tool whose `HANDS.tsv` differed by **5 bytes across 59 records on
   every circuit** — one wrong codex rule in fusion field selection, marks-union
   ordering or pending tie-breaking, invisible to its own `/tmp` testing.
   `bytes_written` 13001 vs 12996.
3. **A reading convention** (`task__CXKfNqj`, `difficulty_crux` FAIL): stored the
   refusal `text` with a trailing `\n` (readline-style) where the reference
   splits on `"\n"`. Wrong on every refusal file in every circuit. The format
   sheet in §12 does disclose it (the quoted line ends at `}`).

**Note what this says:** only one of three landed on the algorithmic crux. The
byte-level reading conventions and the operational one-shot discipline carried
the other two. Keep all three surfaces.

## Hurdles, per gate, in the order they blocked

1. **static (`review / review`), push 1.** `[metadata].artifact_type` value
   `report_or_summary` is not in the closed set — the taxonomy in
   `references/diversity-taxonomy.toml` calls it `document_or_report`. One line,
   but it **skips every downstream gate**, so it costs a whole cycle. Read the
   two closed lists before writing them.
2. **pass@2, push 2.** 2 solved / 0 valid-fail. Fixed by the counter split above.
3. Cosine, changes, ratelimit, similarity, validation, ava_review, deep_review,
   tier1, qc_eval, qc_exec, qc_gate, trials: **never blocked, on any push**.

## Levers measured NOT to work here

- **Stating the crux and relying on shape alone.** Head 2 had every rule stated
  and eleven natural misreadings byte-identical on the shipped circuit; both
  agents got all three right anyway. Confirms
  [[dynamo-stated-algorithms-are-transcription-too]] — a shape starve is
  necessary but on its own it does not convert a frontier agent that reads the
  spec properly.
- **Making the cruxes inferential** (the advisory suggestion). Not tried, and
  deliberately: [[dynamo-b5-vs-pass2-determinability-pincer]] measured both ends
  of the disclosure axis solving 2/2, and anything genuinely underdetermined
  draws a QC **B5 Major**. Rejecting it cost nothing and qc_gate came back with
  an empty fix list.
- **Adding volume.** Never tried — one head-2 trial used the whole 60-minute cap,
  so more work would have converted it into an in-progress timeout, which counts
  for nothing ([[dynamo-timeouts-anchor-nothing]]).
- **Shipping a restorable spare archive** ([[dynamo-irreversibility-costs-the-clock]]).
  Prepared and fully validated (seven abuse routes graded: restore-and-stop 0,
  reckon-then-restore-over-it 0, unpack-inside-the-graded-dir 0,
  leave-a-copy-there 0, reckon-a-copy-only 0, restore-twice-then-reckon 1,
  delete-the-spare-after 1) and then **not pushed**, because head 2's taxonomy
  showed 0 timeouts. It would only have made the task easier — and head 3's
  irreversibility failure was a *graded* one. Read the taxonomy before applying
  that fix; it is for the timeout signature, not for irreversibility as such.

## Gate tensions seen here

The B5-vs-pass@2 pincer is the whole story in this subcategory too, and the
resolution is the vulnerability-analysis one: **state everything, and put the
difficulty in the shape of the shipped instance** — then, when that alone solves
2/2, add counters that are *free to compute and expensive to sample correctly*
rather than rules to transcribe or disclosure to withdraw. The counters do not
weaken B5 (each is defined precisely in the §10 table) and they double the
grading surface of the cruxes that the shape starve already hides.

One deep_review advisory worth carrying: sheet names and the refusal
stem/ordinal naming live in the codex rather than `instruction.md`. Non-blocking
because the codex is agent-visible, referenced and declared normative — but it
"sits just inside" the name-the-filenames-in-the-instruction guidance.

## Operational notes

- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1800`. AVA flagged that
  pass@2 ran under a **3600 s override** while the task declares 5400, which is
  what produced head 3's one in-progress timeout on a ~400–600 line
  implementation — [[dynamo-pass2-overrides-the-agent-timeout]] again.
- Two generator lessons from building the corpus are separate memories:
  [[dynamo-plant-the-deep-knot-do-not-search-for-it]] and
  [[dynamo-search-the-fixture-for-its-own-edge-witness]].
- `ctrf.json` was absent in all five pass@5 trials; the analyser fell back to
  `verifier/test-stdout.txt`. It did not affect the verdict.
