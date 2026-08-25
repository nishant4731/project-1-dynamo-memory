# Project Dynamo — Rework Guide

Source: https://project-dynamo.learn.joinhandshake.com/rework and its three sub-pages
(`/rework/step-1`, `/rework/step-2`, `/rework/step-3`), read 2026-08-25, plus the two pages
they cross-reference (`/stump-the-model/why-tasks-get-rejected`, `/submit/platform`).

This file is the operating procedure for a task that comes back for rework. It does not
replace `HANDSHAKE_DYNAMO_FORM_FILLING_GUIDE.md` (platform form mechanics) or
`PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md` (pre-push soundness); it sits on top of them.

---

## 0. The shape of the rework pipeline

```
[grey]  1. Flagged for rework   — findings already logged as a checklist in ONE GitHub Issue
[blue]  2. Review issues        — read every open issue, end to end
[blue]  3. Fix the code         — address each finding in the repo
[blue]  4. Validate & resubmit  — oracle passes, nop fails, push
[green] 5. Resubmit             — checks that ran are green, then comment on Platform
```

Two framing rules that govern everything below:

- **You do not re-diagnose the task.** Every problem review found is already written up as a
  checklist item. Your job is read → fix → clear, not "work out what went wrong".
- **Rework is not a lighter review.** Whichever checks run against your fix clear the *exact
  same bar* as a first submission. Same accept band on pass@, same green-checks requirement.

---

## 1. Review your assigned rework task and its GitHub issues

### Where the findings live

- Your task repo under the **`handshake-project-dynamo`** org → **Issues** tab.
- **One open issue per review round** — not one issue per finding. Title format:
  `[Task Feedback] <rating> — <task-id>`
- Inside the issue:
  - **`Findings to address`** — each unchecked checklist item is one defect.
  - **`Passed criteria (keep these passing)`** — criteria that already cleared review.

### What a finding contains

Each unchecked finding names:
- the **criterion** it is filed under,
- a **severity**,
- a **description** of the defect,
- **links to specific `file:line` ranges**.

### The six review criteria

Findings *and* passed criteria are drawn from the same pool of six. Any of the six can be
flagged; which one lands where varies task to task.

| Criterion | What it guards |
|---|---|
| `coherent_contract` | The prompt pins down exactly one answer |
| `correct_reference_solution` | `solution/` actually implements the stated spec |
| `sound_verifier` | The tests cannot be passed without doing the work |
| `protected_ground_truth` | Answers/expectations are not reachable from an agent-writable path |
| `deterministic_execution` | Same input → same result, every run |
| `runnable_realistic_task` | The task builds, runs, and resembles real work |

### How to read it

- **Read the whole issue before touching any code.** Reading them all first tells you whether
  they are independent fixes or symptoms of one underlying problem.
- **Fix what it says, not what you assume it says.** Each finding is written against the actual
  state of your repo.
- **If a finding is genuinely unclear, or you disagree — comment on the issue.** Do not silently
  do something else.

### Step-1 checklist (from the guide)

- [ ] Read every unchecked finding on the task repo issue, top to bottom
- [ ] Noted which findings share a root cause and can be fixed together
- [ ] For each finding, know which file it touches (`solve.sh`, `tests/`, `Dockerfile`, `instruction.md`, `task.toml`)
- [ ] Commented on any finding you can't act on as written, instead of guessing

### ⚠️ Save the raw issue text NOW

The platform submission form has a field:

> "Please paste the content you see in issues. This is to check whether you are actually fixing
> the issue that was flagged."

You must paste the **full content of the GitHub issue** — findings, criteria names, descriptions.
**A one-line summary will not cut it.** Copy the raw issue body to a scratch file before you start
editing, so you still have it at submission time.

---

## 2. Fix the code

### Branch

Work on a branch in your fork, exactly as during the build. Conventions are unchanged — build
steps 3 through 7 of the main workflow remain the source of truth for how each file should look.

```bash
cd <your-task-repo>/task
git checkout submission   # or: git checkout -b rework
```

### Fix or flag

- **If a flagged finding is simple, fix it — most rework is.**
- If fixing one would mean **rewriting `solution/`, `tests/`, or `instruction.md` from scratch**,
  mark the rework **unsuccessful**, explain your reasoning **against each flagged finding**, and
  submit as-is.
- This exception is for **genuine redesigns, not routine difficulty**. The expectation for every
  rework is still that the issues get fixed and the task is resubmitted fully green.

### The two most common findings

These two criteria account for most rework.

#### `sound_verifier` — the tests can be passed without doing the work
Fix in `tests/test_outputs.py` / `tests/test.sh`.

Real reviewer write-ups:
- **Hardcoded precedence never mutated** — a candidate can echo the harness with the shipped
  timestamp precedence, timezone, collision order, and device offsets baked in; the mutation test
  never changes precedence or checks behavioral effects.
