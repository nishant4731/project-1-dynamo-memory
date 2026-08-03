# Project Dynamo Stump-the-Model Notes

Source guide:
- https://project-dynamo.learn.joinhandshake.com/stump-the-model
- https://project-dynamo.learn.joinhandshake.com/stump-the-model/strategies
- https://project-dynamo.learn.joinhandshake.com/stump-the-model/amplifiers
- https://project-dynamo.learn.joinhandshake.com/stump-the-model/live-examples
- https://project-dynamo.learn.joinhandshake.com/stump-the-model/why-tasks-get-rejected
- https://project-dynamo.learn.joinhandshake.com/stump-the-model/update-log

Read on: 2026-07-08

Browser check note: the Strategies page exposes the A-I strategy "options" as expandable `<details>` cards, not as actual multiselect/select controls. I inspected the related Stump pages for `select`, `option`, `input`, `listbox`, `checkbox`, `aria-multiselectable`, and `aria-selected` controls; none were present beyond navigation buttons and the A-I expanders.

## 2026-07-22 Browser Read: Stump Guide Refresh

Source: https://project-dynamo.learn.joinhandshake.com/stump-the-model

The live guide reinforces that a good stump should make the agent do most of the work correctly, then fail on one decisive point. The decisive point must still have exactly one right answer; if two careful solvers can defend different outputs from the same visible materials, the task has a contract defect, not valid difficulty.

Use this quick screen before trusting a low pass rate:

- If spelling out the deciding rule makes the task easy, the difficulty was probably artificial.
- If the task admits a real method choice, name the canonical method in `instruction.md`, such as estimator, correction, degrees of freedom, crossing rule, ordering rule, or tie-break.
- Wide tolerance bands are a smell when they compensate for an unpinned contract. They are not proof of robust numerical grading by themselves.
- Verifiers should check material relationships between fields, not only proxies. For statistical outputs, this means checking confidence interval width, standard-error consistency, reference bounds, and the exact top-level schema when those are part of the contract.
- Misdirection is fair only when stronger evidence lets a careful solver reject the decoy. A trusted-looking wrong tool, stale comment, or partial output must be recoverable from data or spec, not a pure gotcha.

## 2026-07-12 Update: Automated Difficulty Check

Source: Project Dynamo team announcement supplied in the task thread. The linked rejection-guide page was not publicly retrievable through search when these notes were updated.

PRs now run an automated difficulty check immediately after `pass@2`. The check analyzes the actual failing trajectories and flags failures that look unfair before human review. Passing Oracle/Nop validation is necessary but no longer enough: at least one model run must fail validly because of the intended reasoning challenge.

Interpret the pipeline in this order:

1. Static and rubric checks validate task structure, clarity, taxonomy, and security.
2. Duplicate checking validates novelty.
3. Oracle/Nop validation proves the reference solution passes and untouched input fails.
4. `pass@2` runs agents against the task.
5. The difficulty analysis decides whether each failure is a genuine model limitation, an unfair task/verifier failure, a timeout still making progress, or infrastructure failure.
6. `pass@5` proceeds only after `pass@2` contains the required valid-failure anchor.

A red `pass@2` is therefore not automatically evidence that the task is hard. Read the analyzer's per-trajectory taxonomy, failing tests, actual-versus-expected values, and approach comparison before changing the task.

### Five Common Rejection Causes

1. **Undisclosed grading rule.** The verifier enforces a format, ordering, tie-break, tolerance, or state transition that the agent-visible materials never state or force.
2. **Contradictory task files.** Instructions, fixture data, reference solution, expected output, and verifier implement different rules.
3. **Ambiguous instructions.** More than one reasonable reading exists, but grading silently accepts only one.
4. **Mistake-only difficulty.** The only challenge is a typo, broken dependency, conflict marker, missing import, or other accidental defect. Fixing or disclosing it removes the difficulty.
5. **Decoy without a recovery path.** A trusted-looking artifact points to the wrong answer, but no stronger evidence lets a careful solver detect and correct it.

### Deciding Test

Write the deciding rule down plainly. If the task then becomes easy, the difficulty was artificial. A strong task remains difficult when every rule is explicit because the challenge lies in applying coupled rules, reconstructing state, searching a constrained space, or handling realistic semantic interactions.

### Fair-Difficulty Audit

Before pushing a task, verify all of the following:

- Every graded schema, ordering rule, tie-break, cutoff, default, and exact-byte requirement is stated or unavoidably derivable from agent-visible evidence.
- `instruction.md`, console/data files, generator, reference solution, expected data, and tests implement one identical rule.
- A careful domain expert can distinguish every decoy from authority without guessing.
- The intended crux still requires substantial reasoning after it is disclosed fully.
- A naive solver fails specifically at the intended crux, not during setup, imports, conflict markers, formatting, or cleanup.
- The verifier deterministically accepts a correct implementation and rejects plausible wrong implementations.
- Timeouts and provider errors are treated as infrastructure unless the analyzer explicitly classifies a stuck run as a valid failure.
- Failure analysis names the intended crux and points to a concrete incorrect value or failing test whenever the verifier ran.

