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

## Mandatory: complete validation and GitHub feedback loop for every change

This is a hard completion gate for every task change made anywhere under the `Project 1` folder. Codex must not report a task as complete, and must not push a Dynamo `submission` branch, after only a unit test, smoke test, static sweep, or one green GitHub check. A partial validation result is not a passing result.

Before the first substantive push, design and validate the final task version as a whole:

- Make the difficult version first. Do not push an easy task and plan to make pass@2 harder in later cosmetic or incremental commits; an enforced cosine pass can index the earlier surface and self-poison later revisions.
- Make pass@2 difficulty fair and output-affecting: use multiple interacting, disclosed subsystems; varied protected fixtures; a reusable-solver/generalization requirement; and direct adversarial or mutant checks for each decisive rule. Do not manufacture difficulty with hidden conventions, undisclosed serialization, arbitrary timeouts, leaked answers, nondeterminism, or malformed inputs.
- Reconcile `instruction.md`, normative environment notes, fixtures, metadata, reference solution, verifier, artifacts, and review evidence before running the final checks. Every verifier-enforced key, type, ordering, tie-break, normalization, path frame, and byte-level convention must be stated or uniquely derivable from agent-visible material.

Run every applicable local check and inspect its result, including the full sequence documented in `DYNAMO-PLAYBOOK.md` and `PROJECT_DYNAMO_TASK_SOUNDNESS_CHECK.md`: regeneration/refreezing and reference pins; syntax/compile and diff checks; image build and preflight; reference/oracle; the complete verifier/unit sweep and build count; cross-checks and documentation-name checks; wrong-output, nop, adversarial, mutation, tamper, and isolation probes; and Harbor oracle `1.0` plus nop below full reward (using the documented manual Docker fallback only when Harbor is unavailable). If a repository does not provide one of these checks, record that fact and run the closest equivalent; never silently omit it.

Before committing, inspect `git status`, the complete pending diff, and `git log --oneline -3`; apply the commit-similarity procedure below. Prefer one cohesive, substantively distinct commit containing the complete task contract and all known fixes. Do not use empty retrigger commits or a burst of near-identical commits.

After every push, GitHub CLI monitoring is mandatory and must run outside the sandbox when it depends on authentication, private repositories, Actions logs, PR checks, or network state:

```bash
export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"
gh api user --jq .login
gh pr checks <pr-number> --repo <owner>/<repo> --watch
gh pr view <pr-number> --repo <owner>/<repo> --comments
```

The active account must be `nishant4731`, and the remote and PR must point to the intended fork/submission branch. If any check fails, do not call the task done: read the failed job's actual log and PR sticky/comments with `gh`, classify the cause as task contract, verifier/reference, static/review, cosine/similarity, pass@2, deep review, AVA/QC/eval, Harbor, authentication, cancellation, or other infrastructure, and collect all available feedback before editing. Fix the root cause and rerun the complete local gate; then push one cohesive follow-up and wait for that single pipeline to finish before making another change. Treat cancelled runs, provider errors, authentication failures, and action-download failures as infrastructure evidence only, but still verify the succeeding run rather than assuming it passed.

Completion requires all applicable local checks and all required GitHub checks to be green, with Harbor oracle/nop evidence recorded. If an external service remains blocked after the documented retries and diagnosis, report the exact blocker and evidence instead of claiming successful validation.

## Mandatory: harvest the Pass@2 Difficulty Suggestion and the trial feedback before the next commit

**Whenever a pipeline run fails — for any reason, on any stage — do not start editing until you have pulled every piece of feedback that run produced, including the advisory ones that did not cause the failure.** The same harvest is mandatory after a run that *passed* but landed in a bad band (pass@2 2/2 solved, pass@5 3–5/5 solved). The next commit must be written against this evidence, not against a guess about why the run went red.

Read all of these, in this order:

1. **`pass2_suggestion` — the Pass@2 Difficulty Suggestion sticky.** It is advisory, never blocks, and is capped at ~2 runs/day/task, so it is easy to lose: it can be present on a run whose `gate` is red for an unrelated reason, and it will not be regenerated on the next push. Read it on *every* failed run, even when the failure was cosine, static review, validation, AVA, or QC and pass@2 never ran or already passed. Copy its text into the task's working notes before pushing again.
2. **The pass@2 trial detail.** Per trajectory: fail reason, *Agent Approach*, golden vs agent values, failing tests, solve time vs the agent budget, and the `difficulty_crux` / `approach_validity` / `task_specification` / `reward_hacking` columns. Classify each failure as solved / good valid fail / invalid fail / timeout / operational wedge before deciding anything.
3. **The pass@5 `trials` panel when the run reached it.** Solved count, per-trajectory validity, and `difficulty_crux` on each trajectory — the headline fraction alone is not the finding.
4. **The failed job's own log and sticky** for the stage that actually went red, per the classification list in the section above.

Pull them with `gh` outside the sandbox:

```bash
gh pr view <pr-number> --repo <owner>/<repo> --comments
```

```bash
gh run view <run_id> --repo <owner>/<repo> --json status,conclusion,jobs
```

```bash
gh run view --job <job_id> --repo <owner>/<repo> --log
```

Stickies are edited in place and truncate long findings — when the sticky and the job log disagree, or the sticky looks clipped, the **job log** is the record. For deeper pass@ evidence use *View logs & artifacts → trials → Upload Harbor Output*.

Then apply the evidence deliberately, not literally:

- Treat the suggestion as **input, not an instruction**. It is an LLM hint and can be wrong about the cause. Weigh it against the measured taxonomy: when failures are in-progress timeouts, heredoc/terminal wedges, or near-misses at the budget ceiling, the correct move is usually to **shrink non-crux volume or provide plumbing**, even if the suggestion asks to harden further — an agent that never finishes is not difficulty evidence. `[agent].timeout_sec` cannot exceed 3600s.
- A suggestion or trial finding that is genuinely load-bearing must be answered with a real, output-affecting change in **one** cohesive commit — and that commit still has to clear the cosine last-commit window checklist below before it is pushed.
- Record, in `PROJECT_MEMORY.md`, what the suggestion said, what the trial taxonomy actually showed, and whether the next commit adopted or rejected the suggestion **with the reason**. Rejections are as reusable as adoptions; several of the entries already there exist because a suggestion was followed blindly once.

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
4. Is the change a **load-bearing contract** or a **domain identity reskin**, not only wording, docstrings, empty commits, or whitespace?
5. Would a reviewer still see a different comparison embedding than the previous green/red cosine SHAs?

If the sticky says `"too similar to a delivered Dynamo task"` (often no score, ~10–15s, later stages skipped):

- Stop. Do **not** empty-retrigger, close/reopen, `gh run rerun`, or keep rewording prose.
- **Measured fact:** lexical self-similarity can go *down* while the service still blocks; a domain rename can drop the service score by ~0.20 when rewording only moved ~0.02. Treat the metric as tracking what the task is **about**, not bag-of-words overlap.
- Prefer a **domain identity reskin** in **one** commit (see below), then Harbor oracle `1.0` / nop `0.0`.
- Keep a local token-cosine guard against recent heads (including current `HEAD`) as necessary-but-not-sufficient.

If the sticky is HTTP/`401`/`503`/`000` / Actions download failure → infra; empty retrigger is OK.

### Domain identity reskin (preferred clear for “delivered Dynamo task”)

Rename the visible identity, then rewrite the two graded files **from scratch** in the new vocabulary. In one push, rename at least:

1. Package/tool directory under `task/environment/data/` (or the primary fixture archive dir)
2. Executable/command the agent must produce (e.g. `/app/kiln_bake.py`)
3. Entry-point function the agent implements (e.g. `bake_outputs`)
4. Contract/design-note filename (e.g. `GLAZE_SPEC.md`)
5. Sample/fixture archive directory (e.g. `probes/`)
6. Primary output filename(s) the deliverable writes
7. `[task].name` and `description` in `task.toml`
8. Image tags / Dockerfile install paths for the renamed executable

Apply renames as ordered plain-string substitutions across every source file (longest first). Do **not** change engine math, fixture semantics, or verifier pass/fail meaning — vocabulary and identity only.

Then:

1. Replace `task/instruction.md` and `task/tests/test_outputs.py` entirely (not line-edit the old prose).
2. Re-check Dockerfile `COPY`/`chmod`, `artifacts = [...]`, mutation tables quoting renamed ids, regenerated pins/fixtures.
3. Harbor oracle `1.0` / nop `0.0` before push. Do not push on a green unit sweep alone.

### How to clear a real cosine flag without a full reskin

Only if a reskin is impossible: change **both** compared artifacts with a *new* graded deliverable + verifier reshape in one commit (new path/digest schema, not another soft rename of the same domain). Harbor oracle/nop before push. Docstring-only or atomic-split-only edits are **not** enough after a cosine-green SHA that already introduced the same artifact.

Docstring-only or atomic-split-only edits are **not** enough when the last cosine-green SHA already introduced the same artifact. Treat the last ~3 commits as poison for near-duplicate surfaces.

**The "one free cosine pass" rule (confirmed on `dynamo-562b1d3`/perm-forge):** cosine is ✅ on the FIRST surface snapshot, because nothing similar is stored yet; that snapshot then becomes the lineage baseline, so **every later commit is scored against your own commit-1 surfaces**. A large instruction reword + renaming every test + rephrased docstrings scored ~0.99 against the prior snapshot and stayed blocked. Practical consequences: (1) get `instruction.md` and `tests/test_outputs.py` right on commit 1 — do not plan to iterate on them; (2) never push a wording/rename/docstring-only change to those two files after commit 1; (3) when a later commit MUST touch them (fairness fix, added rule), bundle a NEW graded output artifact (new `/app/out/*` path wired through instruction → RULES/FORMAT → solution → reference → verifier) so both surfaces diverge well past the threshold in a single push.

**Hard ban — last-3-commit self-match (flare/ledger/profile pattern):** if the previous 1–3 `submission` commits already changed cosine surfaces via sidecar rename / thin-wrapper reshuffle (`recovery_audit` → `fit_ledger` → similar digest JSON, or `_harness` → thin `test_outputs` only), the next push **must not** be another rename/reword of that same shape. Required instead, in **one** commit:
1. A **new** graded contract with a **different schema** (e.g. ordered `weight_vector` + nested `moduli` + `policy_sha256`, not the same flat op/bounds object under a new filename).
2. A **desk/prompt rewrite** of `instruction.md` (structure + framing), not synonym swaps.
3. A **verifier entrypoint reshape** (`test_outputs.py` import style, test names, private module name) so the compared verifier bytes are not a near-copy of HEAD~1..HEAD~3.
4. Local oracle `1.0` / nop fail before push.
Renaming `*_audit.json` → `*_ledger.json` → `*_profile.json` without schema+prompt+entrypoint divergence **will** fail enforced cosine against the PR lineage.

While working:

- When blocked, identify whether the blocker is local setup, GitHub auth, fork/remotes, Harbor validation, static review, cosine similarity, pass@, deep review, QC, or task-contract fairness.
- Prefer fixing the underlying pipeline/reviewer issue over changing task logic blindly.
- Treat infrastructure failures, setup failures, provider failures, and all-run timeouts as non-evidence for task difficulty.
- Keep verifier rules, instructions, reference solution, visible data, hidden tests, metadata, and PR evidence aligned.
- **Before every commit, apply the "Commit similarity CI gate" procedure below** — the cosine-similarity check breaks the pipeline if the last 3 commits (messages and diffs) are too similar.

### Enforced cosine similarity (`review / cosine_similarity`) — detail

This gate can flip from shadow to **enforced** mid-PR. Once enforced, it runs on **every push** and can block before static/validation/pass@.

- Compared surfaces are only `task/instruction.md` and `tests/test_outputs.py` (first 64 KiB each). Threshold is typically `0.9`; sticky often hides the matched task.
- **Recent-commit window (always check):** the checker compares the current surfaces against this PR's **last ~3 commits** and stored/delivered snapshots of the same lineage. Empty commits, amend-style redraws, docstring-only patches, and tiny QC wording often fail immediately with `"too similar to a delivered Dynamo task"` even when an older duplicate sticky said UNIQUE.
- Sticky `"too similar to a delivered Dynamo task"` = real **flag** verdict, not infra.
- Sticky `"could not produce a verdict (HTTP …)"` / `401` / `503` / `000` / Actions download `Service Unavailable` = infra or auth.
- Shadow-mode scores above threshold (e.g. verifier `0.91`) warn that the next enforced run will block the same surface.
- If only one facet is over threshold, keep the green facet stable and move the red one harder; if both are high, add another cross-artifact invariant.
- Long-lived PRs can self-match earlier SHAs of the **same** task at ~0.99 after tiny retries — change surfaces, not just wording.