- **Only two collapse cases covered** — a cold `max-age=60` result and a preseeded `304`, so
  relookup-only implementations pass without ever reusing a result.
- **Hidden case dirs are writable** — a shortcut precreates them, swaps each generated input
  mid-run, emits empty artifacts, and the oracle derives expectations from the altered input.
- **Interactions never tested together** — delay and unmount are tested separately with no owner
  override, and pointer tests never change the top layer mid-sequence, so the reference defects pass.

Pattern: *mutate the decisive rule and assert the behaviour flips; cover interactions jointly, not
one at a time; make hidden case dirs non-writable.*

#### `coherent_contract` — the prompt doesn't pin down one answer
Fix in `instruction.md` (and any spec under `environment/data/`).

Real reviewer write-ups:
- **Undefined sort order** — the exact-byte report sort key omits tombstone revision, so distinct
  tombstones on one target can be ordered either way and both are "correct".
- **Rule given only by example** — the proprietary check is specified through 37 examples and
  exclusions with no algorithm family or constants; infinitely many functions fit and disagree on
  hidden blocks.
- **Unspecified math** — the normalization function, dual-mode coefficient formula, and
  intermediate rounding are never defined, despite the claim that short samples determine them.

Pattern: *name the canonical rule (sort key, tie-break, algorithm family, constants, rounding).*

### Keep the task hard for the right reason

If an issue is about difficulty, fix the **core reasoning** the task demands. **Do not** pad the
runtime, add busywork, or raise the timeout to make the agent fail — that gets caught downstream.

### Step-2 checklist (from the guide)

- [ ] Every open issue has a concrete change in the repo behind it
- [ ] `instruction.md`, `solution/`, and `tests/` still describe the same task — paths, schemas, and limits agree
- [ ] The `Dockerfile` still never `COPY`s `solution/` or `tests/`, and ground truth isn't readable from an agent-writable path
- [ ] `instruction.md` still ends with the "You have N seconds…" line, and N matches `[agent].timeout_sec`

### Do not regress the passed criteria

The issue ends with `Passed criteria (keep these passing)`. Your fix PR must clear every unchecked
finding **without breaking any of those**. Re-check them explicitly before you push.

---

## 3. Validate and resubmit

### Validate locally first — the two hard gates

```bash
harbor run -p . --agent oracle   # must score reward 1.0
harbor run -p . --agent nop      # must score reward < 1.0
```

If either is off, the fix isn't done. **Don't push yet.**

### Not every check reruns

```
Does your fix change the task's difficulty?
 ├─ No  → pass@ skipped — targeted fix
 └─ Yes → full run — changed solution or clarified instructions
Either way: every check that ran must be green.
```

### Push and open a NEW PR

**Your original PR is closed. Rework goes out as a brand new PR — there is no "update the old
one" path.**

```bash
git add -A
git commit -m "Fix sound_verifier finding from #2: tighten verifier tolerance on rounding"

# If you're back on the original submission branch (already tracked upstream):
git push

# If you branched to a new rework branch:
git push -u origin rework

gh pr create --repo handshake-project-dynamo/<your-task-repo> --fill
```

Commit-message convention — **name the finding in the commit message, not just the PR
description**:

```
Fix <criterion> finding from #<issue number>: <short description>
```

PR description: there is one issue per review round, so reference that single issue number
(e.g. `Fixes #2`) and list which findings you addressed **by criterion name**. **A single PR must
clear every unchecked finding on that issue.**

### Step-3 checklist (from the guide)

- [ ] Oracle passes (reward 1.0) and nop fails (reward < 1.0) locally
- [ ] Every check that actually ran on your PR is green (which ones run depends on your fix)
- [ ] If pass@ ran for your fix, its bot comment lands in the **accept band** — same bar as a first-time submission
- [ ] Every finding on the linked issue is checked off **and the issue itself is closed**
- [ ] Recorded the resubmission on the platform

**Done means:** every check that ran is green, pass@ (if it ran) is in the accept band, and no
open issues remain on the repo.

---

## 4. Recording the resubmission on the platform

Same flow as a first submission (`/submit/platform`):

1. **Confirm the PR is actually green on GitHub first.** Submitting with failing checks wastes a
   reviewer slot and bounces straight back.
2. **Walk the checklist one item at a time**, then add reviewer notes covering anything subtle,
   tricky, or non-obvious about the task.
3. **Paste the full GitHub issue content** into the "Please paste the content you see in issues"
   field (see §1 — this is the rework-specific field).
4. **Attach the pass@ screenshot and enter the pass@ score.** The pass@ result is a comment on
   the Pull Request tab in the repo — screenshot that comment.