### Responding To Difficulty Results

- **Model solved:** strengthen the disclosed semantic or algorithmic coupling; do not add an unstated verifier trap.
- **Valid verifier failure at the intended crux:** preserve it and allow `pass@5` to measure robustness.
- **Undisclosed-rule or ambiguity flag:** align the instructions and all task files before rerunning.
- **Incidental implementation failure:** remove or disclose the accidental mechanic, then strengthen the real crux separately.
- **Still-progressing timeout:** reduce mechanical workload or obtain the supported timeout; do not count it as a reasoning failure.
- **Rate limit, provider error, environment setup failure, or missing verifier run:** escalate or rerun after infrastructure recovery. Do not churn validated task logic based on that trajectory.

### Current Release-Recovery Lesson

For the release-recovery task, authority capacities, corridor rotation, cooldown, witness ordering, temporal reductions, and semantic conflict rules must remain fully disclosed in the recovery console. Difficulty should come from solving the combined global assignment and bitemporal semantics. A trajectory killed by an OpenRouter rate limit gives no difficulty signal even if its reward is zero; a trajectory that computes the canonical witness assignment correctly shows that the authority crux was solved and should motivate an additional fair semantic crux only after a stable run confirms the downstream behavior.

## Core Principle

A strong Dynamo task should not be hard because it is vague, huge, tedious, or unfair. It should be hard because a capable agent can do most of the work correctly and still fail on one decisive, deterministic point.

The best traps are:

- Determinate: there is one right answer.
- Recoverable: the needed rule can be inferred from available evidence or stated spec.
- Professional: the failure is a real mistake a skilled human would know how to avoid.
- Silent: the wrong answer looks plausible and does not crash.
- Hidden from easy self-checks: visible samples do not reveal the decisive case.

The recurring model weakness is stopping too early after a green local result, trusting a default rule, a convenient tool, or a visible sample without probing the unseen edge.

## Stumping Patterns

### A. Latent Crux

The decisive case is absent from the visible/sample data but present in hidden grading. The agent validates carefully against visible cases, becomes confident, and misses the one branch that matters.

Use when:
- The hidden case exercises a real domain rule.
- The sample is homogeneous along the important axis.
- A professional solver could still infer or guard for the missing case.

Good Dynamo examples:
- A file format where sample chunks use only one encoding, but hidden chunks require a second legal encoding.
- A records task where visible rows have no late supersession, but hidden rows do.
- A media task where visible segments never trigger parity repair, but hidden segments do.

### B. Wrong-Default Lure

The obvious heuristic is almost right but not the true definition. Agents converge on the shortcut because it passes casual inspection.

Use when:
- There is a plausible simple rule.
- The correct rule is more semantic or expensive.
- Both rules agree on most visible data and diverge only on carefully chosen cases.

Good Dynamo examples:
- Treating path-prefix rows as rollups instead of verifying value equality.
- Sorting by revision number instead of applying the official current-state rule.
- Using file extension to determine content type instead of magic bytes or embedded metadata.

### C. Misdirection

The environment contains a trusted-looking but wrong pointer: a helper tool, stale doc, misleading comment, decoy branch, or partial reference output.

Use when:
- The decoy is believable and useful enough to tempt the agent.
- Ground truth is still recoverable from stronger evidence.
- The task tests the real professional skill of validating tools and docs against data.

Avoid making the decoy a lie with no correction path. The solver must be able to discover why it is wrong.

### D. Evidence-Forced Reverse Engineering

The solver must infer undocumented rules from observed input/output behavior or raw data. This is fair when the evidence forces one consistent answer.

Use when:
- The task provides enough traces, logs, archives, binaries, or paired examples.
- A senior engineer could form and test hypotheses until the rule is clear.
- The grader has margin against harmless implementation differences.

Good Dynamo examples:
- Reconstruct a custom checksum from archive examples.
- Infer segment transforms from stored descriptors and hashes.
- Recover hidden scaling, reset, sentinel, or timestamp conventions from logs.

### E. Ordering Assumption

The agent assumes data is sorted, monotonic, well-formed, or stable because the visible sample is. Hidden data violates that implicit invariant.

Use when:
- Correct logic should not depend on input order.
- The sample accidentally supports the wrong stateful implementation.
- Hidden cases require independent anchoring, canonical sorting, or explicit dependency resolution.

Good Dynamo examples:
- Timestamps need pointwise anchoring, not a running lower bound.
- Ledger events must be topologically or causally ordered, not file ordered.
- Repeated artifacts must be deduplicated by authority, not first-seen order.

### F. Discovery Hop

