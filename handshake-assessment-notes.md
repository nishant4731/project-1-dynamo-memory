# Handshake AI Assessment Notes

Source form: https://ai.joinhandshake.com/fellow/forms/ef4b6267-5d97-4f82-be7b-146977b1fa17  
Guidelines page: https://project-dynamo.learn.joinhandshake.com/pitfalls  
Date reviewed: 2026-07-20

Note: I opened and reviewed the assessment in Chrome using the `utkarsha` Chrome profile. I filled the draft answers in the live form but did not click Submit.

Current status: the form page is left open in Chrome for manual review and submission. The optional feedback field is blank.

## Assessment Overview

The assessment is titled **Common Errors Assessment: Five Exhibits**. It asks the reviewer to inspect five flawed benchmark/task examples. Each exhibit has one multiple-choice question and one free-response question.

The core idea: all five tasks shipped and passed CI, but each still violates an important benchmark-review requirement. The assessment is testing whether the reviewer can identify the broken requirement and describe a competent fix.

## Five Review Dimensions

1. **Coherent and complete contract**
   - The instructions must define one internally consistent task.
   - No two rules should contradict each other on the shipped data.
   - Every required field, edge case, format, and method choice that affects grading must be specified.

2. **Correct reference solution**
   - The reference/oracle solution must implement the written instruction, not just produce a plausible answer.
   - If the verifier is built from the oracle, an oracle bug becomes bad ground truth.
   - Tie-breaking, ordering, schema, and edge cases need explicit checking.

3. **Sound and materially complete verifier**
   - The verifier must distinguish correct answers from plausible or degenerate wrong answers.
   - Surface checks such as row counts, types, or broad tolerances are not enough if a fake answer can pass.
   - The verifier should assert the actual promises in the spec.

4. **Protected and independent ground truth**
   - The answer key must not be readable, writable, aliasable, or influenceable by the agent.
   - The verifier must compare the submitted artifact to independent ground truth, not to something the agent can redirect.
   - Symlinks, mutable inputs, and agent-writable paths are important threat surfaces.

5. **Runnable, realistic benchmark task**
   - A correct solution should be able to pass reliably as packaged.
   - Difficulty should come from reasoning, not guessing undocumented oracle quirks.
   - If the reference is too rough or the method is under-specified, better solutions may be unfairly rejected.

## Guideline Takeaways

- Run the oracle and the no-op/trivial agent before submission:
  - `harbor run -p task --agent oracle` should score `reward 1.0`.
  - `harbor run -p task --agent nop` should score below `1.0`.
- Oracle failure usually points to instruction, reference-solution, or runnable-task issues.
- A trivial solution passing usually points to verifier or ground-truth-protection issues.
- Walk the real shipped data against the instructions. Hypothetical consistency is not enough.
- Pin methodology only when the choice changes the graded answer.
- Verify against the spec, not merely against the oracle output.
- Keep ground truth outside agent-writable areas and reject artifact tricks such as symlinks.

## Exhibit Notes

### Exhibit A: Last One In, Wins

Domain: software engineering / pathfinding.

The task requires deterministic tie-breaking for equal-length paths: when several shortest paths tie, the same canonical path should be returned every time. The reference code overwrites `best` on every valid tied path, so it keeps the last tied path rather than the first/canonical path. The checker repeats the same buggy logic, and the graded layouts do not contain real ties.

What a strong answer should discuss:

- The reference solution does not implement the stated tie-break rule.
- The verifier agreeing with the buggy reference does not make the result correct.
- The absence of a current grading failure is not evidence of safety; the missing tied case means the benchmark never exercised the requirement.
- A competent fix should correct the tie-break implementation and add at least one graded fixture with a real tie.

Primary review dimensions involved:

- Correct reference solution.
- Sound and materially complete verifier.

### Exhibit B: The VWAP That Cannot Be

Domain: finance / feature generation.

The task defines a daily volume-weighted average price and a distance-from-average feature. One rule says zero-volume days have undefined averages and should be blank. Another rule says blanks are allowed only in the first 120 warm-up rows. The provided data includes zero-volume days after row 120, so both rules cannot be satisfied at once.

