# Project 1 Agent Instructions

This workspace keeps persistent project memory in `PROJECT_MEMORY.md`.

Before starting any task in this folder:

- Read `PROJECT_MEMORY.md` first.
- For Project Dynamo or Handshake tasks, also skim the relevant root playbooks:
  - `PROJECT_DYNAMO_LEARNINGS.md`
  - `DYNAMO-PLAYBOOK.md`
  - `FORK_AND_PUSH_GUIDE.md`
  - `PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md`
  - `project_dynamo_reviewer_notes.md`
- Apply the pipeline lessons proactively instead of rediscovering them.

While working:

- When blocked, identify whether the blocker is local setup, GitHub auth, fork/remotes, Harbor validation, static review, pass@, deep review, QC, or task-contract fairness.
- Prefer fixing the underlying pipeline/reviewer issue over changing task logic blindly.
- Treat infrastructure failures, setup failures, provider failures, and all-run timeouts as non-evidence for task difficulty.
- Keep verifier rules, instructions, reference solution, visible data, hidden tests, metadata, and PR evidence aligned.

### Dynamo CI retrigger (hard rule)

- **`review / cosine_similarity` grades the latest commit’s task surface** (instruction / verifier facets). An empty `git commit --allow-empty` makes HEAD a no-op diff and commonly fails cosine / stops the pipeline before `similarity`, validation, and pass@.
- **Never retrigger Dynamo PRs with an empty commit.** Always push a real, defensible change under `task/` (even a small verifier comment, `merge_recipe.md` clarification, or Dockerfile pin) so the tip commit has a non-empty task diff.
- Prefer one meaningful task commit over “content commit + empty redraw.” If a prior empty tip already failed cosine, land a new non-empty `task/` commit and push that.
- Empty commits are also wrong for **tier1** D-findings that require a real file diff (“0 files = fix not attempted”).

After finishing or learning something reusable:

- **Always update memory when you hit a blocker, review failure, or QC finding** — not only at task end. If a PR check fails, a reviewer flags something, or you spend time debugging a recurring pattern, append a dated note before moving on.
- Update `PROJECT_MEMORY.md` with a short dated note under **Dated Notes** (issue → root cause → fix → prevention).
- Add only broad lessons that will help future tasks; keep task-specific noise out unless it explains a recurring blocker.
- If the lesson is Dynamo-specific and detailed, also update `PROJECT_DYNAMO_LEARNINGS.md` or the relevant focused playbook (`DYNAMO-PLAYBOOK.md`, soundness checklist, etc.).

Memory update is part of the task, not optional cleanup. Future agents in this workspace should read `PROJECT_MEMORY.md` first and inherit these lessons instead of rediscovering them.