After the hard part, a final value or combination has no partial feedback. This is high-risk: it is fair only if the missing value is discoverable from the provided material.

Use carefully when:
- The opaque rejection behavior is realistic for the domain.
- The correct literal, scope, role, or mode is hinted or derivable.
- The search space is bounded by evidence, not luck.

Avoid pure guessing. If a human expert would call it a coin flip, cut it.

### G. Multi-Mechanism Accumulation

The task requires many independent fixes, and every one must be right. Difficulty comes from breadth under an all-or-nothing verifier.

Use when:
- Each mechanism is individually fair and meaningful.
- The mechanisms are independent enough that one insight does not solve all of them.
- At least one mechanism is hidden by the visible sample.

Good Dynamo examples:
- Multiple archive recovery rules: codec, parity, supersession, release ticket, hash binding.
- Several binary repair bugs: alignment, symbol binding, revision, kind encoding.
- Several report-cleaning rules where missing any one breaks exact output.

### H. Entangled Rules

Each rule is simple alone, but applying them independently gives the wrong global state. The difficulty is coupling, not count.

Use when:
- Events or rules reach backward and change prior validity.
- The correct approach must reason about the whole history/state graph.
- A streaming or one-rule-at-a-time implementation produces plausible but wrong output.

Good Dynamo examples:
- Reset/revocation/supersession event histories.
- Approval workflows where late events resurrect or invalidate earlier records.
- Dependency resolution where one choice changes what another rule means.

### I. Stale Authority

The current value is not the value that was authoritative at the relevant time. Agents default to latest/current state and silently rewrite history.

Use when:
- Inputs include publication times, effective dates, revisions, or cutoffs.
- Visible samples do not contain late corrections.
- Hidden cases require point-in-time lookup.

Good Dynamo examples:
- Use price known at cutoff, not latest corrected price.
- Use document version active at event time, not newest version.
- Use identity/account mapping as of transaction time, not current merged identity.

## Amplifiers

Use these after choosing a fair trap:

- Silent failure: wrong output should look normal, not crash.
- No self-check: visible tests should not expose the hidden decisive case.
- All-or-nothing: one wrong artifact or field should fail the result when the domain justifies exactness.

These are powerful, but they can become unfair if the hidden requirement is not recoverable.

## Fairness Rules

Before shipping a trap, check:

- Can the answer be recovered from instruction plus visible input?
- Is the mistake a real professional mistake, not random trivia?
- Are tolerances and schemas explicit enough that formatting is not the real challenge?
- Does the task avoid stating a false rule that nothing can correct?
- Would a human expert with only the agent-visible material call the failure fair?

If the answer to the last question is no, the task is probably testing luck.

## Live Example Lessons

The guide lists accepted/delivered examples where frontier models failed:

- `bytecode-vm-debug`: fixed an obvious bug, saw green tests, missed a hidden subtraction case.
- `accrued-interest`: followed visible convention and missed a jurisdiction-specific finance rule.
- `gnss-log-decode`: decoded bytes correctly but applied one clock rule to every satellite system.
- `experiment-readout`: used the wrong statistical unit, making a result look significant.
- `legacy-formatter-clone`: guessed known checksums instead of reconstructing the custom one.

Common thread: the agent often got the visible or mechanical part right, then failed by trusting the first plausible model of the problem.

## Dynamo Task Design Checklist

Use this before starting a new task:

- Pick one main trap pattern from A-I.
- Add one or two amplifiers, not five.
- Write down the exact hidden failure mode before generating data.
- Make the visible sample friendly but not representative of the trap.
- Ensure the correct rule is either stated or inferable from data.
- Pin any method choice that can change the graded value.
- Build the oracle from the same rule, not hand-written expected values.
- Verify a naive/default solver fails for the intended reason.
- Treat very wide tolerances as a contract-review trigger before treating them as calibration.
- Verify the official solution passes without relying on hidden test files.
- Make output schema explicit and short.
- Keep `instruction.md` under the static token cap.
- Avoid formatting-only pitfalls unless formatting is the actual domain task.
- In `task.toml`, explain why the task is hard for professional reasons.

## Patterns That Fit Our Recent Dynamo Work

For file/media and audit-record tasks, the strongest reusable patterns are:

- A + I: hidden late correction, stale supersession, point-in-time authority.
- B: plausible path/revision/source shortcut differs from the true authority rule.
- D: custom archive or checksum rule recoverable from descriptors and hashes.
- E: sample order matches the easy assumption; hidden order breaks it.
- G: several independent mechanisms are required, such as decoding, filtering, ledger validation, artifact recovery, and proof hashing.
- H: event-history tasks where resets, revocations, repairs, and supersessions interact.

For future refactors, prefer adding one new decisive semantic crux instead of piling on more proof fields. Proof fields help verification, but the model-stumping work should come from a domain rule the solver must discover or apply correctly.