What a strong answer should discuss:

- The written contract is internally contradictory on the actual shipped data.
- This is not primarily a code bug or checker bug; the spec gives mutually incompatible requirements.
- The right repair is to rewrite the blank-value rule so it accounts for zero-volume days, then align the reference and verifier with that clarified contract.
- The checker should also preserve relevant data assumptions such as row order when the meaning depends on temporal sequence.

Primary review dimension involved:

- Coherent and complete contract.

### Exhibit C: The Symlink That Grades Itself

Domain: security / hidden-answer artifact checking.

The expected answer file is absent during the agent run and appears only during grading. A fake solution creates a symlink from the submitted output path to the future ground-truth path. When grading opens the submitted file, it follows the symlink and compares the answer key to itself.

What a strong answer should discuss:

- The submitted artifact is not independent from the hidden ground truth.
- The fact that the symlink did not contain the secret during the run does not matter; it successfully redirects the verifier at grading time.
- The checker should reject symlinks and ensure the submitted path is a normal file in the expected location before reading it.
- Randomizing the answer path is weaker than validating artifact type and trust boundaries.

Primary review dimension involved:

- Protected and independent ground truth.

### Exhibit D: The Confidence Interval That Is Not

Domain: machine learning / statistical output verification.

The verifier checks that the submitted margin of error is within a broad band, that the estimate lies inside the reported interval, and that the interval includes or excludes zero consistently with significance. A fake result reports a plausible margin of error but an almost zero-width interval around the estimate. Because no assertion links interval width to margin of error, the fake result passes.

What a strong answer should discuss:

- The original verifier checked several local properties but missed the relationship between fields.
- Passing every existing check does not imply the result is trustworthy when the checks omit a material invariant.
- A competent fix should require nonzero interval width and require the interval width to be reasonably consistent with the reported margin of error.
- Exact equality to the reference is too brittle; the goal is to catch degenerate/fabricated ranges while still allowing legitimate numerical variation.

Primary review dimension involved:

- Sound and materially complete verifier.

### Exhibit E: Re-Entry Time Depends on Whose Ruler You Use

Domain: scientific computing / numerical simulation.

The instruction asks for a sufficiently accurate re-entry time, but does not define the integration method, step size, or how to locate the crossing moment between steps. The reference solution uses fixed one-second steps and reports the full step that first crosses the threshold. That rough reference can be more than the allowed half-second tolerance away from a more accurate method.

What a strong answer should discuss:

- This is not just a tolerance being too strict; the reference value itself is not reliable enough to define ground truth.
- Better numerical methods can fail because they disagree with the oracle's undocumented rough approximation.
- The task should specify the calculation method or the crossing convention only where needed, and the reference should be rebuilt with a more careful method.
- The allowed tolerance should reflect real numerical uncertainty, not the error introduced by the reference's crude stepping.

Primary review dimensions involved:

- Runnable, realistic benchmark task.
- Coherent and complete contract.
- Correct reference solution.

## Response Strategy

For each free-response answer, a solid structure is:

1. Name the broken requirement.
2. Explain the concrete failure mode in the exhibit.
3. Explain why passing CI or not yet affecting a grade does not make it safe.
4. State the minimal competent fix.

Keep answers process-focused rather than domain-trivia-focused. The assessment appears to reward recognizing benchmark construction failures: contradictory specs, buggy oracles, incomplete verifiers, compromised ground truth, and unrealistic/under-specified tasks.

## Draft Answers Filled In Chrome

These are the draft answers currently entered in the live form. Review and edit before submitting.

### Multiple Choice

1. **Q1: B** — Fix the code to keep the first tied path and add at least one graded tie case.
2. **Q3: C** — Rewrite the blank-value rule so it also allows blanks on zero-trading days, and check row order.
3. **Q5: B** — Verify the submitted file is a real file, not a shortcut/symlink, and lives in the expected folder.
4. **Q7: B** — Require non-zero interval width and consistency between interval width and reported margin of error.
5. **Q9: B** — Specify the numerical method/crossing rule and rebuild the reference with a more careful method.

