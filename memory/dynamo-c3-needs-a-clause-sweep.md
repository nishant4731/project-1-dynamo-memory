---
name: dynamo-c3-needs-a-clause-sweep
description: "QC C3-exec reported one unwitnessed clause; a sweep weakening every admission condition found 18 across three families — masked, redundant, and simply missing."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-13T04:54:51.243Z
---

On `dynamo-56ae913`, `qc_exec` blocked with C3-exec: it dropped the §3.2 rule refusing a
docket row with a negative `attempt`, and **all 26 tests still scored reward 1.0**. Patching
that one clause would have shipped the same failure again next cycle.

Instead, sweep it. For each boolean sub-condition in the reference solution's admission
chains, weaken it, re-run against every graded job, and check whether *any* output byte
moves. That found **18 unwitnessed clauses**, in three kinds that each need a different fix:

1. **Missing fixture** (13) — no graded record exercises the clause. Plant one.
2. **Provably unreachable** (2) — the clause can never be the deciding cause, so no fixture
   can exist. A leading `/` always yields an empty first segment, so the empty-segment rule
   already refuses it; a digest binding model *and* judge means two free slots can never both
   match. Delete the distinction from code **and** the spec sentence claiming it. Do not
   invent a witness.
3. **Masked** (6) — the nastiest. A fixture existed, but when the clause was weakened the
   record was refused a step later anyway, so the bytes were identical. Every malformed
   stray registered the *healthy* slot's digest, so dropping a validity check just moved the
   refusal to the digest match. Fix: build the fixture so it **would succeed** if the clause
   under test were the only thing stopping it. Same trap internally — corrupting a chit's
   magic byte also broke its parity byte, so the parity rule hid the magic rule.

**Why:** C3 asks whether the verifier's coverage is narrow enough to hardcode past. A clause
with no witness is a rule the grader does not actually grade, and QC mutates the *solution*
to find it — so mirror that: mutate the reference and diff the artifacts.

**How to apply:** when C3-exec names one clause, treat it as a sample, not the finding. Run
the sweep over all three admission families before pushing, and re-check each mutant per
seed. See [[dynamo-c3-is-a-clause-family]] and
[[dynamo-witness-must-be-the-selected-value]] — masking is the same failure in both: the
witness exists but nothing downstream lets it change the output.
