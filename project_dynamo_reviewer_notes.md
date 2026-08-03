# Project Dynamo Reviewer 1 Notes

## Decision Rule

- **Accept / score 4-5**: no blocking issue. A proposal/category mismatch alone is not blocking.
- **Revise / score 3**: real, fixable issue that does not collapse the task's difficulty. Feedback must name the file/criterion, the defect, and the fix.
- **Reject / score 1-2**: illegitimate difficulty where fixing the issue would trivialize the task, unfair verifier/wrong golden answer, task needs rebuild, or prior required feedback was ignored.

Reject vs Revise hinge: if disclosing/fixing the missing rule leaves the task genuinely hard, choose **Revise**; if it makes the task easy/trivial, choose **Reject**.

## HAI Form Editing Rule

If the HAI page already contains stale answers, edit only the fields owned by the current review layer.

Do **not** edit submitter/contributor fields during R1 review, including proposal text, artifact type, task objective, uploaded pass@ screenshot, or the submitter's pass@ score. Even when those values are stale, leave them as submitted and account for the mismatch in the review comments.

Reviewer-owned fields are safe to edit:

- Issue selection.
- Exact reviewed commit hash.
- Review comments.
- Task quality score.
- Task verdict.
- Fellow quality verdict.
- Right-side Praise or General Feedback.

If a submitter field is changed by mistake, revert it to the original value before submission.

## Prefilled Reviewer Fields Are Evidence

When an R1/R2 HAI page has prefilled reviewer fields, read them before forming the final verdict. Do not assume they are stale, and do not treat them as a UI detail to clean up after the repo review.

Review order for prefilled tasks:

1. Read the GitHub PR/task package and form an initial technical view.
2. Read the HAI proposal and every prefilled reviewer-owned field before choosing Accept/Revise/Reject.
3. Verify each prefilled claim against concrete files, tests, pass@ comments, and expected outputs.
4. Keep, edit, or replace only reviewer-owned fields after that verification.

Calibration from `dynamo-daff0ea-software-engineering`: a local repo pass initially looked like Accept because the spec, verifier isolation, checks, and pass@ analysis were strong. The prefilled review comment caught a sharper issue: `formatting/014` expected duplicate record fields to be preserved and printed, but `spec.md` did not disclose duplicate-field semantics or tie ordering, and the reference deduped fields by name in subtyping/join. Several agents converged on the defensible unique-keyed-record interpretation and failed the same hidden convention. That made the correct route **Revise, score 3, Trainable**, not Accept.

Deep-check rule: if pass@ failures cluster around the same "reasonable but different" interpretation, investigate whether the task has an underspecified hidden convention even when the automated checks are green and the task is otherwise well engineered.

Fellow-quality calibration: a material Revise caused by a missed spec/verifier fairness issue is usually **Trainable**, not Excellent, even if the task is close and the fellow did high-quality work.

## Qualification Answers

- Fixable issue that does not collapse difficulty: **Revise**
- Excellent/sendable task: **Accept, score 4-5**
- Feedback purpose: **specific and actionable so the next revision can pass**
- Definite rejects:
  - Undisclosed verifier requirement that becomes trivial once disclosed
  - Wrong golden/reference solution
  - Unspecified ordering/naming/format convention that trivializes once pinned
  - Undisclosed incorrect instruction/input information
  - Overly strict verifier rejecting valid answers
  - Ignored prior required reviewer fixes
- Proposal/category mismatch alone: **Accept**
- Non-exploitable theoretical verifier note: **Accept**
- Typical revise cases:
  - Agent-writable verifier input can be pinned and task stays hard
  - Small coverage gap for a stated requirement
  - Misleading sentence whose correction leaves task hard
  - Missing boilerplate that does not affect difficulty
  - Instruction contradiction where one sentence states exhaustive bucket/accounting behavior but the verifier expects an exception; if clarifying the exception leaves the task hard, choose Revise.

## Calibration: Example-Derived Hidden Specs

