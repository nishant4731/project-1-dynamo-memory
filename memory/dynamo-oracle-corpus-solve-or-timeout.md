---
name: dynamo-oracle-corpus-solve-or-timeout
description: "A worked-example corpus that fully verifies the deliverable makes pass@5 binary — agents either finish and solve, or time out; there is no valid-fail region."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-12T09:31:19.401Z
---

Measured on `dynamo-56ae913` (2026-08-12), across five pass@2 draws and one pass@5.

Design: undocumented scoring policy, recoverable from N "worked jobs" shipped with complete
inputs beside the exact artifacts a correct run emits. Fairness proved by replaying the whole
mutation table against the corpus (nothing undetermined).

**The trap: that corpus is a complete oracle.** An agent replays its candidate over the
worked jobs and iterates until byte-exact, so anyone who *finishes verifying is correct by
construction*. Outcomes collapse to two:

| corpus size | result |
|---|---|
| 10 jobs | 1 solved (~40 min), 1 in-progress timeout |
| 6 jobs  | 2 solved (34–46 min) |

Every knob (corpus size, how much of the pipeline is documented) only slides trials along the
solve↔timeout line. pass@5 needs ≥3 **valid** fails and in-progress timeouts do not count, so
this shape cannot reach the accepted band. Confirmed: 0/5 solved, avg@5 0.000, but only 1 of 5
countable — blocked as "not hard enough."

The oracle property cannot simply be removed: it is what makes an inferred-policy task fair,
and `qc_gate` B5 (Underdetermined / Hidden-Knowledge Mapping) demanded it twice — once for
the policy generally, once specifically for **tie-breaks**, which ties too rare to appear in
the corpus can never pin.

**How to apply:** for the pass@5 band, prefer the mold with *no* end-to-end oracle in the
environment — a fully documented spec whose difficulty is volume of exactly-graded rules, or
hidden parameters pinned by *narrow* evidence (calibration rows) rather than whole worked
jobs. Those produce finished-but-wrong runs, which is the only thing that counts as a valid
failure. See [[dynamo-pass2-typo-is-not-difficulty]] — the same repo's first commit, fully
documented with no corpus, produced exactly that: 1 solved / 1 valid fail.

Caveat measured in the same session: adding three interacting subsystems to the fully
documented version did **not** move solve time (17–18 min both times). More rules against a
complete spec buys typing, not thinking.

**Narrow calibration rows do not escape this either (measured 2026-08-13, `dynamo-d44c669`
head 3).** The prescription above — "hidden parameters pinned by *narrow* evidence
(calibration rows) rather than whole worked jobs" — was implemented as literally as
possible: a trust score whose constants appear nowhere in the contract, only the term
shapes (saturating cap, hinge, cap, clamp); 28 retired records publishing features and
the assigned score; each term isolated by a short sweep with the row past each boundary
appearing **exactly once**; and a verifier test enumerating every policy of the disclosed
shape that fits the rows, proving exactly one does. Two of the five features were outputs
of the agent's own audit, so a wrong settlement propagated into every score.

**Result: 2/2 solved.** The analyser: "Both agents parsed calibration.tsv to derive the
scoring formula coefficients rather than hardcoding guesses." One agent *did* initially
get the trust multiplier wrong — and caught it by re-checking against the corpus, listing
"trust penalty multiplier" among its five self-found patches.

**Why:** the collapse is not about corpus *size* or whether it covers whole jobs. It is
that **a corpus the agent can check a candidate against is an oracle**, full stop. 28 rows
are cheap to verify exhaustively, so anyone who finishes is correct by construction —
exactly the failure mode above, reached from the opposite direction. And the oracle
property cannot be dropped, because B5 requires the shipped data to pin the mechanism
uniquely; the verifier test that proves fairness is the same fact that guarantees
solvability.

**How to apply:** for an induced policy to produce valid fails, *verifying* a candidate
must itself be expensive or incomplete — a corpus too large to check by hand against a
hypothesis space too big to search, which is what the infer-release-gate family had.
A small, clean, provably-pinning corpus is a fair task and a solved one.