### Free Responses

**Q2.** The reference solution implemented the tie-breaker incorrectly: it kept overwriting the best path and returned the last tied path instead of the first deterministic one required by the contract. The checker repeated the same buggy logic, and the graded cases had no real tie, so the broken behavior was invisible. "It has not caused a problem yet" is not safety; it only means the current tests do not exercise the promised behavior. The fix needs both corrected reference logic and at least one graded tie case.

**Q4.** The broken part is the task contract: it requires blanks only during the first 120 warm-up rows, but also requires blanks whenever a whole day has zero volume, including later rows. Because the requirements contradict each other on the given data, no implementation or checker can be correct until the instructions say one coherent rule. Once the contract is made consistent, the reference code and verifier can both enforce the same intended behavior.

**Q6.** The ground truth was not protected from the submitted artifact. A symlink at `/app/my_answer.json` could point to the future answer key path, so when grading later created `/tests/correct_answer.json` the checker compared the key to itself. The shortcut did not contain the secret during the work, but it still created a path that let the grading phase read protected truth as the submission. The checker must reject symlinks and ensure the submitted file is a real file in the expected location before comparing contents.

**Q8.** The original checks verified several surface properties independently but never checked the relationship between them. A submission could report a plausible margin of error while giving an essentially zero-width range, making the uncertainty dishonest even though each existing assertion passed. Passing incomplete checks only proves the answer fits the checker, not that it satisfies the task's real promise. The verifier needs to connect range width to the reported margin of error.

**Q10.** The failure is that the benchmark's ground truth is not trustworthy enough for the tolerance being enforced. The instructions leave the numerical method, step size, and crossing rule vague, while the reference uses coarse one-second steps and reports the first full step after crossing. A more accurate method can disagree with that rough reference by more than 0.5 seconds. This is not merely a strict tolerance problem; the expected answer itself is approximate and underspecified, so the contract and reference need to be rebuilt around a careful, explicit method.

## Quick Use Guide

Use this as a fast checklist while filling the form yourself.

### Exhibit A

Likely issue: the reference/oracle tie-breaking logic is wrong, and the verifier/data do not catch the tied-path case.

Core points to include:

- The spec requires deterministic canonical tie-breaking.
- The reference keeps the last tied path because it overwrites `best` on ties.
- A checker that repeats the same flawed logic is not independent evidence of correctness.
- Add tied fixtures, fix the tie-break, and make the verifier assert the written rule.

### Exhibit B

Likely issue: the written contract contradicts itself on shipped data.

Core points to include:

- Zero-volume days after the warm-up period require blank VWAP values.
- Another rule forbids blanks after the first 120 rows.
- No correct implementation can satisfy both conditions on the actual dataset.
- Clarify the blank-value rule, then update the reference and verifier accordingly.

### Exhibit C

Likely issue: the submitted artifact can alias hidden ground truth through a symlink.

Core points to include:

- The verifier reads the submitted path and follows a symlink to the answer key.
- The agent does not need to know the secret value during the run for this to break grading.
- Ground truth must be independent from agent-writable outputs.
- Reject symlinks and validate that the submitted artifact is a normal file before comparison.

### Exhibit D

Likely issue: the verifier misses a material invariant between reported fields.

Core points to include:

- The interval can be nearly zero-width while the margin of error looks plausible.
- Existing checks inspect isolated properties but do not connect interval width to margin of error.
- This allows fabricated or degenerate confidence intervals to pass.
- Require nonzero interval width and consistency between interval bounds and margin of error within reasonable tolerance.

### Exhibit E

Likely issue: the numerical task is under-specified and the reference method is too crude.

Core points to include:

- The task asks for an accurate re-entry time but does not define integration/crossing conventions.
- The oracle uses one-second stepping and reports the first crossed step, which can be outside the tolerance of a better method.
- Correct, more accurate solutions can be unfairly rejected.
- Specify the numerical convention or use a more accurate reference with a tolerance tied to real numerical uncertainty.