When a task's central premise is that the agent must reverse-engineer hidden rules from examples, do not only confirm that the repo is coherent, the checks are green, and pass@ failures look valid. The review must test whether the examples uniquely determine the hidden spec.

Concrete R2 override lesson from task `7d83944c-58b4-495e-8bc8-7e98e3a80c23`: the R1 write-up covered the same ground as the automated review and missed the core risk. The task required deriving a hidden behavior from three example tapes. R2 built an alternative interpretation for how `MERGE` assigns IDs after a prior delete; that alternative matched all three pilot tapes and the calibration check, but produced different answers on two main-tape stories. That is a working counterexample showing the examples did not pin down the verifier's intended rule.

Review rule: for tasks built around examples, traces, pilot tapes, demonstrations, or hidden protocol inference, actively try to construct at least one plausible alternative rule. If the alternative matches all public examples/calibration data but fails the hidden/main verifier answer, treat it as an underspecification or unfair hidden convention. Do not accept based only on green checks or automated-review language.

Feedback pattern:

> Revise/Reject. The blocking issue is that the public examples do not uniquely determine the hidden rule the verifier expects. I can use an alternative rule for `<specific behavior>` that matches all provided examples/calibration cases but produces a different result on `<specific checked case>`. Add an explicit rule or an example that distinguishes the intended behavior. Choose Revise if the clarification preserves the task's core difficulty; choose Reject if the task's difficulty depends mainly on guessing that hidden convention.

## Task Verdicts Filled In Form

| Task | Verdict | Score | Reason |
|---|---|---:|---|
| Task 1 | Accept | 4-5 | Hidden-input failures are legitimate; only proposal-specific bug mismatch is non-blocking. |
| Task 2 | Revise | 3 | Instruction incorrectly says word-initial pieces universally use marker; fixing leaves tokenizer task hard. |
| Task 3 | Reject | 1-2 | Exact dependency-array order is enforced but unstated; pinning it removes the main difficulty. |
| Task 4 | Accept | 4-5 | All failures map to documented VM spec composition rules; verifier recomputes reference. |
| Task 5 | Revise | 3 | Verifier trusts agent-writable capture.pcap; pin hash/read-only copy fixes tamper issue while task stays hard. |
| R2 calibration: state_summary retryable | Revise | 3 | If instructions say every incomplete task is accounted for exactly once across buckets, but verifier omits tasks with an outstanding valid retry, this is a material instruction conflict. Clarify that outstanding-valid-retry tasks are omitted from `state_summary` buckets and update/remove the “exactly once” sentence. |
| R2 calibration: example-derived MERGE IDs | Revise/Reject depending on fix impact | 2-3 or 1-2 | If public examples do not uniquely determine a hidden rule, and a plausible alternative matches all examples but diverges from verifier/golden answers, the task has an underspecified hidden convention. Require a distinguishing rule/example; reject if that clarification removes the main difficulty. |

## Feedback Pattern

Use this structure for Revise/Reject:

1. Verdict and severity.
2. File/criterion/test where defect lives.
3. Why it blocks or does not block.
4. Exact fix required.
5. Reject-vs-Revise justification when ambiguity/spec issue is involved.

Example:

> Revise. The blocking issue is in `task/tests/test_outputs.py`: it recomputes expected values from `/app/data/capture.pcap`, which the agent can overwrite. Pin the capture SHA-256 or read a read-only copy before computing the reference. This remains a Revise because the packet-reassembly challenge stays hard after the verifier input is pinned.

R2 calibration example:

> Revise. The blocking issue is an instruction contradiction around `state_summary.retryable`: the prompt says each incomplete task is counted exactly once under active lease, blocked, or retryable, but the verifier expects incomplete tasks with an outstanding valid retry to be omitted from all those buckets. Explicitly state that outstanding-valid-retry tasks are omitted from `state_summary` buckets and update the “exactly once” sentence with that exception. This is Revise, not Reject, because the task and verifier are otherwise coherent and the clarification preserves the core difficulty.