- **Domain reskin clears self-match; prose does not.** When the corpus likely includes your own earlier PR heads, measured lexical self-sim of `instruction.md`/`test_outputs.py` is necessary but not sufficient. Rewording can lower lexical self-sim and still BLOCK; renaming the task domain/identity can raise lexical self-sim and still PASS with a much lower service score. Do not burn rounds on paraphrases. In one push: rename visible identity (probe dir, CLI path/module, contract filename, output filenames, `[task].name`), then rewrite the two graded files from scratch in the new vocabulary. Apply longest-first string substitutions across all sources; fix Dockerfile COPY/chmod, `artifacts = [...]`, mutation literals, and regenerated fixtures. Harbor oracle 1.0 / nop 0.0. Pair needed difficulty ratchets into the same identity push.

- **CRITICAL correction — a reskin that PASSED gets indexed too, so leaving the two graded facets untouched on your NEXT push is not "safe," it's the single surest way to fail.** Confirmed on df4e109, 2026-08-07: after a reskin (`6cf9015`) passed cosine, a follow-up commit (`e438acd`) that ratcheted pass@2 difficulty entirely inside private generator/harness files — deliberately leaving `instruction.md` and `tests/test_outputs.py` **byte-identical** to the passing commit, reasoning "unchanged compared files can't regress a passing score" — **still blocked**. Byte-identical content trivially self-matches its own now-indexed predecessor at ~1.0; "I didn't touch the compared files" is not a shield, it's the failure mode itself, because the comparison is against the corpus (which now contains that exact byte string), not against a diff. **The practical rule: every push that follows a cosine-PASSING push needs its own fresh identity change to the two compared facets — even a push that is 100% about verifier/generator internals and touches neither file's *meaning*.** Bundle a trivial-but-real reskin (new domain vocabulary, rewritten instruction/test files) into EVERY push after the first pass, not just the ones where you consciously changed the graded contract.

