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

While working:

- When blocked, identify whether the blocker is local setup, GitHub auth, fork/remotes, Harbor validation, static review, cosine similarity, pass@, deep review, QC, or task-contract fairness.
- Prefer fixing the underlying pipeline/reviewer issue over changing task logic blindly.
- Treat infrastructure failures, setup failures, provider failures, and all-run timeouts as non-evidence for task difficulty.
- Keep verifier rules, instructions, reference solution, visible data, hidden tests, metadata, and PR evidence aligned.

### Enforced cosine similarity (`review / cosine_similarity`)

This gate can flip from shadow to **enforced** mid-PR. Once enforced, it runs on **every push** and can block before static/validation/pass@.

- Compared surfaces are only `task/instruction.md` and `tests/test_outputs.py` (first 64 KiB each). Threshold is typically `0.9`; sticky often hides the matched task.
- **Recent-commit window:** the checker can also compare the current `instruction.md` / `test_outputs.py` against this PR's **last ~3 commits** (and stored/delivered snapshots of the same lineage). That is why empty commits, amend-style redraws, and tiny QC wording patches often fail immediately with `"too similar to a delivered Dynamo task"` even when an older duplicate sticky said UNIQUE.
- Therefore every new push under an enforced cosine gate must change the compared surfaces enough to diverge from those last few SHAs — not just invent a new git SHA. Prefer one load-bearing commit that moves both files; do not push a pipeline-only empty commit after a cosine flag.
- Sticky `"too similar to a delivered Dynamo task"` = real **flag** verdict, not infra. Empty commits / close-reopen / `gh run rerun` will **not** clear it.
- Sticky `"could not produce a verdict (HTTP …)"` / `401` / `503` / `000` / Actions download `Service Unavailable` = infra or auth — empty retrigger or small real fix is fine; do not invent a duplicate-task rewrite.
- Shadow-mode scores above threshold (e.g. verifier `0.91`) are a warning: the next enforced run will block the same surface.
- **Never** answer a real flag with prose-only rewording or empty CI redraws. Change **both** compared artifacts with a load-bearing contract change in one commit:
  1. Add a graded agent-visible deliverable (new output path, digest/ledger bind, profile sidecar, etc.).
  2. Wire it through FORMAT_NOTES / instruction, solution, reference, calibration if needed, and verifier.
  3. Reshape `tests/test_outputs.py` (thin harness + helpers / new test names / new asserts) so the verifier embedding moves.
  4. Harbor oracle `1.0` / nop `0.0` before push.
- If only one facet is over threshold, keep the green facet stable and move the red one harder; if both are high or near `0.9` after one artifact, add a second cross-artifact invariant (e.g. report digest binding).
- Long-lived PRs can match an earlier delivered/stored shape of the **same** task lineage at ~0.99 after tiny QC retries — treat that like a sibling duplicate and change the comparison surface, not just wording.
- Do not churn empty commits while cosine is red with a real flag; fix the surfaces first so the new commit is structurally different from the prior 3.

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
4. After reusable lessons, update `PROJECT_MEMORY.md` here, commit, and push to `main`.

Notes:

- Cloud Agents do not see unsaved local files or unpushed commits.
- Do not commit individual `dynamo-*` task folders into this instruction repo; those tasks stay in their own forks.
- For GitHub CLI, fork, PR, and check work: use authenticated `gh` with network access; confirm `gh api user --jq .login` before private-repo actions.
- Secrets and env vars for Cloud Agents belong in the Cloud Agents dashboard, not in committed files.
- Optional stronger setup: add this repo plus the task repo in a multi-repo Cloud environment at [cursor.com/dashboard/cloud-agents](https://cursor.com/dashboard/cloud-agents#environments).
- Nested Cloud VMs often need `dockerd --storage-driver=vfs` and may fail Harbor Compose on cgroup v2 threaded mode; use the manual Docker oracle/nop path in `CLOUD_AGENT_DOCKER_HARBOR.md` rather than skipping validation.
- For Docker in **all** chats: use the personal Cloud Environment built from `.cursor/environment.json` + `.cursor/install-docker.sh` in this memory repo. Draft builds are not enough — activate a successful Build in the [Environments dashboard](https://cursor.com/dashboard/cloud-agents#environments) and attach Dynamo repos.
