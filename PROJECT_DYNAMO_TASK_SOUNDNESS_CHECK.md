# Project Dynamo Task Soundness Check

Source link:
- https://project-dynamo.learn.joinhandshake.com/pitfalls/qc-eval

Read status:
- 2026-07-23: the in-app browser blocked the Handshake/JoinHandshake page by policy.
- 2026-07-23: the same URL was opened and read successfully in the user's Chrome profile.

The guidance below combines the announcement text provided in the task thread with the additional content read from the official page.

## Summary

Project Dynamo now runs an automated Task Soundness quality gate on every task PR as soon as it is opened. The check reviews the task like a careful reviewer and also runs the task in a sandbox to try to break the verifier. It posts one PR comment listing what must be fixed.

Tasks that clear this automated gate can go straight to RTD with no human-review requirement, which makes this the fast path for payout.

## Severity Levels

- Major: blocking. Every Major item must be fixed before the task can be submitted.
- Minor: advisory. Worth fixing, but not blocking by itself.

The PR comment should contain a single "Must fix / resolve" list. Each item should identify the defect, file and line, what it means, what was found in the task, and a concrete fix.

## How The Gate Decides

The QC gate defaults to fail. It only reaches pass when every break attempt is refuted by evidence in the submitted task. Any single Major issue fails the whole task.

Important implications:

- "Near correct" is not enough.
- "Obscure edge case" is not a defense.
- "Intended difficulty" is not a defense for an underspecified or breakable task.
- Breadth matters as much as depth: one uncovered failure mode can block the PR.

The official page frames the gate as 30 Major checks across five families:

- A1-A6: solution and oracle correctness.
- B1-B6: contract coherence and determinacy.
- C1-C6: verifier rigor and scoring.
- D1-D5: fixtures, environment, and determinism.
- E1-E7: anti-cheat and isolation.

## Fastest Ways To Avoid A Block

- Compute expected answers from protected inputs, never from files the solver can edit.
- Seed all randomness.
- Document every assumption the solution relies on.
- Make the verifier reject symlinked outputs.
- Make the verifier reject empty outputs.
- Confirm the reference solution passes its own verifier.

## A. Reference Solution And Oracle

Major issues include:

- Oracle fails its own verifier: the reference solution does not pass the tests.
- Incomplete reference solution: the reference does not fully solve the task.
- Hardcoded answer: the reference bakes in the answer instead of computing it.
- Hidden or privileged access: the reference uses files or knowledge the solver cannot see.
- Undocumented assumption: the reference relies on behavior the task never states.
- Oracle edge-case or logic bug: the reference is wrong on some inputs.

## B. Instructions And Spec

Major issues include:

- Ambiguous rule: an instruction can be read more than one way and has no tie-break.
- Internal contradiction or impossible requirement: the spec contradicts itself or asks for something impossible.
- Missing definition, field, or data: the task references a term, field, or file it never defines or ships.
- Undocumented requirement enforced: tests enforce something missing from the instructions.
- Underdetermined mapping: the expected output cannot be worked out from the provided materials.
- Unstated data-anomaly or selection policy: a graded data quirk is not stated.

## C. Verifier Strength

Major issues include:

- Stub or degenerate output accepted: empty or trivial output scores full marks.
- Over-permissive tolerance: wrong answers pass because the threshold is too loose.
- Narrow or hardcodable coverage: graded cases are too few or too predictable.
- Truth recomputed from writable inputs: expected answers are computed from files the solver can edit.
- NaN or Infinity bypass: invalid numeric values slip through comparisons.
- Scoring contract mismatch: tests score differently than the instructions promise.

Minor issues include:

- Loose schema or extra content.
- Type-coercion bypass.
- Undisclosed normalization.
- Type-equality bypass.
- Default-only coverage.
- Untested advertised behavior.
- Correctness not statically confirmable.

## D. Determinism And Environment

Major issues include:

- Degenerate test fixture: shipped data allows a pass with no real work.
- Malformed or unparseable fixture: shipped files do not parse as expected.
- Environment build failure.
- Nondeterminism: graded data or accepted answers change run to run.
- Unseeded build-time randomness.