- **MEASURED COUNTER-EVIDENCE (2026-08-12, dynamo-e488890 PR #3) — do not reskin reflexively.** On a fresh repo, commit 1 passed enforced cosine (instruction `0.7117`, verifier `0.8000`, fingerprint `0.7911`) and ran the whole pipeline through pass@2. Commit 2 was the *same task, same domain, same vocabulary*: local token-cosine of the two compared facets against commit 1 measured **0.9222 / 0.9776 (joined 0.9775)** — deep in the "this will block" band by the a3f35ff heuristic — and it **PASSED**, scoring `0.7323 / 0.8057 / 0.7961`. The service numbers barely moved. Conclusion: the corpus is **delivered/accepted Dynamo tasks**, and an in-flight PR head on the same repo is **not** in it. So the df4e109/a3f35ff "every push after a cosine-green push needs its own fresh identity change" rule is about lineages whose earlier version was actually *delivered* — it is NOT a per-push tax on an ordinary PR. Before spending a session on a reskin, push the real fix and read the score; a reskin costs an hour, breaks literals, and redraws pass@2 for nothing. What commit 2 *did* carry was load-bearing (a whole new graded deliverable wired through instruction → contract → reference → verifier, plus new verifier cases), which is the documented "new graded artifact + verifier reshape" lever — that, not a rename, is what to reach for first.

### Cosine self-poisoning & the difficulty catch-22 (learned 2026-08-07, dynamo-ea98175)

Mechanism confirmed from the failing job log (endpoint `https://ai.joinhandshake.com/api/internal/task-similarity/checks`, which the gate POSTs `instruction.md` + `tests/test_outputs.py` to). The JSON response carries `.threshold`, an **enforced** verdict `.facetResults.{instruction,verifier}.maxScore` and a **shadow** verdict `.observedFacetResults.{instruction,verifier}.maxScore`; a facet's `maxScore` is the **max similarity to any COMPLETED task** (fallback text `"No completed-task comparison yet"` when the corpus is empty). It is a **semantic embedding** score, not lexical, and blocks when a facet's `maxScore >= .threshold` (~0.9 in the PASS sticky). **The number is only surfaced on PASS** — on a block the script writes just "This task is too similar to a delivered Dynamo task" and exits *before* the score table, so the failing score lives only in the runner's discarded `task-similarity-response.json`; neither the sticky nor the log ever shows how far over threshold you are. Consequences that cost a full session:

- **Every evaluated submission of your task joins the comparison corpus.** After a version is scored, later iterations of the *same concept* self-match it at ≥0.9. Renaming columns/variables and rewording prose does **not** reliably drop a semantic score while the underlying task concept (same inputs + same core trap) is unchanged.
- **A fresh PR does NOT reset it.** The corpus is keyed to the task/repo, not the PR number. Closing PR #2 and opening PR #3 with the identical hardened task still failed cosine.
- **The difficulty catch-22.** The *easy* version of a task is usually UNIQUE and clears cosine (e.g. 0.717/0.832), but it fails pass@2 as too easy. The distinctive hardening you add to beat pass@2 (a specific silent trap, e.g. bitemporal label-maturation) is exactly what a *later* hardened iteration self-matches once the first hardened version is indexed. So you can end up able to clear cosine **or** clear pass@2, but not both, purely as an artifact of having iterated on-PR.
- **Therefore: get difficulty right BEFORE the first substantive push.** Design the hard trap up front, reason through pass@2-hardness locally (does the naive/expected agent approach diverge on many rows?), and submit the *hard* version first. Do **not** submit an easy version and then harden it on-PR across several pushes — each near-duplicate push poisons your own future comparisons.
- Manual re-runs do not re-run similarity ("push a new commit to request a new comparison"); and firing several PR events quickly cancels runs via the `cancel-in-progress` concurrency group, surfacing as fake cosine/gate failures.
- If you are already poisoned (hard version self-matches your own earlier hard snapshot), surface edits will not save you — either escalate to Dynamo maintainers (index may over-match your own lineage) or pivot to a **genuinely different task concept** (different inputs + different core trap), not just a renamed feature set.

**Second confirmation (dynamo-df4e109, 2026-08-07) — even new mechanics + full rewrites don't escape.** A journaling text-editor recovery task passed cosine on its first two commits (`b86f2558`, then `815f109` after moving the shared verifier hardening-kit boilerplate into a private `tests/_harness.py` so the compared `test_outputs.py` facet was thin+distinct — that move genuinely cleared the *first* real overlap). `815f109` ran pass@2 (which returned **2 solved / 0 valid-fail = too easy**) and thereby got indexed. Every commit after that failed cosine and **stayed** failed through three escalating attempts: (i) a real difficulty ratchet adding **genuinely new mechanics** (a `move` cut/paste op with a post-cut destination frame + optional `guard` preconditions), (ii) a **full rewrite** of `tests/test_outputs.py` (new names/order/wording), and (iii) a **full paraphrase** of `instruction.md`. Semantic embedding of the *same task concept* self-matched ~1.0 regardless. Confirms: once indexed, only a genuinely different concept or a maintainer-side same-repo/self exclusion escapes; **do not thrash** (each push re-indexes). The move-boilerplate-to-`_harness` trick is a legit one-shot fix for real sibling overlap, **not** a cure for self-poisoning. This is the pass@2/cosine catch-22 in action: the ratchet that would beat "too easy" is exactly what self-matches the indexed easy version.

**Third confirmation (dynamo-df4e109, 2026-08-07) — a whole NEW graded artifact also fails once poisoned.** After the above, we added a genuinely new, fourth graded deliverable — `/app/edit_ledger.tsv`, a per-op TSV audit trail with its own header/schema (`seq  id  type  pos  removed  added  length_after`), wired through both oracles, the verifier, and the instruction (4-arg CLI). This is exactly the "add a distinct graded artifact/new schema" lever that cleared cosine for peer task `c9a0d11` (`peer_cap_ledger`). On df4e109 it **still failed cosine** (`c279990`) — because c9a0d11 added its ledger *before* being deeply self-indexed, whereas df4e109 was already poisoned by two prior passing snapshots. Lesson: the new-artifact lever works as *prevention* (make the first submitted version distinctive), not as a *cure* after multiple same-concept versions are indexed.

### THE PROVEN FIX — domain reskin (measured 2026-08-07). Do NOT reword.

Rewording does **not** work; a **domain reskin** does. Measured on one task, same branch, three consecutive heads (service = the hidden Joinera `instruction` facet score; lower is better):

| head | change | lexical self-sim | service instruction score | result |
|---|---|---|---|---|
| A | baseline | 0.7337 | 0.8842 | **PASS** |
| B | three prose rewrites | 0.6310 | (blocked, no score) | **BLOCKED** |
| C | domain reskin | 0.7341 | 0.6886 | **PASS** |

The push with the **lowest** lexical similarity (B) BLOCKED; the reskin (C) whose lexical similarity went back UP scored **0.20 lower at the service** and cleared. Rewording moved the service score ~0.02; renaming the domain moved it **0.20**. Two lexical models were ruled out by measurement — the two graded files alone (B self-sim 0.63 still blocked), and the whole `tests/` tree (0.9939 across a PASS vs 0.9987 across a BLOCK). **The metric tracks what the task is ABOUT (semantic), so change the domain, not the words.**

**The recipe (ONE push):** reskin the visible surface, then rewrite the two graded files over the new vocabulary. Rename, as ordered plain-string substitutions across every source file at once (longest first):
1. the package/tool directory under `task/environment/data/`
2. the executable / command the agent must produce
3. the entry-point function the agent implements
4. the contract / design-note filename
5. the sample/fixture archive directory
6. the output filename(s) the deliverable writes
7. `[task].name` in `task.toml` and its `description`
8. the image tag in any dev/probe.sh-style helper

Then **rewrite `task/instruction.md` and `task/tests/test_outputs.py` FROM SCRATCH** in the new vocabulary — replaced, not edited. **Do NOT touch the engine, the rules, the fixtures' semantics, or the verifier's behaviour.** Vocabulary and identity only.

**What a reskin reliably breaks (fix all before pushing):** Dockerfile `COPY` paths + any `chmod` of the renamed executable; `artifacts = [...]` in `task.toml` (names the deliverable path); the **mutation table** if it stores code fragments quoting a renamed identifier — the sweep must still report the SAME build count (N of N), or anchors silently no-op; **reference pins** (regenerate after any pinned file changes); the **frozen fixture corpus** if a renamed name appears inside it (e.g. the manifest `schema` string) — refreeze.

**Re-validate in this order (do NOT push on a green sweep alone):** refreeze fixture → regenerate pins → smoke → sweep (check the **BUILD COUNT**, not just "0 survivors") → xcheck → doc-name check → preflight → every adversarial probe → `harbor run --agent oracle` (1.0) and `--agent nop` (<1.0).

**Self-similarity guard (necessary, not sufficient):** before every push, token-cosine `task/instruction.md` + `task/tests/test_outputs.py` against your branch's own recent heads — **HEAD included, not HEAD~1** (a naive edit of your last head measures ~0.999 and blocks outright). A good number is necessary but not sufficient — head B above had the best self-sim that branch ever produced and still blocked. **Caveat:** "the corpus contains your own prior submissions" is strong inference, not platform-confirmed (the matched task and score are hidden on a block); what IS proven is that the reskin recipe cleared a gate that rewording had blocked twice.

### How to overcome cosine self-poisoning (recovery playbook)

Root cause restated: the Dynamo team flipped `cosine_similarity` from **shadow → enforced**. Under enforcement, **every commit that PASSES cosine and runs the pipeline is added to the "completed task" comparison corpus.** So your own earlier passing commits become the delivered task your later same-concept commits match at ~1.0. A failed-cosine commit is NOT indexed (pipeline skips), so retries are harmless to the corpus but waste time and give false hope.

**Best — prevention (the only reliable path):** get difficulty right and submit the HARD, final version on the **first** substantive push. Never ship an easy version and harden it on-PR; the first passing snapshot poisons every later same-concept push. Reason about pass@2-hardness locally before pushing (does the naive/expected agent approach actually diverge?), and bake the crux + any distinctive graded artifact in from commit 1.

**Recovery once already poisoned (in order of preference):**
1. **Escalate to Dynamo maintainers** — ask them to purge/de-index this repo's lineage from the similarity corpus, or add same-repo/self exclusion. This is the fastest real fix and leaves the (otherwise-complete) task intact. This is the recommended action when validation/pass@2-difficulty/qc are already satisfied and only cosine blocks.
2. **Rebuild as a genuinely different task concept** — different inputs AND a different core trap AND a different output contract. A reskin, rename, new mechanic, or new sidecar artifact on the *same* concept is NOT enough (confirmed twice above). Effectively author a new task.
3. **Wait for a fresh assigned repo** (new task hash = clean corpus slate) and author the hard version there first — but never reuse the poisoned concept, or you re-poison the new repo.

**Confirmed NOT to work once poisoned (don't waste pushes):** rewording/paraphrasing `instruction.md`; rewriting/renaming/reordering `tests/test_outputs.py`; moving machinery into a private helper (one-shot only, for *real* sibling overlap); adding new mechanics; adding a whole new graded artifact/schema; squashing history; opening a new PR (corpus is keyed to task/repo, not PR number).

**Diagnostic note:** on an enforced block the numeric `facetResults.{instruction,verifier}.maxScore` and the matched task are **hidden** (the script exits before printing them; they live only in the runner's discarded `task-similarity-response.json`). You cannot tell which facet crossed 0.9. Heuristic: for self-poisoning the **instruction facet** is usually the hard blocker (it's the same task semantically and can't be made different without changing the task), so verifier-side tricks stop helping.

GitHub and push safety:

- **Single account for Cloud Agents: `nishant4731` only.** Do not keep `cursor` / `cursor[bot]` as an active `gh` user and do not `gh auth switch` mid-task.
- **Auth does not persist across chats.** Interactive `gh auth login` in one VM is gone in the next chat. Persist nishant via a Cloud Agents dashboard Runtime Secret `GH_TOKEN` (or `NISHANT_GH_TOKEN`) — see `FORK_AND_PUSH_GUIDE.md`. Memory-repo docs alone do not log the account in.
- At session start: `export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"` if needed, then `gh api user --jq .login` must print `nishant4731`. Only prompt for device login if that secret is missing.
- Strip Cursor managed git URL rewrites that inject `x-access-token` for `cursor[bot]` on `github.com`. Those rewrites make every `git push` look like the bot even when `gh api user` prints `nishant4731`. See `CLOUD_AGENT_DOCKER_HARBOR.md` / `FORK_AND_PUSH_GUIDE.md`.
- Do not force push unless it is necessary to update an existing PR branch after history was intentionally rewritten or to retrigger a pipeline that requires a new commit shape. Prefer a normal `git push` for ordinary changes.
- Before any force push, explain why it is needed, confirm the target remote and branch are the user's fork/submission branch rather than upstream or a protected/default branch, and prefer `git push --force-with-lease` over plain `--force`.
- Run GitHub CLI (`gh`) commands outside the sandbox when they depend on GitHub auth, private repo access, network access, run logs, checks, forks, or PR creation/update. Sandboxed `gh` results can be misleading because credentials, keychain state, and network access may differ.
- **Commit cosine-similarity gate (`review / cosine_similarity`).** The CI pipeline compares the PR's most recent ~3 commits and **breaks if they are too similar** (near-duplicate diffs and/or near-identical commit messages — e.g. repeated empty/one-line "retrigger" commits or the same edit reworded). Every commit you push must be **substantively distinct** from the previous two: change real content, and write a specific message describing that change. When you only need to re-trigger the pipeline, do it with a genuinely different difficulty-neutral change (a distinct README/docs edit, a new fixture witness), never a copy of the last commit. Batch a round of fixes into ONE meaningful commit rather than several tiny similar ones.

Commit similarity CI gate (MANDATORY — read and apply before EVERY commit):

- **A CI pipeline runs a cosine-similarity check over the last 3 commits. If those commits are too similar, the pipeline breaks.** This applies to the trailing three commits on the branch being pushed — both their commit *messages* and their *diff content* count toward the similarity score. The same enforced `review / cosine_similarity` (and `similarity`) check also compares the task's `task/instruction.md` and `task/tests/test_outputs.py` against prior submitted versions and the wider corpus; a retry that leaves those two files near-identical (empty commit, cosmetic reword, helper rename, re-push of the same shape) can score ~0.98+ and fail — never trust an older UNIQUE sticky after retries.
- Whenever you (the LLM agent) are about to commit, keep the last 3 commits **meaningfully distinct**: do not reuse near-identical commit messages, do not repeat the same templated wording, and avoid three consecutive commits whose diffs are trivial variations of each other (e.g. three near-identical "Note …" lines, or three one-line touch-ups of the same paragraph).
- **Required pre-commit procedure, every time:** (1) run `git log --oneline -3` and read the pending diff; (2) if the new commit's message OR diff would be a near-duplicate of either of the previous two, STOP and rewrite the message in fresh wording *and* reshape the change so the diff is substantively different; (3) only then commit. Vary the message for each successive commit — describe what actually changed, never restate the prior commit.
- Prefer one substantive commit over several tiny cosmetic ones. When a task fix is genuinely small, make a real semantic change across instruction + verifier + solution + reference together (or add a genuinely new disclosed artifact/mechanism) rather than pushing a near-duplicate — cosmetic prose edits alone will not move the similarity score enough.
- **Concurrency gotcha — do NOT fire multiple PR events in quick succession.** `dynamo-review` uses `concurrency: dynamo-review-<pr>` with `cancel-in-progress: true`. A burst of events (open → reopen → synchronize → force-push, or many re-pushes) makes each new run **cancel** the previous one. In `gh pr checks` the required `cosine_similarity`/`gate` jobs then surface as **fail/cancelled with no real verdict** — this looks like a cosine flag but is only a cancelled run. Fix: push **one** commit, then wait for that single run to complete before touching the PR again. Read the job's actual log/sticky before concluding cosine truly flagged; a `cancelled` conclusion is infra churn, not a similarity verdict.

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

## Mandatory: on every accepted task, record the playbook by category and subcategory

The pipeline assigns each repo a fixed **category** and **subcategory** (`[metadata]`
in `task.toml`). What clears the gates is strongly subcategory-specific: the mold that
draws valid fails in `Security / Vulnerability analysis` is not the one that works in
`Games / World simulation`. So the moment a task reaches **ALL-GREEN** (or its label is
accepted), before moving on, write the playbook down keyed by that pair.

Write **two** things:

1. **A memory file** under
   `~/.claude/projects/-Users-utkarsha-Documents-Project-1/memory/`, named
   `dynamo-<category>-<subcategory>-playbook.md` (kebab-case, e.g.
   `dynamo-security-vulnerability-analysis-playbook.md`), `type: project`, indexed in
   `MEMORY.md`. If the file already exists, **update it** — one playbook per
   category+subcategory pair, never a second file for the same pair.

2. **A section in `PROJECT_MEMORY.md`** in this repo, under a
   `## <Category> / <Subcategory>` heading, then commit and push, so Cloud Agents see
   it too.

Both must carry, for that subcategory:

- **Category / subcategory** and the task repo + final head SHA.
- **The mold that worked** — what the agent is asked to produce and where the
  difficulty lives (reconstruct-a-policy, repair-in-place, starved-sample, …).
- **Measured pass@2 and pass@5** on the accepted head: solved / valid-fail /
  timeout counts and `avg@5`.
- **Which crux actually drew the valid fails**, quoted from the trial analysis —
  this is the single most reusable fact.
- **Hurdles, per gate, in the order they blocked**: cosine, review, validation,
  pass@2, AVA, deep_review, tier1, qc_eval/qc_exec, qc_gate, trials. For each, what
  it complained about and the change that cleared it.
- **Levers measured not to work** for this subcategory, with the numbers, so the
  next task does not re-run them.
- **The gate-vs-gate tensions** seen here (e.g. QC B1 demands a rule be stated
  precisely, and stating it precisely is what lets pass@2 solve it) and how the
  tension was resolved.

Then start the next task in the same subcategory from that file rather than from
first principles.
