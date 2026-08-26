---
name: dynamo-blind-sample-branch
description: Put the decisive code branch in a path the shipped sample never enters — it produced 0/5 with 5 valid fails on crosstalk-bench.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 153881bd-5cd7-4300-b32c-84cc025d70b7
  modified: 2026-08-13T00:27:29.457Z
---

The single highest-yield difficulty lever measured so far: choose the visible
pack so it never exercises the hardest branch, and witness that branch only in
held-out fixtures. On `dynamo-44fbd85` (`dynamo/crosstalk-bench`) every rig in
the shipped pack was full-rank, so the integer-kernel Hermite-normal-form path
was dead code during the agent's own testing. All five pass@5 agents wrote a
superficially plausible but subtly wrong HNF, passed their self-checks, and
failed on the held-out singular rigs — 0/5 solved, 5 good-valid fails,
avg@5 0.000, `difficulty_crux` PASS on every trial.

**Why:** frontier models self-verify aggressively. A rule they can exercise
locally gets debugged away; a rule whose correctness their sample cannot observe
gets committed to with confidence. Grading exactly and differentially on
held-out instances turns that confidence into a clean reward-0 wrong answer
rather than a timeout, which is what the pass@5 fail taxonomy wants.

**How to apply:** pick a branch that is genuinely load-bearing and fully
disclosed in the contract, then build the shipped fixture so the branch is
never entered (empty kernel, no ties, no boundary hit). Witness it in several
held-out packs instead, and keep a mutation anchor for it so the sweep proves
the verifier actually catches it. Do not hide the *rule* — only starve the
*sample*. Related: [[dynamo-inline-worked-examples]],
[[dynamo-mutation-sweep-finds-witness-holes]].

**Necessary refinement, measured 2026-08-13 on `dynamo-9b8a04d` (cost one pass@2
cycle).** Starving the sample only buys failures when the starved branch is an
algorithm that is *hard to write correctly blind*. I shipped six starved
branches — SCC condensation of dependency cycles, capacity-bound list
scheduling, a once-each dependant span over diamonds, ceil-vs-floor, clamp
counters, an inclusive size limit — and pass@2 came back **2/2 solved in 14 and
39 minutes of 60**. The trial analysis named the reason: every one of those is a
standard CS pattern with strong training-data familiarity, so the agent writes it
right the first time and never needs the sample to check it. Only the span
traversal *direction* cost either agent any debugging.

Contrast crosstalk-bench, where the starved branch was an integer-kernel Hermite
normal form: no retrievable one-shot implementation, so all five agents wrote
something plausible and wrong. **Test before building: can the reference pair
write this branch correctly with no way to run it?** If the branch is Tarjan, a
greedy scan, a dedup set, or a min/max clamp, the honest answer is yes and the
starve buys nothing. Reach instead for a policy that is genuinely unwritten and
must be induced from labelled evidence — see
[[dynamo-recovered-constants-are-still-transcription]] for the boundary: the
inference is only real when the *recovery procedure* is also unstated.

**Third confirmation, same day, `dynamo-d44c669` (Security/Cryptography).** Fourteen
starved branches — Tonelli–Shanks for the one domain with `p ≡ 1 mod 8`, DER
minimal-integer and long-form-length rejections, ledger-wide two-pass custody,
inclusive expiry boundary, off-curve and over-prime abscissas, torn tails, ladder
precedence — measured **2/2 solved in ~10 minutes of 60**, with the trial analysis
reporting `approach_validity` PASS and "no divergence from the golden approach". A
blindness table taken before that push had shown 21 of 22 wrong readings byte-identical
on the shipped batch, so the *starve* was real; what was missing is that none of those
branches is hard to write blind. Every one is either a textbook routine or a single
`<=`.

The remedy tried next, and worth watching: a rule whose answer is a property of a *set*
rather than of any frame — bar frames that withdraw a module's authority, where bars
apply to bars, so they must be settled in timestamp order (ties by position) before
anything else resolves, and a bar late in the stream can carry an early timestamp that
retroactively unseats an earlier one. There is no retrievable one-shot implementation of
a bespoke ordered settlement, and a single pass over the stream is the natural wrong
answer. Blindness re-measured at 25 of 27, ten of them in that subsystem.
