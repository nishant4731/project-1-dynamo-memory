# Fork And Push Guide

Use this workflow when taking any Project Dynamo task repo, making fixes locally, and pushing them through your fork.

This guide combines the official Project Dynamo docs with the local workflow lesson from prior tasks. The official docs show:

```bash
gh repo fork handshake-project-dynamo/<task-repo> --clone
cd <task-repo>/task
git checkout -b submission
git add -A && git commit -m "Task submission"
git push -u origin submission
gh pr create --repo handshake-project-dynamo/<task-repo> --fill
```

That works because `gh repo fork ... --clone` clones your fork, so `origin` points to `utkarsha01/<task-repo>`. If you instead cloned the upstream repo directly, `origin` points to `handshake-project-dynamo/<task-repo>` and `git push origin ...` will fail with `403`. In that case, add a separate fork remote and push there.

## 1. Start From The Right Repo

Preferred official flow for a fresh task:

```bash
gh repo fork handshake-project-dynamo/<task-repo> --clone
cd <task-repo>
```

With this flow, `origin` should point to the fork:

```text
origin  https://github.com/utkarsha01/<task-repo>.git
```

Alternate flow when you already cloned the upstream task repo:

```bash
git clone https://github.com/handshake-project-dynamo/<task-repo>.git
cd <task-repo>
```

Check where you are:

```bash
git remote -v
git status --short
git branch --show-current
```

For an upstream clone, keep `origin` pointed at the upstream repo. Push changes to your own fork remote, not directly to `origin`.

## 2. Use The Correct GitHub Account

Check active GitHub CLI accounts:

```bash
gh auth status
```

Switch to the intended account, for example Utkarsha:

```bash
gh auth switch --user utkarsha01
gh api user --jq .login
```

The second command should print:

```text
utkarsha01
```

If it prints another user, stop and fix GitHub CLI auth before pushing.

## 3. Create Or Connect The Fork

If the fork does not exist yet and policy/tooling allows it:

```bash
gh repo fork handshake-project-dynamo/<task-repo> --clone=false
```

If the fork already exists, or after creating it, add the fork as a separate remote for an upstream clone:

```bash
git remote add fork https://github.com/utkarsha01/<task-repo>.git
```

If the repo was cloned with the official `gh repo fork ... --clone` flow, you usually do not need a `fork` remote: `origin` is already the fork. Keep an `upstream` remote for the Handshake repo if you need to fetch the latest base:

```bash
git remote add upstream https://github.com/handshake-project-dynamo/<task-repo>.git
```

If `fork` already exists, verify it:

```bash
git remote -v
```

Expected shape:

```text
origin  https://github.com/handshake-project-dynamo/<task-repo>.git
fork    https://github.com/utkarsha01/<task-repo>.git
```

Official-clone expected shape:

```text
origin    https://github.com/utkarsha01/<task-repo>.git
upstream  https://github.com/handshake-project-dynamo/<task-repo>.git
```

## 4. Create A Working Branch

Start from the latest upstream base when using an upstream clone:

```bash
git fetch origin
git checkout -b codex/<short-task-name> origin/main
```

For an official fork clone with `upstream` configured, use:

```bash
git fetch upstream
git checkout -b submission upstream/main
```

If the repo uses another default branch, replace `origin/main` or `upstream/main` with that branch.

## 5. Before Editing

Read the task files first:

```bash
rg --files -g '*.md'
sed -n '1,240p' task/instruction.md
sed -n '1,220p' task/task.toml
```

For Dynamo tasks, also inspect:

```bash
find task -maxdepth 4 -type f | sort
sed -n '1,260p' task/tests/test_outputs.py
sed -n '1,260p' task/solution/solve.py
```

Keep in mind:

- Fix the actual pipeline or reviewer issue, not a guessed issue.
- Do not create hidden-only arbitrary rules. If the verifier requires a key, schema, ordering rule, tolerance, or edge case, make it discoverable from `instruction.md` or visible fixtures.
- Difficulty should come from real reasoning: scalable algorithms, exact transformations, robust parsing, edge cases, and independent verifier coverage.
- Do not leak final answers into agent-visible files.
- Keep the oracle and verifier aligned, but do not make the verifier import the oracle.
- Avoid unrelated refactors. Reviewers penalize drift and manufactured complexity.

## 6. Make And Verify Changes

After editing, run the fastest checks first:

```bash
git diff --check
python3 -m py_compile task/solution/solve.py task/tests/test_outputs.py
bash references/check-base-image.sh task
```

