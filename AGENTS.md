# Project 1 Agent Instructions

This workspace keeps persistent project memory in `PROJECT_MEMORY.md`.

These instructions apply to every task under this `Project 1` folder and its task subdirectories.

Before starting any task in this folder, always read:

- `PROJECT_MEMORY.md`
- `PROJECT_DYNAMO_LEARNINGS.md`
- `DYNAMO-PLAYBOOK.md`
- `FORK_AND_PUSH_GUIDE.md`
- `PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md`
- `project_dynamo_reviewer_notes.md`

For form-filling or submission tasks, also read:

- `HANDSHAKE_DYNAMO_FORM_FILLING_GUIDE.md`

Then:

- Apply the pipeline lessons proactively instead of rediscovering them.
- If any listed file is missing, note that briefly and continue with the files that exist.

While working:

- When blocked, identify whether the blocker is local setup, GitHub auth, fork/remotes, Harbor validation, static review, pass@, deep review, QC, or task-contract fairness.
- Prefer fixing the underlying pipeline/reviewer issue over changing task logic blindly.
- Treat infrastructure failures, setup failures, provider failures, and all-run timeouts as non-evidence for task difficulty.
- Keep verifier rules, instructions, reference solution, visible data, hidden tests, metadata, and PR evidence aligned.

GitHub and push safety:

- Do not force push unless it is necessary to update an existing PR branch after history was intentionally rewritten or to retrigger a pipeline that requires a new commit shape. Prefer a normal `git push` for ordinary changes.
- Before any force push, explain why it is needed, confirm the target remote and branch are the user's fork/submission branch rather than upstream or a protected/default branch, and prefer `git push --force-with-lease` over plain `--force`.
- Run GitHub CLI (`gh`) commands outside the sandbox when they depend on GitHub auth, private repo access, network access, run logs, checks, forks, or PR creation/update. Sandboxed `gh` results can be misleading because credentials, keychain state, and network access may differ.

After finishing or learning something reusable:

- Update `PROJECT_MEMORY.md` with a short dated note.
- Add only broad lessons that will help future tasks; keep task-specific noise out unless it explains a recurring blocker.
- If the lesson is Dynamo-specific and detailed, also update the more focused Dynamo playbook or checklist.

## Cursor Cloud specific instructions

Cloud Agents clone this repo from GitHub. They do not see unsaved local files or unpushed commits.

- Treat the files listed at the top of this `AGENTS.md` as required reading for every Cloud Agent run in this workspace.
- Prefer updating `PROJECT_MEMORY.md` and the Dynamo playbooks here, then push, so the next Cloud Agent run picks up the same memory as local agents.
- Do not commit individual `dynamo-*` task folders into this instruction repo; those tasks stay in their own forks.
- For GitHub CLI, fork, PR, and check work: use authenticated `gh` with network access; confirm `gh api user --jq .login` before private-repo actions.
- Secrets and env vars for Cloud Agents belong in the Cloud Agents dashboard, not in committed files.
