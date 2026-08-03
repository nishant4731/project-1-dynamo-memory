# Handshake Dynamo Form Filling Guide

Use this guide after a Project Dynamo PR is accepted and the Handshake task-run form needs to be completed.

The goal is to fill the form accurately from the accepted PR evidence, submit each normal step, and stop before any final manual-only action such as screenshot upload, time confirmation, or final formal submission.

## 1. Confirm The Right GitHub User

Before any GitHub CLI lookup, switch to the required GitHub account and verify it.

For Nishant tasks:

```bash
gh auth switch --user nishant4731
gh api user --jq .login
```

The second command must print:

```text
nishant4731
```

If it prints another username, stop and fix GitHub authentication before reading checks, comments, or PR status.

## 2. Collect The Accepted PR Details

Open the accepted PR and collect these values before touching the form:

- Repository name, for example `handshake-project-dynamo/dynamo-28f5ad2-file-and-media-operations`.
- PR URL, for example `https://github.com/handshake-project-dynamo/dynamo-28f5ad2-file-and-media-operations/pull/1`.
- Final accepted commit SHA.
- Accepted state or label.
- Final check status.
- `pass@2` result if present.
- `pass@5` result.
- `avg@5` score.
- Trial breakdown: solved runs, good valid failures, timeouts, verifier issues, infrastructure issues.
- Category and sub-category.
- Artifact types from `task.toml`.
- Task objectives from `task.toml`.

Useful commands:

```bash
gh pr view 1 --repo handshake-project-dynamo/<repo-name> --json url,state,isDraft,labels,headRefName,headRefOid
gh pr checks 1 --repo handshake-project-dynamo/<repo-name>
gh pr view 1 --repo handshake-project-dynamo/<repo-name> --comments
```

For an accepted task, keep the exact evidence text concise. Example:

```text
Accepted commit: 40382028705f596230ab4ed77b56fcdff53c6865
pass@2: 1/2 passed
pass@5: 2/5 passed
avg@5: 0.400
Breakdown: 2 solved, 3 good valid failures, 0 soft-timeout failures
```

## 3. Open The Handshake Form In The User's Chrome Profile

Use Chrome control when the user asks for their signed-in Chrome profile. Claim the existing form tab if one is already open.

If the user names a profile, for example `Nishant`, first list the connected Chrome browser instances and choose the one whose metadata `profileName` matches that name. Do not assume the active or first Chrome extension instance is correct; another profile may be active. For Nishant tasks, the expected Chrome profile is `Nishant`. Confirm profile signals before opening or filling the form:

- Browser metadata shows `profileName: Nishant`.
- Existing Handshake/GitHub/Gmail tabs, if present, belong to Nishant, for example `nishant4731` GitHub pages or `nishantchoudhary4731@gmail.com`.
- The target Handshake task tab, if already open, is claimed from that same `Nishant` profile.

If the connected Chrome profile is wrong, stop before entering data or submitting anything, switch to the named profile, and re-check the profile metadata. Never fill the Handshake form through another user's Chrome profile.

If multiple Handshake task tabs are open, choose the newest or most recent timer tab. Do not fill a stale duplicate tab.

After claiming the tab, inspect the visible page state before clicking anything. Prefer a DOM snapshot for locators and a screenshot when visual layout matters.

## 4. Proposal Step

The first rich text proposal should include:

- Category and sub-category at the top. Do not delete the category/sub-category text already provided by the form.
- Task title.
- PR URL.
- Accepted commit SHA.
- What the task asks the agent to produce.
- Why the task is genuinely difficult.
- Intended solution approach.
- Verification plan.
- Category justification.
- Accepted result summary.

Good accepted-result wording:

```text
The PR is marked accepted. The final pipeline passed static checks, duplicate/similarity review, validation, pass@2, deep review, adversarial review, AVA review, pass@5 trials, and the final gate. The final pass@5 result was 2/5 solved with 3 good valid failures, avg@5 = 0.400, satisfying the difficulty gate.
```

After filling the editor:

1. Click `Save`.
2. Wait for `Changes saved`.
3. Click `Submit`.

## 5. Repository/Core Workflow Step

This step usually asks the contributor to clone the repo, create the task, validate it, and submit a PR.

If the PR is already complete and accepted, submit this step after confirming the PR details are already included in the proposal.

## 6. Artifact Type Step

Select the artifact types that match the task metadata and real outputs.

For the recovered design-sheet task, the correct selections were:

- `Single script or program`
- `Media artifact`
- `Generated output artifact`

Then click `Submit`.

## 7. Task Objective Step

Select the objectives that match what the agent must accomplish.

For the recovered design-sheet task, the correct selections were:

- `Transform`
- `Recover or repair artifact`

Then click `Submit`.

## 8. Screenshot And Pass@ Results Step

This step asks for a screenshot of pass@ results and a text score.

If the screenshot is already attached, fill the text field with the pass@ details and submit. If no screenshot is attached and the user wants to upload it manually, stop and hand control back before submitting.

Use concise text like:

```text
pass@5: 2/5 passed (avg@5 = 0.400). Breakdown: 2 solved, 3 good valid failures, 0 soft-timeout failures.
```

After filling the text:

1. Click `Save`.
2. Wait for `Changes saved`.
3. Click `Submit` only if the screenshot is already attached or the user explicitly authorized continuing.

## 9. Numeric Pass@ Score Step

Handshake may open a separate numeric field after the screenshot/text step.

Read the field constraints before filling:

- If the field is a percentage or decimal score, use `0.400` or `0.4`.
- If the field has a count-like range, for example min `0` and max `8`, use the solved-count value from pass@5.

For the recovered design-sheet task, the field accepted a count-like score, so the value was:

```text
2
```

This matched `pass@5: 2/5 passed`. The text step already preserved `avg@5 = 0.400`.

Then submit the numeric score.

## 10. Stop At Final Manual Confirmation

After the numeric score, the form may show:

```text
Task complete!
Confirm time
```

Stop here unless the user explicitly asks you to confirm time or final-submit on their behalf.

The `Confirm time` button authorizes Handshake to use the session time as the formal work submission for compensation. Treat it as a manual/user-control step.

For Chrome handoff, keep the tab open as a handoff tab so the user can continue in the same live page.

## 11. What To Tell The User At Handoff

Give a short status:

```text
The form is at the final Task complete page with Confirm time visible.

Filled:
- Screenshot/pass@ details: pass@5: 2/5 passed (avg@5 = 0.400)
- Numeric pass@ score: 2

I stopped before Confirm time because that is the formal final submission/compensation confirmation.
```

## 12. Common Mistakes To Avoid

- Do not use the wrong GitHub CLI profile.
- Do not fill a stale duplicate Handshake tab.
- Do not click final confirmation buttons unless explicitly authorized.
- Do not invent pass@ values; copy them from PR checks/comments.
- Do not enter only `0.400` when the numeric field expects a solved-count score.
- Do not upload screenshots unless the user explicitly asks you to upload that file.
- Do not delete the form's category/sub-category starter text.
- Do not rely on visual appearance alone; verify saved state with `Changes saved`.