When Docker is running, run:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```

Expected result:

- Oracle gets reward `1.0`.
- Nop gets reward `0.0` or less than full reward.

On Cursor Cloud Agent VMs, follow `CLOUD_AGENT_DOCKER_HARBOR.md` first:

- Install `docker.io` + `docker-compose-v2`, start `dockerd` with `storage-driver: vfs`.
- If Harbor Compose fails with cgroup v2 `threaded mode`, do not treat that as a task bug.
- Use the manual `docker run --privileged --cgroupns=host` oracle/nop fallback from that guide, with `/tests` mounted read-write.
- Still prefer real Harbor when it works; remote Dynamo CI remains authoritative.

If Docker is not running and cannot be started, record that limitation and run direct local checks where possible, but rely on the remote pipeline for full container validation.

## 7. Commit Cleanly

Check exactly what changed:

```bash
git status --short
git diff --stat
git diff
```

Stage only intended files:

```bash
git add <file-or-directory>
```

Commit:

```bash
git commit -m "Short clear message"
```

If commit author matters, set it before committing:

```bash
git config user.name "Utkarsha"
git config user.email "<verified-github-email>"
```

GitHub push authentication and git commit author are separate things. Confirm both when the reviewer or owner cares.

## 8. Push To The Fork

Confirm the active GitHub account again:

```bash
gh api user --jq .login
```

Push the branch to the fork.

If `origin` is your fork, use the official docs command:

```bash
git push -u origin <branch-name>
```

If `origin` is upstream and `fork` is your fork remote, use:

```bash
git push fork <branch-name>
```

For this repo pattern:

```bash
git push fork codex/recover-audio-masters
```

## 9. Open Or Update The PR

If no PR exists:

```bash
gh pr create \
  --repo handshake-project-dynamo/<task-repo> \
  --head utkarsha01:<branch-name> \
  --base main \
  --title "<clear PR title>" \
  --body "<summary and validation>"
```

The official docs also allow the shorter form when your current branch is pushed to your fork and tracking is set:

```bash
gh pr create --repo handshake-project-dynamo/<task-repo> --fill
```

If a PR already exists, pushing to the same fork branch updates it automatically.

Confirm the PR head:

```bash
gh pr view <pr-number> \
  --repo handshake-project-dynamo/<task-repo> \
  --json headRefOid,url,statusCheckRollup
```

You can also confirm from git:

```bash
git ls-remote origin refs/pull/<pr-number>/head
```

## 10. Watch The Pipeline

Use:

```bash
gh pr checks <pr-number> \
  --repo handshake-project-dynamo/<task-repo>
```

When multiple GitHub accounts are cached, prefix each private-repo poll with the intended account
switch in the same serial command. Do not parallelize `gh auth switch` plus PR polls across
accounts because the active account is shared state.

```bash
gh auth switch --hostname github.com --user utkarsha01 && \
  gh pr checks <pr-number> --repo handshake-project-dynamo/<task-repo>
```

For detailed JSON:

```bash
gh pr checks <pr-number> \
  --repo handshake-project-dynamo/<task-repo> \
  --json name,state,bucket,link,startedAt,completedAt,workflow
```

If a check fails:

```bash
gh pr view <pr-number> \
  --repo handshake-project-dynamo/<task-repo> \
  --json comments,statusCheckRollup,headRefOid
```

Read the latest comments for the current head commit. Ignore stale comments from older commits unless they still apply.

## 11. Dynamo-Specific Review Checklist

Before pushing a Dynamo task fix, verify:

- `instruction.md` is concise and uses absolute required paths.
- Expected output files are documented.
- Hidden tests do not depend on undisclosed schemas or arbitrary constants.
- Visible fixtures witness unusual schemas or the instruction names them explicitly.
- Tests independently derive expected outputs from inputs.
- The oracle is a real reusable solution, not hardcoded output.
- The no-op agent fails.
- Any pass@ failure is a valid failure, not caused by an ambiguity or verifier bug.
- Difficulty is defensible to a reviewer as realistic expert work.

## 12. Common Mistakes To Avoid

- Pushing to `origin` instead of `fork`.
- Using the wrong active GitHub CLI account.
- Assuming commit author equals push account.
- Fixing an old PR comment without checking the latest head commit.
- Making the task harder by hiding information.
- Adding files that are not used by instruction, solution, tests, or fixtures.
- Leaving generated output, caches, or local `jobs/` directories in the commit.
- Skipping `git diff --check`.
- Forgetting to rerun or recheck the PR pipeline after push.
