---
name: dynamo-blindness-table-before-pushing
description: "Measure the shipped fixture's blindness by running N plausible-but-wrong variants of your own reference tool on it before pushing — it turns the difficulty claim into a number."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ebe61ea7-b950-4d2b-8e6f-3aa1f118f4a1
  modified: 2026-08-12T23:29:23.219Z
---

Before the first push, script a table: for each plausible wrong reading of the contract,
patch the reference tool with a one-line substitution, run it on the **shipped** fixture and
on every held-out fixture, and print `shipped: identical|DIFFERENT` next to `held-out wrong:
k of n`. Built for `dynamo-6bb0151` (`dynamo/tapline-recut`, Security / Network Forensics).

Measured there: **14 of 17 wrong variants left the shipped case byte-identical to the correct
answer while failing 9–12 of 12 held-out cases** — receiver-side profile swap, `last`-wins
everywhere, no modulus on sequence arithmetic, sums never checked, extension split at the
first dot, snapped record dropped, clock chain one hop only, offset order instead of
corrected-stamp order, reset not closing a leg, latest-open wins, no leading hole.

**Why:** it is the only pre-push evidence that the fixture is actually self-check-blind, and
it costs minutes. The variants double as the honest wording of `difficulty_explanation` and
the PR body, and the three variants the shipped case *does* catch tell you where the agent
still gets fair local signal. It is a different instrument from the mutation sweep: the sweep
mutates the **referee** and asks whether grading discriminates; this mutates the **submission**
and asks whether the agent's own testing could notice.

**How to apply:** run it as a scratch script (not in `tests/`), one entry per stated rule, and
assert the unpatched control is `identical / 0 of n`. If a variant is `DIFFERENT` on the
shipped fixture, either accept it as deliberate local signal or move the witness out of the
shipped fixture. See [[dynamo-blind-sample-branch]] for why the blind branch is the lever, and
[[dynamo-mutation-sweep-finds-witness-holes]] for the other half.

**Second measurement (`dynamo-137a569`, `dynamo/rollup-evalrun`, Model Training / Evaluation
Infrastructure, 2026-08-13).** Eight plausible wrong readings, all `visible: identical`, each
caught on 3-5 of 9 graded packs: float score rendering; a shard's highest retry index taken
over its survivors instead of all its records; orderings enumerated in input order rather than
sorted; a half-open window closed at the top; a partially-resolved group scored from what it
has; a missing value read as zero in a comparison count; zero-padding dropped on a value below
a tenth; collection order read from the input file. **8 of 8 blind** — a higher rate than the
14-of-17 above, because that fixture corpus was seed-searched with an explicit predicate
requiring the visible pack to score zero on every starved property while the held-out packs
witness each one at least twice. Searching the fixture for blindness beats checking it after.

Put the resulting table in the PR body verbatim: the Dynamo eval graded
`essential_difficulty` and `anti_cheat` PASS citing exactly those traps.

**Outcome for the first measurement (`dynamo-6bb0151`, 2026-08-13): ALL-GREEN, pass@5 2/5 solved
with 3 good-valid fails, avg@5 0.400** — inside the accepted band on the second commit. The
failures stratified into two root causes, exactly as the table predicted was possible: two
Terminus-2 heredoc wedges, and one genuine near-miss where the agent ran an unverified tool on
the irreplaceable live case, consumed the spool, then shipped a corrected tool that still
under-counted per-leg conflicts because the accumulator sat after the `continue` for refused
records. Every individually-tested clause passed for that agent; it lost on the one interaction
no local check could show it.