## E. Isolation And Anti-Cheating

Major issues include:

- Answers readable by the agent.
- Immutable-input integrity not enforced.
- Reward or harness plumbing exploit.
- Root or elevated access exposes secrets.
- Symlinked output path.
- Unsafe archive extraction.
- Non-self-contained or copied oracle.

## Practical Pre-Push Checklist

- Run the reference/oracle and verify it passes.
- Run nop or a deliberately bad output and verify it fails.
- Check that all expected values come from protected test fixtures or fixed constants, not solver-writable files.
- Check every verifier-enforced schema key, ordering rule, tie-break, tolerance, and normalization rule against `task/instruction.md`.
- Confirm randomness is seeded in generators, fixtures, and build-time data creation.
- Reject symlinked, missing, and empty artifacts before content checks.
- Search for leaked answers in agent-visible paths.
- Keep the automated PR comment focused: fix all Majors first, then decide whether Minors are worth addressing.

## Proven Strategies From The QC Guide

1. Put every graded decision in agent-visible material.
   - Covers common A3, A5, B3, and B4 failures.
   - Enumerate constants, thresholds, tie-breaks, ordering, precedence, units, and filters.
   - If a mechanism is meant to be inferred, say that explicitly and ship enough data to pin it uniquely.

2. Make the verifier enforce structure, not only an aggregate.
   - Covers C1 and C2 failures.
   - Assert exact count, shape, keys, ordering, and byte-level requirements where the spec promises them.
   - Try to construct a wrong-shape or degenerate answer that passes; if it does, tighten the verifier.

3. Protect ground truth in code, not by convention.
   - Covers C4, E1, E2, and E5 failures.
   - Grade from protected `/tests` data or fixed verifier constants.
   - Do not derive expected answers from agent-writable `/app/data`.
   - Guard symlinked outputs and avoid copying `solution/` or `tests/` into the agent image.

4. Make the whole pipeline deterministic.
   - Covers A1, D3, D4, and D5 failures.
   - Seed all RNGs with fixed constants.
   - Avoid time, network calls, mutable dependencies, and set/dict iteration-order dependence on graded paths.
   - Pin dependencies when exact output bytes or hashes matter.

5. Ship a complete reference that derives its own answer.
   - Covers A2, A4, and B5 failures.
   - The reference must perform every required action, not only report partial outputs.
   - It must derive answers from agent-visible inputs.
   - Private helpers are only acceptable when every value they supply is recoverable from the shipped corpus.

## Official Checklist Items

- All verifier rules are stated in `instruction.md` or derivable from `environment/`.
- Nothing graded lives only in `solution/` or `tests/`.
- Learned mechanisms are explicitly described as learned and pinned by shipped data.
- The verifier enforces structural requirements directly.
- Every path-valued report field has a disclosed frame such as manifest-relative, output-root-relative, input-root-relative, or absolute, and the verifier rejects the wrong frame explicitly.
- If a report field is intentionally relative, `instruction.md` avoids bare backticked relative path examples that static checks may treat as invalid output paths; use an absolute `/app/...` example and describe removing the output prefix.
- Wrong-shape and degenerate answers have been tested and fail.
- Cross-check artifacts, such as JSON reports plus TSV/NDJSON ledgers, are not just inventory files: add explicit tamper tests showing that missing or stale secondary views fail even when the copied payload bytes and main report look correct.
- Graded numeric fields reject `NaN` and `Infinity`.
- Reward behavior matches the stated grading contract.
- Ground truth comes from `/tests` or non-agent-writable inputs.
- Output paths reject symlinks.
- Protected inputs are hash-pinned where mutation risk matters.
- `solution/` and `tests/` are not copied into the agent image.
- Reference tools and oracles cannot be copied as the deliverable.
- Randomness is seeded, dependencies are pinned, and no time/network nondeterminism affects grading.
- The reference solution scores full reward exactly as shipped.
- The reference performs every action the instructions require.
- Data anomalies such as duplicates, ties, and malformed rows have stated and enforced handling rules.
