---
name: dynamo-starve-a-ranking-rule-with-graph-shape
description: "On dynamo-bf7c1a7 the shipped instance was built with no diamond subgraphs, so a path-summing reach implementation was byte-identical there and wrong on every held-out bench — ALL-GREEN on push 1, pass@5 2 solved / 3 good valid fails."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 54a73c4c-f09a-4819-8973-6862c5a2aca7
  modified: 2026-08-16T22:33:25.713Z
---

`dynamo-bf7c1a7` (`dynamo/dovetail-refit`, Debugging and Repair / Build Failure
repair, 2026-08-16). A hermetic build plant's bench is refitted after a pass
died mid-build; admission of rebuilds is ranked by **reach** — the number of
actions downstream of a candidate, counting itself.

**ALL-GREEN on the first substantive push.** pass@2 1 solved · 1 valid fail ·
0 task issues · 0 timeouts, `Rerun Recommended: NO`; pass@5 **2 solved · 3
good-valid-fail · 0 soft-timeout · 0 in-progress-timeout · avg@5 0.400**, and
every other check green (cosine 0.680/0.753/0.780, Dynamo eval 30 PASS + 1 N/A,
duplicate, validation, deep_review, AVA, tier1, qc_eval, qc_exec, qc_gate with
an empty `QC-FIXES-B64`).

The failing trials wrote

    count = 1 + sum(dfs(succ) for succ in dependents[aid])

which counts a shared descendant once per path instead of once. The analyser's
own diagnosis is the lesson: *"The mainline bench … apparently contains no
diamond subgraphs whose count matters to the ranking, so the bug was invisible
during the agent's own validation."* It passed all 16 live-bench structural
checks and lost all ten held-out benches plus the salted one. **Three of the
four failing trials across both gates hit this same reach bug independently** —
it is not a fluke of one draw, it is where frontier agents actually land.

The other two pass@5 failures show the rest of the surface is load-bearing
too: one wrote the computed digest for `deferred` rows where the contract says
`-`, and one captured the corrupt-file list at startup but ran the deletion
loop *after* writing rebuilt artifacts, deleting a just-written file whose
digest matched a formerly corrupt name. Both are ordering/precision slips in a
faithful reimplementation, which is the failure class
[[dynamo-uniqueness-proof-is-a-self-check-oracle]] predicts once no oracle
ships.

**The generalisable move: starve by graph *shape*, not by clause coverage.**
[[dynamo-withhold-an-algorithm-not-a-clause]] says make the wrong algorithm
byte-identical on the shipped sample. A ranking function over a DAG gives that
for free — a shipped instance whose contention never involves a converging
path makes unique-count and path-sum agree, and no amount of the agent's own
testing can separate them. Cheaper to build than a hand-planted trap and it
converts a solver, which [[dynamo-recovery-tasks-are-bimodal]] records that
merely-stated tie-breaks do not.

**Second starve on the same task, same principle:** the live bench's slot
budget is never binding, so the deferral cascade, the per-tool cap and the
retention of an unsettled action's recorded artifact are exercised only on
held-out benches. A local blindness table over 43 plausible misreadings
measured 8 as byte-identical on the live bench and caught on 8-9 of 10
held-out ones; the evidence rules (sealed-run ownership, artifact validation,
scratch adoption) were deliberately left firing on the live bench so they stay
fair and C3-witnessed.

**Build the blindness table before pushing** — see
[[dynamo-blindness-table-before-pushing]]. Running each variant as a program
over the whole corpus and printing BLIND/shows per variant is what found three
readings that were provably *equivalent* (reach over pending vs all
descendants; key-match vs digest-match; excluding seal rows from an
abandoned-run count) and would have shipped as inert clauses or unkillable
mutants.
