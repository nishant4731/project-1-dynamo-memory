---
name: dynamo-regulated-knowledge-medical-and-clinical-workflows-playbook
description: "PLAYBOOK Regulated Knowledge Work / Medical and Clinical Workflows — ALL-GREEN ward-attribution mold; the converting crux is a stated quantity whose obvious algorithm is infeasible at the graded scale."
metadata:
  type: project
---

**Category:** Regulated Knowledge Work and Business Operations · **Subcategory:** Medical
and Clinical Workflows
**Repo:** `handshake-project-dynamo/dynamo-a8b2707-...` · PR #1 · **`ecd61e8` ALL-GREEN**
(2026-08-23). Eleven heads. Sibling in the same category: `dynamo-e2765c3`
(`covenant-margin`, Finance) — different subcategory, and its allocation mold was
deliberately *not* reused.

## The mold

`dynamo/sentinel-trace`: a read-only ward surveillance pack at `/app/sentinel_pack`
(bays, bitemporal stay + screen records, calibration probes) and a complete protocol at
`/app/SENTINEL_PROTOCOL.md`. The agent writes `/app/sentinel_trace.py PACK CASE LINE
REVIEW CUT` and emits four SHA-256-chained byte-graded reports. Attribution is a least
fixed point over patient carriage `(day, grade)` states.

## Measured

| gate | accepted head `ecd61e8` |
|---|---|
| pass@2 | **0 solved · 2 valid-fail · 0 timeouts** |
| pass@5 | **1 solved · 3 good-valid · 1 in-progress-timeout · avg@5 0.200** |
| cosine | passed all 11 heads, ~0.65–0.71 instruction / 0.68–0.72 verifier |
| review / similarity / validation | green every head |
| deep_review / ava / tier1 / qc_eval / qc_exec | green from the first head that reached them |
| qc_gate | green except one C3 (below) |

## What converted — the only lever that worked

**A quantity cheap to state and expensive to compute.** `minimum_cut`: the fewest admitted
contacts whose *joint* refusal averts a case — a minimum edge cut between the seed states
and that case's states. It adds no rule, so QC B5 stays green, but enumeration cannot
reach it. Plus `least_cut`, the lexicographically least such set, which one max-flow run
does **not** give (a residual-graph cut is *a* min cut, rarely the least).

The analyser on the accepted head: *"Across all four failing trials the minimum-cut
computation is the pivot point — either wrong, too slow, or partially fixed but not
complete."* And on the blindness: *"The shipped pack has all single-contact cuts (depth
≤ 1), so the flaw is invisible there — both agents produced byte-exact shipped-pack output
and passed 6 of 7 tests."*

**Scale that made it bite:** 41–55 admitted contacts, deepest cut **5**, 6–11 of 34
attributed patients needing a joint cut, out of contacts that are *not* individually
critical. Shipped pack: 4 contacts, every cut depth 1. Reference settles a pack in 0.5 s;
depth-5 enumeration is ~3.5 M combinations against a 150 s per-pack budget.

## Levers measured NOT to work (do not re-run these)

| lever | draws | result |
|---|---|---|
| more stated computation, however intricate | 3 heads / 6 trials | all solved, `difficulty_crux` NA every time |
| operational irreversibility (destructive fold, spent intake) | 1 head / 2 trials | both solved; agents validate before touching the live copy |
| raising `[agent].timeout_sec` 3600 → 5400 | 1 head | pass@5 **3/5 → 4/5**; `low_timeout` FAILed on a *passing* trial. Extra clock buys solves, not merit failures. Reverted. |
| volume for its own sake | — | the intake fold was 99 of 700 deliverable lines and produced 1 failure in ~14 trials vs the cut machinery's 5; cutting it is what let agents finish and fail on merit |

## Two traps that cost heads

1. **A mutation sweep can be green while a rule is inert.** The crowding cap was placed
   only where the cap was not binding, so mutants that reduced *more* fired while deleting
   the rule outright changed nothing. Always test the **delete-the-rule** direction. See
   [[dynamo-mutation-sweep-green-on-an-inert-rule]].
2. **QC C3 builds its own packs, so it finds precedence holes yours cannot.** It mutated
   `crowded_acquisitions` from `elif` to `if` and constructed a pack where a contact was
   *both* horizon-clipped and landing in an over-crowded bay — a combination my graded
   packs never contained. An `A else B` precedence needs a case satisfying **both**, not
   one case of each.

## Operational

- `[verifier] timeout_sec = 2700` (suite ~100 s locally), `[agent] timeout_sec = 3600`.
  pass@2 pins 3600 regardless of `task.toml`, so "raise the timeout" advice cannot fix a
  pass@2 blocked on an in-progress timeout — only cutting volume can.
- Turn a submission's own timeout into an `AssertionError` ("did not finish within Ns"),
  not a bare `subprocess.TimeoutExpired`, so a brute-forcer counts as a merit failure.
- A verifier test that checks the protocol document against the emitted reports **in both
  directions** catches spec/reference drift; one rubric FAIL here came from trimming two
  report keys without the matching spec edit landing.
- Probe discipline: a probe that *passes* may be testing a correct variant. My first
  min-cut-restriction probe used `flow == width - 1`, which is a correct pool.
- Run isolation probes against a **baked** `/tests`; `chmod` on a macOS bind mount is a
  no-op and will report a false all-clear.
