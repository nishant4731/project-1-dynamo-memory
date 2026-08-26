---
name: dynamo-data-science-and-reporting-data-visualization-playbook
description: "PLAYBOOK Data Science and Reporting / Data visualization — ALL-GREEN and accepted; pass@5 1 solved/4 good valid, avg 0.200. The lever was a stated OPTIMUM greedy gets wrong, plus bounding a wedged submission."
metadata:
  node_type: memory
  type: project
---

**Category:** Data Science and Reporting · **Subcategory:** Data visualization
**Repo:** `handshake-project-dynamo/dynamo-d8a8539-data-science-and-reporting`
· PR #1 · head **`a5dc643`** · **ALL-GREEN, label `accepted`** (2026-08-24).
pass@2 pass, pass@5 **1 solved / 4 good-valid-fail / 0 timeouts, avg@5 0.200**.
Took **13 heads**; heads 1-9 all died on pass@2 "too easy".

## The mold

Rebuild a byte-exact chart renderer from its house standard.
`dynamo/particulate-board`: sift a day of monitor readings against six ordered
causes, reduce to per-bin medians, scale per band off a 1/2/5/25 ladder, thin to
a fixed point, place label callouts, emit `board.svg` + `ladder.tsv` +
`callouts.tsv` + a 38-counter manifest. Twelve sections, complete — which keeps
QC **B5** green throughout.

## What did NOT work (9 heads, all measured 2/2 solved)

**Adding stated rules never adds difficulty.** In order I added: a fixed-point
thinning crux; a band-raise closure (drop a label → raise the ladder, re-settle,
≤3); a margin subsystem (spill → reserve a column → narrow the plot → re-settle);
raises carrying across margin passes. Blindness grew 32/57 → 39/66 → 51/78 → 55/82
single-change misreadings invisible on the shipped board, and **pass@2 did not move
once**. Agents read the standard end to end and implement whatever it says.
See [[dynamo-feedback-edges-not-clauses]] — that entry's optimism was wrong;
feedback edges got transcribed too.

Also measured not to work: withholding the anchor order (searched real boards —
**zero** strips pin it uniquely, so it would be QC B5, not difficulty);
withholding the label metric alone (two linear equations, solved in minutes).

## What DID work: state an OPTIMUM, not an algorithm

Replace greedy first-fit placement with: *the strip takes the allowed placement
that labels the **most** candidates; among those, the one first in bin order with
anchors ranked above<below<right<left<none.* Fully determined (B5-safe), but the
natural implementation is wrong.

- greedy differs from the optimum on **26 of 29** networks
- the **shipped estate is one of the 3 where they agree** — byte-identical
- conflicts reach only ±2 candidates, so an exact DP is ~0.26s

Every pass@5 failure was this. Agents reach for DFS backtracking; one wrote
`"n=12 definitely too slow... could fail for adversarial data"` at step 37 and
shipped it anyway **because the quiet home network has one candidate per strip.**

## The other half: a wedged submission must not be able to spend your budget

This is what converted the result. An exponential DFS **hung the verifier**:
per-run timeout was 300s × 32 graded runs, so one hang ate the whole 900s before
pytest wrote a line. A verifier that emits nothing is scored
**`infra/setup-timeout`** — your problem, not the submission's — and the trial
was thrown away despite being reward 0 with *every* rubric column PASS.

Fix: per-run timeout **30s** (reference draws the heaviest network in 0.26s), and
a `_WEDGED` latch that **refuses all remaining runs** once one wedges. The pass@5
analysis then reads "triggers the verifier's `_WEDGED` guard, cascading remaining
tests into instant failure" — i.e. a **good valid fail**. Same trial, opposite
classification. See [[dynamo-timeouts-anchor-nothing]].

## The oscillation trap, and how the band was found

Squeeze the hour → agents die on their own plumbing bugs → in-progress timeouts,
which count for nothing. Give the hour back → 2/2 solved. Do not tune volume
([[dynamo-volume-bound-tasks-oscillate]]). Escape by **handing over the plumbing**
and putting the difficulty in *correctness*: `board_intake.py` ships sections 1-4
(read, sift, suspects, fold) **and** `render_svg`. The tables and 38 counters stay
with the agent. Guard the withheld metric — the generator strips CHAR_W/BOX_PAD/
BOX_H/MARK_GAP/ROW_PITCH and refuses to write if any survive.

## Hurdles, gate by gate

1. **qc_gate B1/B5/C3** (head 2) — centring rule; grade the empty sheet.
2. **pass2 "too easy" ×9** — see above.
3. **review** ×2 — metadata drift. Growing the corpus invalidates every number in
   `task.toml`. Also: **`difficulty_explanation` forbids results-based framing** —
   no "agents did X on pass@5", no measured blindness tables. I carried that
   defect for many heads before it was caught.
4. **pass2 low_timeout** — declare `[agent].timeout_sec = 3600`, the value pass@2
   actually enforces. [[dynamo-declare-the-timeout-pass2-enforces]]
5. **Two infra flakes** (`AgentTimeoutError`, `VerifierTimeoutError`) — the sticky
   says so explicitly. `gh run rerun` 404s from a fork; **close/reopen the PR**.
6. **qc_gate C3** (head 12) — §11 said "leave anything already there alone" and
   nothing graded ever *put* anything there. Every graded run now starts with a
   planted file **and subdirectory**; probe renders start lived-in too.

## Traps I set for myself

- `open(p,"w").write(open(p).read()...)` **truncated BOARD_STANDARD.md to 0 bytes**
  and the oracle still scored **reward 1** — the only check was a hash against a
  pin regenerated from the damaged file. Verifier now checks the standard is whole.
- Shipped a helper module, then made importing it fatal: `python3 -I` implies `-P`
  and drops the script's directory from `sys.path`. Use **`-s -E`**.
- Wrote a regression probe for the variant that already worked (`sys.path` fixed)
  instead of the one that broke (bare import). It passed and proved nothing.
- A vacuous `all(... for ... in ())` made a uniqueness check green and useless.

## Numbers

31 graded networks, 23 in the probe sweep, 77 probes (0 survivors, none caught by
one network), suite 161s of a 900s budget, attack suite 16/16.