5. **Read the pass@ Job Analysis.** A failed run on its own is not sufficient; the Job Analysis
   explains *why* it passed or failed. Act on it before submitting.

---

## 5. Background: why tasks get rejected (the five reasons)

All five share one root problem: **a low pass rate that looks like difficulty but isn't** — the
model failed because the task was unfair, not because it reasoned and got the answer wrong.

**The single test behind all five:** *If spelling out the deciding rule makes the task easy, the
difficulty was fake.* Ask: "with the deciding rule written plainly, would a strong engineer still
struggle?" If no, you'll get flagged.

**Roughly half of all flagged tasks fail for reason 1.** If you fix nothing else, make sure every
rule your verifier enforces is written in the instructions.

| # | Reason | What it is | How to avoid it |
|---|---|---|---|
| 1 | **Undisclosed verifier convention** | Verifier requires a format, sort order, tie-break, or convention `instruction.md` never mentions. Agents solve everything documented and fail only on the hidden rule. | Write down every rule the verifier checks — output format, ordering, tie-breaks, edge cases. Test: could a reasonable different implementation still pass? If only your exact choice passes and you never stated it, disclose it. |
| 2 | **Contradictory shipped data / spec** | A data file, config, or the reference solution follows a different rule than the instruction states. An agent that trusts the instruction does the right thing and still fails. | Make shipped data and reference solution obey the instruction exactly. Regenerate drifted fixtures. Never ship a file that contradicts the instruction — even one labeled "old" or "not used". |
| 3 | **Ambiguous spec** | A term or rule has two defensible readings; the verifier silently accepts only one. The score just measures which reading the model guessed. | Name the single canonical rule (assignment, priority, tie-break, sort order). Then check: once unambiguous, is the task still hard? If not, add a real crux. |
| 4 | **Difficulty collapses once the defect is removed** | The only thing failing the model is one unstated or broken rule. Disclose or fix it honestly and the task is trivial. | Build difficulty into genuine reasoning that survives full disclosure. A task that only "works" because of one confusing rule needs a new hard part, not a patch. |
| 5 | **Misleading / decoy documentation** | The task points the agent at the wrong answer via an authoritative-looking file, while the real rule hides in something marked "deprecated / superseded / not used" — and nothing visible corrects it. | Misdirection is allowed only if the task can set the record straight ("No uncorrectable lie"). Never state a wrong rule the agent can't overturn. |

### These are now caught by pass@2 in GitHub Actions

The pass@2 check flags these right after it runs — the analysis of the two trials calls out when
failures look **unfair** (undisclosed rule, ambiguity, contradiction, decoy) rather than a genuine
miss. The flag appears in your PR comments. **Read it before pushing further: if it says your
failures aren't legitimate, fix the cause — don't try to submit around it.**

Self-check before pass@2 does:
- Run your own oracle from a **clean checkout** and confirm the failures your trials show are the
  intended crux — not a format, ordering, or naming convention.
- **Red flag:** if the failing tests are about *file existence* or *output formatting*, that's
  usually an undisclosed convention, not real difficulty.
- Re-read `instruction.md` as if you'd never seen your solution: is every rule the verifier checks
  actually stated? Can any sentence be read two ways?
- A fair 0/5 is great; a *flagged* one means fix the cause.

---

## 6. Cross-references in this repo

- `AGENTS.md` — mandatory validation loop and playbook-recording rules; applies unchanged to rework pushes.
- `PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md` — pre-push soundness sweep.
- `HANDSHAKE_DYNAMO_FORM_FILLING_GUIDE.md` — platform form mechanics for the submission record.
- `DYNAMO-PLAYBOOK.md`, `PROJECT_MEMORY.md` — category/subcategory playbooks; if the rework is a
  difficulty finding, start from the playbook for the task's exact `[metadata]` category+subcategory.
- `PROJECT_DYNAMO_STUMP_GUIDE.md` — the stump-the-model material this rework guide's §5 comes from.

## 7. Local pitfalls worth re-reading before a rework push

From auto-memory, these have each cost a cycle and all apply to rework pushes:

- **Don't push mid-pipeline.** Pushing while checks are in flight kills every gate that hasn't
  reported. Hold the fix until checks settle.
- **In-flight PR heads are never indexed** — no reflex reskin is needed on a rework push.
- **Never `chmod` the reward file.** Harbor reads `/logs/verifier/reward.txt` host-side; `0600`
  turns a green suite into an Oracle ❌.
- **Rebuild the base image before the validation image** after any fixture regeneration, or you get
  a fake oracle failure from a stale env layer.
- **Verifier must be idempotent** — if QC A1 is red while validation is green, your verifier can
  only run once. Stash the reference; don't delete it.
- **Sticky comments edit in place** — a red job with a stale verdict sticky died in infra; check
  whether pass@2 even ran before reading its number.
