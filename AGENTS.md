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
- `CLOUD_AGENT_DOCKER_HARBOR.md`

For form-filling or submission tasks, also read:

- `HANDSHAKE_DYNAMO_FORM_FILLING_GUIDE.md`

Then:

- Apply the pipeline lessons proactively instead of rediscovering them.
- If any listed file is missing, note that briefly and continue with the files that exist.

## Mandatory: look at cosine last-commit window before EVERY push

**Do this on every Dynamo submission push. No exceptions. Do not skip when the change feels “small” or “docs-only”.**

Enforced `review / cosine_similarity` compares only:

- `task/instruction.md`
- `task/tests/test_outputs.py` (path may be `tests/test_outputs.py` in Harbor layout)

…first 64 KiB each, threshold typically `0.9`. The service can match against **delivered Dynamo tasks and this PR’s last ~3 commits / lineage snapshots**. A new git SHA alone never clears a flag.

Before `git push` to `submission`, answer all of these. If any answer is “no”, do not push yet:

1. Did I open the latest cosine sticky / check conclusion for this PR?
2. Is cosine currently **enforced** (or was it green only after a prior surface rewrite)?
3. Do `instruction.md` **and** `test_outputs.py` both change in this commit vs `HEAD~1` / the last ~3 SHAs?
4. Is the change a **load-bearing contract** (new graded artifact/path/digest/schema/assert harness), not only wording, docstrings, empty commits, or whitespace?
5. Would a reviewer still see a different comparison embedding than the previous green/red cosine SHAs?

If the sticky says `"too similar to a delivered Dynamo task"`:

- Stop. Do **not** empty-retrigger, close/reopen, or `gh run rerun`.
- In **one** commit, change **both** compared files with a real graded deliverable + verifier reshape (see below).
- Re-run Harbor oracle `1.0` / nop `0.0` before push.

If the sticky is HTTP/`401`/`503`/`000` / Actions download failure → infra; empty retrigger is OK.

### How to clear a real cosine flag

Change **both** compared artifacts in one commit:

1. Add a graded agent-visible deliverable (new output path, digest/ledger bind, profile sidecar, renamed audit artifact, etc.).
2. Wire it through instruction / FORMAT_NOTES / RULEBOOK, solution, reference, calibration if needed, and verifier.
3. Reshape `tests/test_outputs.py` (new module split, new test names, new asserts) so the verifier embedding moves.
4. Harbor oracle `1.0` / nop `0.0` before push.

Docstring-only or atomic-split-only edits are **not** enough when the last cosine-green SHA already introduced the same artifact. Treat the last ~3 commits as poison for near-duplicate surfaces.

While working:

- When blocked, identify whether the blocker is local setup, GitHub auth, fork/remotes, Harbor validation, static review, cosine similarity, pass@, deep review, QC, or task-contract fairness.
- Prefer fixing the underlying pipeline/reviewer issue over changing task logic blindly.
- Treat infrastructure failures, setup failures, provider failures, and all-run timeouts as non-evidence for task difficulty.
- Keep verifier rules, instructions, reference solution, visible data, hidden tests, metadata, and PR evidence aligned.

### Enforced cosine similarity (`review / cosine_similarity`) — detail

This gate can flip from shadow to **enforced** mid-PR. Once enforced, it runs on **every push** and can block before static/validation/pass@.

- Compared surfaces are only `task/instruction.md` and `tests/test_outputs.py` (first 64 KiB each). Threshold is typically `0.9`; sticky often hides the matched task.
- **Recent-commit window (always check):** the checker compares the current surfaces against this PR's **last ~3 commits** and stored/delivered snapshots of the same lineage. Empty commits, amend-style redraws, docstring-only patches, and tiny QC wording often fail immediately with `"too similar to a delivered Dynamo task"` even when an older duplicate sticky said UNIQUE.
- Sticky `"too similar to a delivered Dynamo task"` = real **flag** verdict, not infra.
- Sticky `"could not produce a verdict (HTTP …)"` / `401` / `503` / `000` / Actions download `Service Unavailable` = infra or auth.
- Shadow-mode scores above threshold (e.g. verifier `0.91`) warn that the next enforced run will block the same surface.
- If only one facet is over threshold, keep the green facet stable and move the red one harder; if both are high, add another cross-artifact invariant.
- Long-lived PRs can self-match earlier SHAs of the **same** task at ~0.99 after tiny retries — change surfaces, not just wording.

GitHub and push safety:

- **Single account for Cloud Agents: `nishant4731` only.** Do not keep `cursor` / `cursor[bot]` as an active `gh` user and do not `gh auth switch` mid-task.
- **Auth does not persist across chats.** Interactive `gh auth login` in one VM is gone in the next chat. Persist nishant via a Cloud Agents dashboard Runtime Secret `GH_TOKEN` (or `NISHANT_GH_TOKEN`) — see `FORK_AND_PUSH_GUIDE.md`. Memory-repo docs alone do not log the account in.
- At session start: `export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"` if needed, then `gh api user --jq .login` must print `nishant4731`. Only prompt for device login if that secret is missing.
- Strip Cursor managed git URL rewrites that inject `x-access-token` for `cursor[bot]` on `github.com`. Those rewrites make every `git push` look like the bot even when `gh api user` prints `nishant4731`. See `CLOUD_AGENT_DOCKER_HARBOR.md` / `FORK_AND_PUSH_GUIDE.md`.
- Do not force push unless it is necessary to update an existing PR branch after history was intentionally rewritten or to retrigger a pipeline that requires a new commit shape. Prefer a normal `git push` for ordinary changes.
- Before any force push, explain why it is needed, confirm the target remote and branch are the user's fork/submission branch rather than upstream or a protected/default branch, and prefer `git push --force-with-lease` over plain `--force`.
- Run GitHub CLI (`gh`) commands outside the sandbox when they depend on GitHub auth, private repo access, network access, run logs, checks, forks, or PR creation/update. Sandboxed `gh` results can be misleading because credentials, keychain state, and network access may differ.

After finishing or learning something reusable:

- Update `PROJECT_MEMORY.md` with a short dated note.
- Add only broad lessons that will help future tasks; keep task-specific noise out unless it explains a recurring blocker.
- If the lesson is Dynamo-specific and detailed, also update the more focused Dynamo playbook or checklist.

## Cursor Cloud specific instructions

This repo (`nishant4731/project-1-dynamo-memory`) is the shared memory for all Dynamo task Cloud Agents.

Cloud Agents working on any Dynamo task repo must:

1. Clone or locate this memory repo first (User Rule requires it).
2. Read the files listed at the top of this `AGENTS.md` before editing the task.
3. Before claiming Harbor validation, follow `CLOUD_AGENT_DOCKER_HARBOR.md` (vfs dockerd, cgroup workarounds, manual oracle/nop fallback).
4. Before every `git push` to a Dynamo `submission` branch, run the **Mandatory: look at cosine last-commit window** checklist above.
5. After reusable lessons, update `PROJECT_MEMORY.md` here, commit, and push to `main`.

Notes:

- Cloud Agents do not see unsaved local files or unpushed commits.
- Do not commit individual `dynamo-*` task folders into this instruction repo; those tasks stay in their own forks.
