---
name: dynamo-d44c669-attest-ledger
description: "dynamo-d44c669 (Security/Cryptography) — starved-sample task cleared cosine, static, Dynamo eval 31/31 and validation on the first push."
metadata: 
  node_type: memory
  type: project
  originSessionId: e718b780-7192-426b-b840-e8cfc51901c3
  modified: 2026-08-12T23:47:53.822Z
---

`dynamo/attest-ledger-audit` on `handshake-project-dynamo/dynamo-d44c669-security`
PR #1, commit `8371e8f`, pushed 2026-08-13. A reusable auditor for a binary
append-only attestation ledger: DER-like TLV grammar, three short-Weierstrass
domains, Schnorr verification, ledger-wide custody, an ordered eight-status
verdict ladder, twenty exact integer/digest report fields.

**Design = [[dynamo-blind-sample-branch]] applied deliberately.** The shipped
batch is clean, ordered and confined to the two domains whose prime is 3 mod 4,
so the general modular square root, every encoding rejection, out-of-order and
duplicated custody frames, the inclusive expiry boundary, off-curve and
over-prime abscissas, unknown frame types and the ladder's precedence are all
dead code while the agent self-tests. Measured with
[[dynamo-blindness-table-before-pushing]]: **21 of 22 plausible wrong readings
left the shipped batch byte-identical** and failed 1–8 of 8 held-out batches.

First-push gate results (no iteration needed on any of these): cosine
`0.734 / 0.812 / 0.835` against a 0.9 threshold; 25/25 static checks; **Dynamo
eval PASS on all 31 criteria, zero failures**, with `essential_difficulty` PASS
citing the starved-domain trap by name; similarity UNIQUE; validation green.
Local: oracle 1.0 (28/28, 143 s), nop 0.0, 58 mutation anchors with 0 survivors
and none caught by a single batch, plus probes for stub, replay-the-visible-answer,
symlinked output, a tool reading `/tests`, tampered inputs, and a planted
`conftest.py`/`pytest.ini`/PATH shim.

**How to apply:** the recipe that produced an all-green first push here was — pick
a coherent real format spec, write it out exhaustively so nothing is ambiguous,
then choose the *shipped sample* so it never enters the decisive branches, and
grade differentially on held-out plus a submission-salted batch. Volume of rules
is not the lever; blindness is.

## Second measurement: the authority ratchet did not move the failure rate

Head 2 (`f2833d6`) added module identity to every frame plus a BAR subsystem whose
settlement is a property of the *set* — bars settle in `barred_at` order, ties by
ledger position, and a bar whose own module is already barred is set aside, so a bar
late in the stream can carry an early timestamp that retroactively unseats an earlier
one. Void frames then cascade into custody (a void ANCHOR costs a device its
enrolment, a void REVOKE hands one back). Plus a third graded artifact and
before/after-cascade counters. Blindness re-measured at **25 of 27**.

**Result: 2/2 solved again**, 21 and 27 minutes of 60 (up from ~10). The analyser:
"No meaningful divergence between agent approaches and the golden approach in either
trial. The agents followed the same ordering of passes (bar settlement → custody →
verdict ladder)." Both independently used Jacobian coordinates and Tonelli–Shanks; one
proactively patched a `y = 0` parity edge case it was never shown.

So on one repo, in one day: 14 starved branches → 2/2 in 10 min; + a bespoke
order-dependent settlement → 2/2 in ~24 min. **The ratchet bought solve time at
roughly 2.4x and failure rate 0.** That is the third independent confirmation of
[[dynamo-spec-mold-caps-at-80pct-solve]] and [[dynamo-recovered-constants-are-still-transcription]]:
against a complete normative contract this reference pair does not fail, and the next
ratchet converts solvers into timeouts, which do not count. Everything else on the PR
was green at both heads — cosine, 25 static checks, Dynamo eval 31/31, similarity,
platform validation.

**How to apply:** stop ratcheting a fully-specified contract after the second 2/2 with
spare budget. The remaining shape with a track record is the reverse-engineering mold
(labelled corpus, undisclosed policy with an exact-integer non-linear component, graded
on held-out records) — a different task, not another subsystem.

## The rebuild cleared pass@2 — reconstruction beats specification

After three 2/2-solved heads, the task was rebuilt as a different concept:
`dynamo/escrow-release-gate` (commit `36dc230`). A key-escrow authority's decision log
survives; its policy does not. The notes give the request schema, the Feldman share
check, the ten reason codes, both file layouts and the *shape* of the assurance score —
one saturating term, two hinges, a floor-divided step, a two-condition bonus, a clamp —
and **no constant and no check order**. Twenty-five integers and a ten-rung precedence
order have to come out of 376 logged decisions that vary jointly rather than one factor
at a time.

**Result: pass@2 0/2 solved, 1 valid fail, 1 in-progress timeout — PASSED, proceeding to
pass@5.** Run time 1h07 for two trials, i.e. at least one used the whole 3600s budget.

The analyser's read is the important part: *"Both trials share the same root cause: the
agent committed fully to exhaustive data analysis before writing any implementation code,
then ran out of budget... Both trials independently stalled on the same two conditions
(`quorum_short`, `rate_limited`), which is a strong signal that these are genuinely the
hardest constants to recover — consistent with the task's stated crux. This is not a
specification or verifier problem."*

**Why it worked where three ratchets failed:** a specification is read once and typed; a
policy has to be *searched for*, and search is the one thing that consumes the budget
without converging. See [[dynamo-oracle-corpus-solve-or-timeout]] for the boundary — a
corpus is only a wall when it is large and jointly varying enough that verifying a
candidate presupposes having found one.

**The live risk:** one of the two failures was an in-progress timeout, which does not
count at pass@5. The band needs ≥3 countable fails of 5. If pass@5 returns mostly
timeouts, the documented fix is to *trim non-crux breadth* so agents finish the recovery
and commit to a wrong parameterization (an anchor), never to simplify the wall itself.
