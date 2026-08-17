# Project 1 — Claude Code Instructions

**Rule: before starting any task anywhere under this `Project 1` folder (including its task subdirectories), first read the markdown files in this root folder for reference.**

Canonical, maintained list of what to read and when lives in [AGENTS.md](AGENTS.md) — read that file first, then follow its list (currently: `PROJECT_MEMORY.md`, `PROJECT_DYNAMO_LEARNINGS.md`, `DYNAMO-PLAYBOOK.md`, `FORK_AND_PUSH_GUIDE.md`, `PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md`, `project_dynamo_reviewer_notes.md`, `CLOUD_AGENT_DOCKER_HARBOR.md`, plus `HANDSHAKE_DYNAMO_FORM_FILLING_GUIDE.md` for form-filling/submission tasks).

Do not duplicate that list here — if it changes, update AGENTS.md only, so this file and AGENTS.md never drift out of sync.

Apply the lessons in those files proactively instead of rediscovering them. If a listed file is missing, note that briefly and continue with the files that exist.

**Before starting a task:** read `task.toml`'s `[metadata]` category and subcategory, then look for the playbook for that exact pair — `dynamo-<category>-<subcategory>-playbook.md` in the auto-memory directory, and the matching `## <Category> / <Subcategory>` section of `PROJECT_MEMORY.md`. What clears the gates is subcategory-specific; start from that file rather than from first principles.

**On any ALL-GREEN or accepted label:** before moving on, write that playbook down — the mold that worked, the measured pass@2/pass@5 numbers, the crux that actually drew the valid fails, the hurdles gate by gate in the order they blocked, and the levers measured not to work. One file per category+subcategory pair, updated rather than duplicated, plus a section in `PROJECT_MEMORY.md` committed and pushed so Cloud Agents see it. The full required contents live in [AGENTS.md](AGENTS.md) under "Mandatory: on every accepted task, record the playbook by category and subcategory". Do not restate them here.

**On any failed pipeline run:** before editing anything, harvest the full PR feedback — the `pass2_suggestion` "Pass@2 Difficulty Suggestion" sticky (advisory, rate-limited, and often present even when the failure was elsewhere) and the per-trajectory pass@2 / pass@5 trial detail — and write the next commit against that evidence. The procedure, the `gh` commands, and how to weigh a suggestion against the measured trial taxonomy live in [AGENTS.md](AGENTS.md) under "Mandatory: harvest the Pass@2 Difficulty Suggestion and the trial feedback before the next commit". Do not restate it here.
