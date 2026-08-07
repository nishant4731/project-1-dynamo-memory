# Project Dynamo — Complete Task-Authoring Playbook

> Consolidated knowledge from ~30 authored Handshake AI "Project Dynamo" Terminal-Bench tasks
> (July 2026), the official stump-the-model guide, and every lesson learned along the way.
> Written so another Claude instance can author, harden, and ship accepted tasks from scratch.

---

## 1. What this project is

- You are a Handshake AI "Project Dynamo" fellow authoring hard-but-fair Terminal-Bench-2-style
  tasks in **Harbor** format that stump frontier models.
- **The bar (current, since 2026-06-30): pass@5.** The reference agent runs 5 times; the task is
  **accepted at 0–2/5 solved** (0/5 with valid failures = best band), **rejected at 3–5/5**.
  Reference pair: **GPT-5.4 or Opus-4.8 + Terminus-2** (check the repo), reasoning effort xhigh,
  **3600s hard timeout ceiling** (raising `[agent].timeout_sec` above 3600 does nothing).
- One GitHub repo per task under `handshake-project-dynamo`, named `dynamo-<hash>-<category-slug>`.
- Workflow: fork → work only inside `task/` on a `submission` branch → validate locally →
  push → `gh pr create --fill` → iterate on automated PR-comment feedback until every check is
  green → user submits the platform form (pass@ score + screenshot).
- **Never claim done** until: proposal approved · PR exists · oracle/nop pass locally · static /
  rubric / similarity / validation green · pass@2 with ≥1 valid failure · deep_review + AVA pass ·
  tier1 (if required) · qc_eval + qc_exec + qc_gate green · pass@5 in 0–2/5 with valid fails ·
  final gate green. Pre-push checklist: Section 4A.
- 8-hour tracked time cap per task (incl. revisions); max 2 revisions before Holding-Rejection.
- AI policy: `instruction.md`, the proposal text, and the solution must be **human-written**;
  other files (Dockerfile, test boilerplate) may be assistant-generated if human-verified.

---

## 2. The difficulty doctrine (why models fail, fairly)

### The single most important idea
A hard task does **not** depend on the model not knowing something. It depends on the model being
**confidently wrong** — running the obvious solution, getting output that *looks* right, and
committing to it with no way to notice. Obscurity is not difficulty; frontier models have read
every textbook and CVE.

### The #1 trap to avoid: the "named gotcha"
If a specialist can name the bug in one sentence ("oh, that's the NFC/NFKC mismatch"), the model
names it too and fixes it with the standard one-liner. Never build a task around a recognizable
bug class (biased-nonce ECDSA, CDC-FIFO Gray codes, etc.). "Hard for a human specialist" ≠ "hard
for the model."

### Five core strategies
1. **Silent trap** — the naive solution completes with no error and believable output. Avoid
   anything that throws; models fix everything that throws.
2. **Instruction-defined but never-sampled cases** — the spec fully determines every graded case;
   the shipped samples just never exemplify some of them (the `gnss-log-decode` pattern). The
   instruction must never lie; every graded case must be unambiguously derivable.
3. **Remove self-verification** — no oracle, reference binary, or checkable ground truth in the
   environment. Real grading runs on hidden held-out cases.
4. **Compound corrections that overlap** — several independent fixes that interact on the same
   records; fixing some-but-not-all still fails.
5. **Exact grading** — tolerances calibrated so every valid method passes and every
   requirement-violating method fails; exact match for discrete outputs.

Amplifiers: silent failure, no self-check, all-or-nothing grading.

### Fairness (non-negotiable — ~half of all rejections)
- Every rule the verifier enforces must be **stated in the instruction or derivable from shipped
  files** — format, sort order, tie-breaks, thresholds, encodings, hash conventions, dedup rules.
- One-line test: *could a careful engineer who follows the instruction exactly still fail the
  verifier?* If yes → unfair; fix the prompt/band, not the difficulty.
- When a value can be computed more than one valid way, **name the single canonical rule**.
- Misdirection allowed only if something the agent can see sets the record straight ("no
  uncorrectable lie").
- The meta-test: **if writing the deciding rule down plainly makes the task easy, the difficulty
  was fake.** A good task stays hard with every rule stated.
- Red flag: failing tests about file existence or output formatting = undisclosed convention,
  not difficulty.

### The five rejection reasons (run this checklist on every task)
1. Grading on a rule you never told the agent (undisclosed verifier convention) — the #1 cause.
2. Task files contradict the instructions (even files labeled "old"/"unused").
3. Instructions that read two ways (ambiguity — the score just measures which reading was guessed).
4. The only hard part is the mistake (difficulty collapses once the defect is disclosed).
5. Decoys with no way out (an authoritative-looking lie nothing visible corrects).

---

## 3. THE EMPIRICAL CORE: what actually stumps frontier models

This is the hard-won knowledge that the official guide does not tell you.

### The fully-specified-spec ceiling (firm rule)
**Never build "compute the exact answer to a fully-specified deterministic problem over a fully
visible instance."** Confirmed across 10+ failed attempts: a complete normative spec = pure
transcription for Opus-4.8/GPT-5.4. They read the whole spec for 20–30 min, then implement
~500-line solutions single-shot and self-verify. Defeated levers (all drew 2/2-solved): traps,
entanglement, 40 independent rules, machinery growth, optimization reshaping, deferring a single
readable constant, non-idempotency guards that are spec-stated. Verdicts literally say "the SPEC
was sufficiently prescriptive that a careful first-principles reading leads to a correct
implementation." Fair, self-contained, spec-driven tasks cap at ~20–40% per-trial fail rate —
never the ~60% you need.

### The two proven winning shapes
1. **The salvage/repair mold** (restitch / shoot-mend / depot-mend family — accepted ~15 times):
   a reusable CLI tool (`/app/<tool> <dir>`) that repairs a crashed store/spool/vault/pipeline
   **in place**, combining:
   - **Evidence consumption** — the tool files verified items then DELETES the evidence realms,
     so a buggy first draft run on the sole live copy destroys graded state forever.
   - **Evidence-mined hidden parameters** — e.g. per-device clock offsets recoverable only by
     differencing verified anchors (including superseded ones), with lying decoy fields.
   - **Digest-driven assembly search** — floating fragments assigned by backtracking against
     registered digests.
   - **Exact-integer report accounting** — a JSON report of 13–23 independent counters, each
     computed at a distinct pipeline decision point.
   - **Byte-exact naming rules** — collision ordinals, leading-dot extension splits, case folding.
   - Graded **differentially**: verifier runs the agent's tool on pristine copies of the shipped
     fixture + 4–5 held-out seeds and compares against a reference.
2. **Reverse-engineering / spec-by-environment** (infer-release-gate / infer-rollout-gate family):
   no prose rules; the agent gets a labeled corpus (~300 records) + a schema doc disclosing
   function FAMILIES but not constants; must recover a deterministic policy (~20 interacting
   rules) and reimplement it; graded on fresh held-out records. The wall = at least one
   **exact-integer NON-LINEAR score formula** (caps, hinges, clamps) — regression/tree fits
   validate on training and fail held-out.

When a subcategory is saturated with your own molds, **port the proven engine that has never
appeared in that subcategory** (not a reskin of one that has) — this produced first-commit
ALL-GREENs three times in a row.

### Kill levers, ranked by observed lethality
1. **Evidence consumption / operational irreversibility** — fires ~2–3 of 5 trials per draw;
   several failing agents had CORRECT final tools (passed all held-out seeds) but had already
   destroyed the shipped fixture with a draft run. Strongest when the contract is broad (a first
   build is never complete) and the destructive step is the LAST thing the tool does. Caveat:
   some agents test on a /tmp copy (it fired 0/5 once) — never rely on it alone.
2. **Report-side independent counters** — one-field slips by otherwise byte-exact solvers.
   Deadliest variants: counters whose value depends on WHEN they're sampled (before vs after
   eviction — two agents wrong in opposite directions); counters whose branch has no visible
   output artifact (one killed 4/5 trials whose main output was byte-perfect); fields whose value
   SOURCE differs between verified and failed entries (the wrong reading coincides with golden on
   all verified entries).
3. **Slip-surface exactness**: dotfile/collision ordinals, leading-dot extension splits,
   case-sensitive literals, ceil-vs-floor with primes that never divide the rate, validate-at-parse
   vs validate-at-output, `\r`/strip() divergences, stdlib glob semantics (`fnmatch` `*`/`?`
   crossing `/`, `**`), strftime `%M` vs `%m`.
4. **Evidence-mined parameters** with decoys (check every decoy for a constant relation to the
   hidden truth — a decoy that is `truth + 977` is a free shortcut; add per-item jitter).
5. **Corrupt records of a NON-obvious kind carrying a forged decision-relevant field** (a corrupt
   commit-record forging a timestamp that shifts a whole retention window) — stronger than
   corrupt content bytes.
6. **Bit-exactness cruxes** for porting tasks: binary32 double-rounding (JSON decimal →
   `float()` → `struct.pack('f')` is 1 ULP wrong near the midpoint; correct route needs
   `Decimal`/`Fraction`); Python `set` dedup collapsing `0.0`/`-0.0`.
7. **Self-check-blind design**: ship a deliberately clean sample (container mechanics only) so
   self-testing teaches nothing; every rule exercised only in held-out fixtures. Rules whose
   correctness is content-reconstruct-checkable always get solved; prefer layout / ordering /
   absence / accounting properties the agent's natural self-check can't see.

### Difficulty-scaling laws (learned the expensive way)
- **Volume of genuinely distinct rules is the primary flip mechanism** — push cumulative solve
  time toward the 3600s budget so the self-correction margin vanishes. ~15 rules drew 3–5/5;
  ~18 distinct rules with pass@2 solve time at ~50 min flipped to 1/5.
- **When pass@5 sits at 3–4/5: add 2–3 genuinely distinct INTERACTING subsystems in one push**
  (not edge cases, not redraws). Confirmed 5+ times; each flip was one push (4/5→1/5, 3/5→1/5).
- **Kind beats quantity past a point**: same-kind rules get self-debugged away (adding 5 similar
  rules once made agents FASTER). The rule that breaks a deadlock **re-keys the whole algorithm**
  (e.g. sessions changing the identity tuple, forcing every existing rule to be revisited).
- **Prefer rules that MULTIPLY with already-graded exact-format rules** over standalone rules
  (locale routing as the collision-ordinal scope produced 3 of 4 kills).
- **Entanglement per unit of implementation volume**: when agents are byte-exact and near budget,
  add ~8-line derivation chains with many orderings/roundings/units to get wrong (offset →
  reading-rate lengthen → frame-grid snap), feeding outputs already graded.
- If render/mechanism volume plateaus (repeated 2/2 draws), the flip comes from adding an
  **orthogonal exactly-graded deliverable** (the accounting report) computed at the same decision
  points as the main output.
- **Witnesses are free difficulty; filler is not** — when forced to add witnesses, cut random
  filler in the same push.
- **"Does this subsystem make the agent *derive* something, or just *type* something?"** — only
  the first buys valid fails.

### When NOT to ratchet
- **>90%-of-budget rule**: if the pass@2 solver used >90% of the agent budget, STOP — more volume
  converts good valid fails into invalid timeouts. The ratchet discriminator is **spare budget**,
  not the pass@2 solve ratio.
- A 0/2 draw with clean valid fails and zero timeouts is already the right band — more load risks
  converting anchors into invalid timeouts (one task won by never pushing its fully-built ratchet).
- An UNANALYZED/infra-tainted draw is not a difficulty verdict — redraw with a difficulty-neutral
  push (a `README.md` note outside `task/` never enters the agent image).
- pass@2 blocking on TIMEOUT with high near-miss scores → SHRINK breadth (cut a whole non-crux
  axis), don't add rules. Trim targets = mechanisms that never appear in any fail analysis.
- Reverse-engineering calibration: MORE score constants → agents commit a wrong parameterization
  (a VALID anchor); FEWER → they loop on regression fits and productive-timeout. 4 timeouts +
  1 anchor = trim non-crux breadth (drop a field); never simplify the score wall. If every trial
  mis-frames the formula's shape (penalty-from-100 vs additive-from-0), disclose the SHAPE —
  costs no determinacy, converts clock fails into merit fails.
- Reduced agent timeouts are counterproductive: a doomed destructive trial cut mid-flail becomes a
  neutral in-progress-timeout instead of a countable fail. Keep 3600s.
- Budget ~1 subsystem per 10 min of agent time; the repair mold lands at ~30–35 min solve time.

---

## 4. Gate mechanics (pass@2 / pass@5 / what counts)

### Full pipeline order (every push)
Each push cancels the in-flight run and starts fresh. Downstream jobs **skip** when an upstream gate fails.

```
cosine_similarity      FIRST gate — embedding match vs DELIVERED Dynamo tasks (enforced, ≥0.90 blocks)
    ↓
review/review          Stage 1 — deterministic static checks + Dynamo eval (31 rubric criteria)
    ↓
similarity             duplicate / near-duplicate vs public TB2/TB3 (lexical; verdict UNIQUE/duplicate)
    ↓
validation             harbor oracle must score 1.0, nop must score < 1.0
    ↓
ratelimit              daily pass@2 budget (6 runs/day/task, UTC midnight)
    ↓
pass@2                 2 agent trials — need ≥1 valid failure, no blocking timeout
pass2_suggestion       advisory hardening hint (max 2/day, never blocks)
    ↓
deep_review  ─┐
ava_review   ─┼─ parallel LLM gates (either blocks → tier1 skipped, QC skipped, trials skipped)
adversarial_review ─┘  (adversarial is advisory-only — never blocks)
    ↓
tier1                  fix-addressal — only when a prior QC run left open Major fixes
    ↓
qc_eval  ─┐            Tier-2 QC — LLM read of ~37 soundness checks
qc_exec  ─┘            Tier-2 QC — Daytona execution probes + mutation reasoning (A6/B5/C3)
    ↓
qc_gate                consolidates eval+exec + runs heavy C3 mutation probes (~44 checks total)
    ↓
trials                 pass@5 — 5 agent trials; accepted band is 0–2/5 solved with valid fails
    ↓
gate                   final aggregator — any red upstream job blocks here
```

**PR comment stickies to read (in order of appearance):**
| Check job | Sticky comment header | HTML marker |
|---|---|---|
| `review/review` | `### Dynamo eval — …` | `<!-- dynamo-eval -->` |
| `deep_review` | `## 🤖 Automated Review` | (none) |
| `adversarial_review` | `## 🔍 Adversarial Cheat-Pass (advisory)` | (none) |
| `ava_review` | `## 🤖 Automated Review (AVA ∪ Deep-Review union gate)` | `<!-- AVA-GATE -->` |
| `tier1` | `## 🚦 Tier-1 fix-addressal` | `<!-- TIER1-ADDRESSAL -->` / `TIER1-BASE:` |
| `qc_gate` | `## 🤖 Per-Check QC — Task Soundness` | `<!-- QC-STICKY -->` / `QC-BASE:` / `QC-FIXES-B64:` |

Sticky comments are **edited in place** (createdAt stays at first run) — always read the `QC-BASE:` / `TIER1-BASE:` SHA and the **job log** for full finding text (stickies truncate).

### 4A. Stage encyclopedia — what each checker hunts

Use this as a **pre-push checklist**. Ship Section 6's hardening kit from commit 1 to pre-clear AVA + qc_gate; the recipes in Section 7 fix specific failure modes once they appear.

---

#### `cosine_similarity` — delivered-task embedding gate (FIRST gate; enforced, gates)

**Runs before everything.** A red here **skips the entire rest of the pipeline** (review, similarity, validation, pass@2, …) — so `gate` goes red and you get NO other feedback. Because it precedes pass@2, iterating on it does **not** burn pass@2 budget.

**What it does (from the job script):** POSTs two **facets** — `task/instruction.md` and `task/tests/test_outputs.py` (first 64 KiB of each) — to an internal service (`ai.joinhandshake.com/api/internal/task-similarity/checks`, `Joinera`). The response carries `enforcement` (`shadow`|`enforced`), `overallVerdict` (`clear`|`flag`), `threshold` (≈**0.90**), and per-facet `facetResults.{instruction,verifier}.maxScore`. It **blocks only when `enforcement==enforced` AND `overallVerdict==flag`** (i.e. some facet's maxScore ≥ threshold against a **delivered Dynamo task**). The matched task and the scores are **hidden** on an enforced block (scores are only surfaced in `shadow` mode, under `observedFacetResults`).

**Fail-open:** an unavailable/invalid/`turned off` response does **not** block ("only a confirmed duplicate in enforced mode is terminal"). So a red cosine_similarity is a real ≥0.90 match, not an infra flake.

**vs the `similarity` gate:** totally separate. `similarity` is a **lexical** duplicate check vs **public TB2/TB3** (verdict UNIQUE). `cosine_similarity` is a **semantic embedding** check vs **delivered Dynamo tasks** (your org's accepted corpus). A task can be UNIQUE on `similarity` yet ≥0.90 on `cosine_similarity`.

**What legitimately trips it — and the fix:** two mold tasks share the *hardening-kit boilerplate* in `test_outputs.py` (delete-oracle, priv-drop, sealed-oracle, mutant-sweep) → the **verifier facet** self-scores high vs a delivered sibling. **Fix that works: move ALL reusable machinery into a private helper module** (e.g. `tests/_harness.py`, which is **not** a compared facet) and keep `tests/test_outputs.py` a thin, distinct list of assertions; keep `instruction.md` prose lexically distinct from sibling molds. Squashing / rewriting commit history does **nothing** — it compares file *content*, not commits.

**The self-ingestion trap (confirmed 2026-08-07, df4e109):** the corpus appears to **ingest your own commits once they PASS cosine and run the pipeline.** Sequence observed: commit A passed → ran pass@2 → got ingested; **every** later commit on the same PR then failed cosine, and *stayed* failed after fully **rewriting** `test_outputs.py` **and** fully **paraphrasing** `instruction.md`. Embeddings capture **meaning**, and it is the *same task*, so it self-matches ~1.0 regardless of wording — **no task-side edit can escape once a version is ingested.** This is a platform bug (missing same-repo/self exclusion). **Do NOT thrash** (each push re-ingests and pollutes the corpus): stop, flag the platform owner, and wait for a fix or a corpus purge; then a single re-trigger clears it. The "move-boilerplate-to-helper" trick genuinely helps the *first* time (real sibling overlap) but is **not** a cure for self-ingestion. Also confirmed on df4e109: adding a **whole new graded artifact** (a per-op `edit_ledger.tsv` with its own schema — the "peer_cap_ledger" lever that cleared cosine for peer `c9a0d11`) **also failed** once already poisoned — that lever is *prevention* (distinctive first submission), not a *cure*.

**How to overcome (recovery playbook):** the Dynamo team flipped this gate shadow→**enforced**; under enforcement every commit that PASSES cosine and runs is indexed, so your own earlier passing snapshots become the match. (1) **Prevention is the only reliable path** — submit the HARD, final, distinctive version on the FIRST push; never iterate easy→hard on-PR. (2) **Already poisoned →** escalate to Dynamo maintainers to purge/de-index the repo's lineage (fastest; task stays intact), OR rebuild as a genuinely different *concept* (different inputs + core trap + output contract; reskin/rename/new-mechanic/new-sidecar is not enough), OR start in a fresh assigned repo and author the hard version first.

**Every push after a PASS needs its own fresh reskin — even one that only touches non-graded files.** Confirmed on df4e109: a commit that ratcheted difficulty entirely inside private `_gen.py`/`_harness.py`, deliberately leaving `instruction.md`/`tests/test_outputs.py` byte-identical to the immediately-prior PASSING commit, still blocked — identical content trivially self-matches its own now-indexed predecessor at ~1.0. "I didn't change the compared files" is not a shield once the predecessor is indexed; it's the failure mode. Bundle a real (if small) reskin into every push that follows a cosine PASS, not only the ones that consciously change the graded contract.

Full recovery detail + the "confirmed NOT to work" list live in `AGENTS.md` → "How to overcome cosine self-poisoning".

---

#### `review/review` — Stage 1 static + Dynamo eval

**Two gates in one job.** Static checks run first (deterministic, ~10s failures); Dynamo eval (LLM against `references/dynamo-rubric.toml`) runs in the same job and posts the `<!-- dynamo-eval -->` comment.

**Static checks hunt (deterministic — fix before pushing):**
- `.dockerignore` missing when `environment/` has subdirectories (`data/`)
- Dockerfile COPYs `solution/` or `tests/` (even in comments — grep is literal)
- Unpinned pip/npm in Dockerfile RUN lines (`pip install … --retries 5` fails as unpinned `5`; use `ENV PIP_RETRIES=5`)
- Base image not pinned by `@sha256:` digest
- `allow_internet = false` (live rubric requires open internet)
- instruction.md ends with "You have N seconds…" (fails `instruction_concision`)
- Root-level `task = "..."` string instead of `[task].name` (Harbor loads zero tasks)
- `[task].description` **required non-empty** by the static checker (documented in repo README) — but Dynamo eval's `task_toml_schema` criterion may **fail** the same field as "not in Harbor schema". Known conflict: keep `description` for static; if eval blocks, note the conflict in a PR comment rather than removing it.
- `check-diversity-labels.py`: invalid `task_objective` / `artifact_type` vocabulary
- `no_extraneous_files`: `__pycache__`, `jobs/`, editor cruft staged
- Missing `artifacts` top-level declaration for every agent path the verifier reads

**Dynamo eval hunts (31 rubric criteria — same list as deep_review, LLM-graded):**
All criteria in `references/dynamo-rubric.toml` must PASS. High-frequency blockers:

| Criterion | What it looks for |
|---|---|
| `unambiguous` | A competent domain expert could produce a passing answer; name a **concrete sound approach** that would fail before blocking |
| `test_instruction_alignment` | Every assertion traces to instruction; every instruction requirement has a test; atomic functions with docstrings |
| `anti_cheat` | No oracle/expected values in `environment/`; tests resist shortcuts |
| `verifier_configuration` | Single shared image; pytest baked & pinned; ground truth only in `tests/` overlay |
| `environment_hygiene` | No solution/tests COPY; no verify-time `pip install` in `test.sh` |
| `instruction_concision` | Human prose, absolute `/app/…` paths, no tool listings, no step-by-step procedure |
| `open_internet` | Must not require offline; answer not Googleable |
| `task_toml_schema` | Only recognized Harbor fields — **no invented keys** |
| `metadata_reality_alignment` | Every count/stat in task.toml/README matches shipped data |
| `solution_quality` | Solution computes; no bare-printed final answers |
| `verification_explanation_quality` | Every tolerance justified against instruction |

---

#### `deep_review` — Automated Review (gates)

**Mindset:** read-only **contract auditor** — spec alignment, discoverability, metadata. AVA (Section 4B) handles **verifier soundness**; both form a **union gate** — either blocks pass@5.

**Division of labor (official):** Deep Review asks "does the task work and is the contract fair?" AVA asks "can the grader be fooled?" Deeper contract-coherence checks live here; attack-the-boundary checks live in AVA.

**What it hunts:**
- **Unverified requirements** — maps each normative spec clause → test assertion; any gap is blocking
- **Oracle derivation** — reference must derive every decisive value from agent-visible inputs; no smuggled answer tables
- **Metadata drift** — quoted file counts, actor counts, fixture sizes in task.toml must match reality
- **Discoverability** — hidden behavior must be stated in instruction OR derivable from shipped `environment/` files (headers, schemas, README)
- **Advisories escalate** — fix deep_review advisories immediately; QC probes often promote them to Majors later

**Typical blocking patterns:**
- Verifier grades behavior never stated in instruction or environment docs
- Instruction contradicts itself or contradicts shipped data
- Hidden test depends on default/fallback behavior not pinned in agent-visible text
- Over-strong instruction claims ("single self-contained executable") create enforcement burden — delete the claim

**Does NOT block on:** speculative ambiguity, tolerance calibration it cannot verify, pass@5 difficulty signal (undemonstrated crux is advisory).

---

#### `adversarial_review` — Adversarial Cheat-Pass (**advisory only**)

**Never gates the PR.** Still read every FAIL — QC and human reviewers often care about the same exploit class.

**Mindset:** red-team the **verifier**, not the agent solution. Reads the **git repo**, not the built container image — "generator is agent-visible" can be a false positive; verify against the actual Docker image.

**What it hunts:**
- **Fixture memorization** — behaviors covered only by fixed literal tests with no held-out oracle (the #1 finding shape)
- **Lookup-table pass** — randomized tests that never exercise the hard sub-behaviors (e.g. VM preflight only tested on fixed invalid programs; replay branch-certification only on fixed multi-tick trees)
- **Tolerance exploits** — over-wide bands where wrong methods pass (rare in exact-integer tasks)
- **Hardcodable constants** — rules whose answer is identical on every graded instance
- **Copied-oracle deliverables** — agent could paste expected output without computation

**Pre-emptive fix:** for every subsystem, ship either (a) a randomized held-out oracle with `SystemRandom` entropy, or (b) enough structurally distinct fixed seeds that literal-key shims cannot cover all cases. Mirror the `reference_resolve_round` / `reference_plan_routes_small` pattern.

---

#### `ava_review` — AVA-GATE (gates)

> Full AVA doctrine, exploit catalog, and 11-item self-check: **Section 4B**.

**Mindset:** stochastic adversary that tries to **make the verifier accept invalid work**. Attack enumeration varies run-to-run — identical code can pass one push and block the next. Pin/harden pre-emptively. **Empty AVA output = fail-closed.**

**Major check families (blocking when `routing=block`):**

| AVA check | What it tries |
|---|---|
| `sound_verifier` | Wrong/invalid submission still gets reward=1 — e.g. lookup shims, forged purity reports, import-time `reward.txt` writes |
| `verifier_coverage` | Mutants / wrong implementations pass because tests don't exercise the broken path |
| `no_false_rejection` | Verifier rejects valid alternative formats the instruction allows |
| `metadata_reality_alignment` | task.toml claims don't match files |

**Recurring AVA attack shapes (from signal-bastion and accepted tasks):**
1. **Import-time reward poisoning** — agent module writes `reward.txt=1` on import; pytest fails but reward sticks → fail-closed `test.sh` (write 0 first, rewrite after pytest)
2. **Purity spoof** — `_submission_call` reports `args_after == args_before` without checking → capture args in child process before/after; response path via `sys.argv[2]` not request JSON
3. **Narrow randomized probes** — `SystemRandom` tests exist but parameter space too small (2-agent 3×3 only; arithmetic-only VM ops) → broaden grid sizes, agent counts, opcode sets
4. **Missing reference oracle** — randomized tests compare against hand-built expected instead of independent recomputation → ship `reference_*` functions in verifier
5. **CONSTANT graded facts** — same output on every seed → property-balanced held-out seed search

**When AVA blocks on noise** (finding's own evidence shows agreement): hand-verify, push benign redraw + explanatory PR comment; don't change grading.

**Infra block:** "Set the DYNAMO_EVAL_API_KEY" = platform gap; flag admin, don't thrash commits.

---

#### `tier1` — Tier-1 fix-addressal (gates when HOLD)

**Only runs after a prior QC failure.** Verifies you **attempted** each required fix before re-running the expensive Tier-2 QC.

**What it hunts:**
- Each Major from the last `QC-FIXES-B64` / sticky must show a **real diff** to the named file(s)
- **Empty commit = "fix not attempted"** → HOLD blocks full pipeline at `gate`
- `base_sha` is pinned at the finding commit and **never advances** — tier1 diffs cumulatively from that base
- Cumulative diff **truncates at ~60 files** — a bulky fixture regen can push your fix out of view → "not attempted". Fix: shrink cumulative diff (`git checkout <pinned-base> -- <bulky paths>`); land QC fixes in **small separate commits**, never bundled with fixture regen
- D-findings naming a file (e.g. "D3 Environment Build Failure" from infra flake) clear only on a defensible edit to **that exact file** (`ENV DEBIAN_FRONTEND=noninteractive`, `PIP_NO_CACHE_DIR=1`, …)

**On PASS:** posts `TIER1-STATE:{"verdict":"PASS","fixes":{"C3":true}}` and unlocks `qc_eval` + `qc_exec`.

---

#### `qc_eval` — Tier-2 LLM soundness eval (gates)

> Exhaustive check IDs A1–E7: **Section 4B**. Five strategies + 15-item checklist there too.

**~37 read-only soundness checks** via `tools/dynamo_qc_eval/run_eval.py` (Claude Opus, 3 deep samples, 8 parallel workers). Maps to the **30 official Major IDs** below plus extended probes. No container execution — pure file/contract analysis.

**Major families (ANY one fails the task):**

| Family | Code | Hunts |
|---|---|---|
| **A — Solution/oracle** | A1–A6 | Oracle fails own verifier; incomplete reference; hardcoded answers; hidden/privileged access; undocumented assumptions; edge-case bugs |
| **B — Contract coherence** | B1–B6 | Ambiguity; contradiction; missing definitions; undocumented enforced requirements; underdetermined mappings; unstated anomaly policy |
| **C — Verifier rigor** | C1–C6 | Stub output accepted; over-permissive tolerance; **hardcodable held-out coverage**; truth from agent-writable inputs; NaN bypass; scoring mismatch |
| **D — Fixtures/determinism** | D1–D5 | Degenerate fixtures; build failures; nondeterminism; unseeded build-time randomness |
| **E — Anti-cheat** | E1–E7 | Readable oracle; unpinned inputs; **harness plumbing exploit**; root secrets; symlinks; unsafe extraction; copied-oracle deliverables |

**Core principle:** everything graded must be derivable from `instruction.md` + `environment/` + shipped examples; verifier must independently enforce every structural requirement, not a proxy. "Near-correct / immaterial / intended difficulty" are **not** valid defenses.

**High-frequency qc_eval blockers:** B1 ambiguity (type/semantics underspecified), B2 contradiction (instruction vs data), C2 over-permissive tolerance, C4 truth from agent-writable files.

---

#### `qc_exec` — Tier-2 execution probes (gates)

**Runs on Daytona** — actually builds/runs the task and executes deterministic + reasoning probes. Companion to `qc_eval`; results merge into the QC sticky.

**What it runs:**
1. **Deterministic probes** — symlink attacks, oracle leak checks, loose-verifier probes, demonstrated exploit attempts in container
2. **Reasoning probes (A6/B5/C3-exec)** — LLM-guided mutation loop: mutates reference/source, runs verifier, checks if mutation is caught

**Typical blocking output:** `FAIL blocking=['C3-exec']` — mutation survived verifier (same root cause as qc_gate C3 but caught earlier in exec tier).

**Infra:** `DAYTONA_API_KEY` missing → job fails; not a task signal.

---

#### `qc_gate` — Per-Check QC / C3 mutation gate (gates)

**The heaviest commit-loop stage.** Consolidates `qc_eval` + `qc_exec` artifacts and runs ~44 total checks & probes. Posts the `<!-- QC-STICKY -->` comment with machine-readable `QC-BASE:<sha>` and `QC-FIXES-B64:` (base64 JSON of required fixes).

**The #1 blocker: C3 — Narrow / Hardcodable Held-Out Coverage**

The C3 prober **mutates** your reference (or a copy) to violate one stated rule, runs the verifier, and checks reward=0. If the mutant passes → Major block.

**What C3 looks for:**
- Too few held-out seeds — literal-key / `if input == <fixture>` shim passes everything
- Randomized tests that don't cover the mutated dimension (blink energy, replay half-range `<= 32768`, preference-rank tie-break, living-start attack guard, …)
- Fixed tests whose inputs are visible constants in test source — adversarial cheat-pass finding becomes C3 block on next push

**C3 recipes (ship from commit 1):**
- **Layered precedence** → distinct value at every layer
- **Order-sensitive rules** → ≥3 elements under a non-involutive permutation
- **"Summed over all X"** → witness in each X-subclass
- **Boundary constants** → fixture at exactly the boundary (EXACTLY min_bytes; EXACTLY `newest − keep_within`)
- **Every literal the contract spells out** → case-fold / delimiter-position variants pre-emptively
- **`A and B` predicates** → plant (A,¬B), (¬A,B), (A,B)
- **Single-fixed-value parameters** → vary per held-out seed; which row drifts must vary too
- **Rarely-taken branches** → deterministic boundary probes on fixed stride
- Force coverage in generator `_self_check` asserts

**Other qc_gate advisories (usually non-blocking):** type-coercion boolean bypass, correctness not statically confirmable.

---

#### Pre-push cross-stage checklist (minimize commit loops)

Ship all of these **before first PR push** (also run the **15-item official checklist** in Section 4B):

1. Section 6 hardening kit (pytest isolation, fail-closed reward, reference oracles, delete-oracle, privilege drop, determinism, mutant sweep, §-maxima witnesses)
2. Every normative spec clause → discriminating fixture on shipped + ≥1 held-out seed
3. Every subsystem → randomized `SystemRandom` oracle OR ≥3 structurally distinct fixed seeds per hard behavior
4. `_submission_call` purity enforced in child process; no response path in request JSON
5. task.toml counts match actual data; `[task].description` present for static
6. instruction.md pins every hidden edge case the verifier tests (especially defaults before time-based rules)
7. Full mutant sweep locally (30–90 single-rule mutants; no-op control mutant must score 1)
8. oracle 1.0 / nop 0.0 with **all hardening active** (including planted conftest + PATH shim attacks)

**When a stage fails:** read the sticky comment → identify check ID (B1, C3, `sound_verifier`, …) → apply matching recipe in Section 7 → repin verifier bytes if tests changed → oracle/nop → one focused push (never push while trials live).

---

### 4B. Official QC & AVA guide (Flags & Fixes)

> Sourced from the Dynamo learning platform **Flags & Fixes** and **Pass AVA** pages. Use alongside Section 4A for pre-push hardening.

#### QC gate mindset

The QC evaluation reviews every submission **adversarially**. It assumes the task should **FAIL** unless it can verify every requirement is implemented correctly. It looks for ways a model could produce an **incorrect answer and still pass the verifier**.

**How the gate decides:**
- Defaults to **FAIL**; reaches PASS only when every break attempt is refuted by a citation in your code
- **Any single Major check fails → entire task fails** — breadth matters as much as depth
- **No discretion** to excuse a surfaced break — "near-correct," "immaterial," "obscure," and "intended difficulty" are **not** valid defenses
- Materiality sets severity only; it never decides whether something is a finding

**Core principle:** everything the verifier grades must be **derivable** by the agent from `instruction.md` + `environment/` + shipped examples. The verifier must **independently enforce every structural requirement**, not a proxy metric. Design backward from that.

#### The 30 Major checks (qc_eval / qc_gate — every ID blocks)

| ID | Check |
|---|---|
| **A1** | Oracle fails its own verifier — reference wouldn't score full reward as shipped (fixture/generator bug) |
| **A2** | Incomplete reference — `solution/` doesn't perform every action the instruction requires |
| **A3** | Hardcoded answer in reference — decisive value baked in, not computed from agent-visible inputs |
| **A4** | Oracle hidden/privileged access — imports private crux module or reads protected fixture agent can't reconstruct |
| **A5** | Oracle undocumented assumption — silent default, injected record, unit conversion, or dedup neither documented nor derivable |
| **A6** | Oracle edge-case/logic bug — valid input class where oracle crashes or returns wrong result |
| **B1** | Ambiguous rule — two reasonable readings yield different graded answers; nothing agent-visible picks one |
| **B2** | Internal contradiction — rules conflict on real input, or end-state unreachable via permitted mechanism |
| **B3** | Missing definition/field/data — graded computation needs value absent from agent-visible inputs |
| **B4** | Undocumented requirement enforced — verifier grades hidden thresholds, encodings, precedence, tie-breaks |
| **B5** | Underdetermined mapping — disclosed material doesn't uniquely determine outputs (rule family undisclosed, inputs outside observed range) |
| **B6** | Unstated anomaly policy — duplicates, ties, malformed rows, overlapping windows with no stated handling |
| **C1** | Stub/partial output accepted — report-only, boolean-only, or subset of actions clears verifier |
| **C2** | Over-permissive tolerance — band accepts a concrete materially-wrong answer |
| **C3** | Narrow/hardcodable held-out coverage — hardcoded constant or ignored input still passes |
| **C4** | Truth from agent-writable inputs — verifier recomputes expected from paths agent can alter |
| **C5** | NaN/Infinity bypass — graded numeric with no non-finite rejection |
| **C6** | Scoring contract mismatch — reward scheme contradicts stated grading (partial credit promised, binary `test.sh`) |
| **D1** | Degenerate fixture — initial/no-op state already satisfies verifier |
| **D2** | Malformed/unparseable fixture — shipped data raises parse error under assumed format |
| **D3** | Environment build failure — unpinned/uninstallable dep fails for specified Python/OS |
| **D4** | Nondeterminism — unseeded RNG, `time.time()`, network fetch, set/dict iteration order changes graded answer |
| **D5** | Unseeded build-time randomness — key/IV generated at build without fixed seed |
| **E1** | Oracle/answers readable by agent — `solution/`, `tests/`, seeds, or expected values in agent image |
| **E2** | Immutable-input integrity not enforced — protected path not hash-pinned AND tampering changes outcome |
| **E3** | Reward/harness plumbing exploit — agent-writable file imported/executed as verifier code |
| **E4** | Root/elevated access exposes secrets — agent reads ground-truth file verifier relies on |
| **E5** | Symlinked output path — verifier follows agent symlink to golden/expected file |
| **E6** | Unsafe archive extraction — agent archive with `../` or absolute paths not sanitized |
| **E7** | Copied-oracle deliverable — agent passes by preserving/copying reference tool without real work |

#### Five proven strategies (official — build tasks like the green blocks)

**Strategy 1 · Put every graded decision in agent-visible material** (A3, A5, B3, B4 — *most common flags*)
- Enumerate every constant, threshold, tie-break, ordering, precedence, unit, filter the verifier uses
- For each, cite the exact line in `instruction.md` or `environment/` — if it lives only in `solution/`/`tests/`, document it or remove the dependency
- If mechanism must be **learned** not told: say so explicitly AND ship enough data to pin it uniquely (pass pattern: rule recoverable from gold frames/corpus; fail pattern: `FLOOR = 4.5` only in solution)

**Strategy 2 · Enforce structure, not just an aggregate** (C1, C2)
- List every structural requirement (exact count, shape, keys, ordering, byte-exactness) → one assertion each
- Never let ARI/RMSE/correlation/count-tolerance stand in for structure
- Actively construct a wrong-shape answer that clears your metric — if you can, tighten (fail pattern: correct logic never exercised because no fixture reaches closure threshold)

**Strategy 3 · Protect ground truth in code, not by convention** (C4, E1, E2, E5)
- Grade from verifier's own `/tests` copy OR recompute from non-agent-writable inputs
- Never re-read agent-writable path for expected answer (fail pattern: `compute_expected()` reads `/app/data` the agent corrupted)
- Open graded outputs with **O_NOFOLLOW** / `os.lstat` + `realpath` guard; hash-pin protected inputs; never COPY `solution/`/`tests/` into image
- Pass pattern: assemble graded package from pristine spec + submission artifact only in private temp dir

**Strategy 4 · Make the whole pipeline deterministic** (A1, D3, D4, D5)
- Seed every RNG on graded paths; env-var seed without default = nondeterministic
- Avoid `time.time()`, network fetches, hashing set/dict iteration order
- Pin deps exactly; don't hash-match binary from unversioned toolchain (fail pattern: fixed SHA-256 of GCC-built binary)
- Pass pattern: explicit total-order sort keys; fixed timestamps; exact decimal arithmetic

**Strategy 5 · Ship a complete reference that derives its answer** (A2, A4, B5)
- Reference performs **every** mandated action, not a subset
- Derives from agent-visible inputs — no private module handing the crux unless its output is recoverable from shipped corpus (pass pattern: `octant_core` import OK when SPEC says corpus fully determines field widths)

#### Official pre-submission checklist (15 items)

Run before first PR push; each maps to Major IDs:

1. All verifier rules in `instruction.md` or derivable from `environment/` — constants, thresholds, tie-breaks, units (**A3, A5, B3, B4**)
2. Nothing graded lives only in `solution/` or `tests/`
3. If mechanism must be learned: instruction says so AND shipped data pins every graded answer (**B5**)
4. Verifier enforces every structural requirement, not just aggregate metric (**C1, C2**)
5. You tried to construct wrong-shape/degenerate answer that clears metric — and couldn't (**C1, C2, C3, D1**)
6. Graded numerics reject NaN/Infinity (**C5**)
7. Reward path matches stated grading — binary vs partial credit (**C6**)
8. Ground truth from `/tests` or non-agent-writable recompute; no agent-writable path feeds expected (**C4, E2**)
9. Graded output paths opened with O_NOFOLLOW; protected inputs hash-pinned (**E5, E2**)
10. `solution/` and `tests/` never COPY'd into agent image (**E1**)
11. Every reference-tool copy neutralized; deliverable self-contained (**E7**)
12. RNGs seeded with fixed default; no time/network/iteration-order nondeterminism; deps pinned (**D3, D4, D5**)
13. Reference scores full reward against verifier exactly as shipped (**A1**)
14. `solution/` performs every instruction action, not a subset (**A2**)
15. Every data anomaly (dupes, ties, malformed rows) has stated, enforced handling (**B6**)

#### AVA — Adversarial Verifier Audit (official doctrine)

**Division of labor:** AVA audits the **verifier**, not whether the task "works." Deep Review / Automated Review handles contract coherence and spec alignment. **AVA ∪ Deep-Review union gate** — both must pass; either blocks → pass@5 skipped.

**Question AVA asks:** "Can the grader be fooled?" It reconstructs what the verifier accepts **blind** (without trusting your reference), then attacks the pass/fail boundary.

**Sound verifier = boundary exactly right:**
- **False accept (false positive)** — invalid/adversarial submission still gets reward 1. **Dangerous.** AVA catches this first (stubs, hardcodes, echo fixtures, symlink to truth, harness hijack).
- **False reject (false negative)** — valid spec-faithful submission wrongly failed (over-tight format/order/tolerance). Also a defect.

**Routing:** `pass` or `block`. Major → blocks PR. Minor → advisory only. **Empty/unparseable output = fail-closed.**

**Be your own AVA before push:**
1. Write a submission that passes **without doing the work** — stub, hardcode, echo fixtures. If you can, AVA will too.
2. Run valid-but-differently-shaped correct answers — all must pass (`no_false_rejection`).
3. Re-read reference against instruction — obeys stated **method**, not just output.

**Classic Major finding shape:**
```python
# ❌ Truth on path submission can read
expected = np.load("/app/reference_data.npz")

# ✅ Truth verifier-only
expected = np.load("/tests/private/reference_data.npz")
```

#### Don't expose the answer (official exploit catalog)

**Symlink cheat:** Agent replaces `/app/output/file` with symlink to `/tests/…`, `/solution/…`, or expected dir. Verifier follows link → reads ground truth → pass with zero work. `os.path.exists`/`is_file` **follow symlinks** — useless alone.

```python
p = "/app/output/clean.csv"
assert not os.path.islink(p)
assert os.path.realpath(p).startswith("/app/")
actual = open(p).read()
expected = load_from_sealed_fixture()  # never from agent-nameable path
```

**Re-running agent code at grade time:** Verifier subprocesses `/app/ledger_audit.py` **after** `/tests` overlay → agent code reads `/tests/data/expected/*.json` and copies golden answer. Fix: **grade artifacts already on disk** from agent run; only harness code runs at verify time; truth unreachable during agent execution.

**Docs must be true of the data (coherent contract — B6):** Documentation can be internally consistent yet **false about the data** ("exactly one row per SKU per date" when 120 duplicates exist). Agent following docs builds wrong thing through no fault of its own. Fix both: (1) make doc true OR fix data; (2) ship fixture exercising the anomaly and grade it.

#### Two failure modes (don't conflate)

| Mode | What breaks | Example |
|---|---|---|
| **Coherent contract** | Rule reads fine but is **false about the real system** | "All dinosaurs female → can't breed" (frog DNA sex change); data dictionary guarantees uniqueness data violates |
| **Sound verifier** | Check exists but **doesn't audit the full rule** | Counter stops at 238 → catches shortfall, never surplus |

Fixing one leaves the other open. Both must pass.

#### AVA quick self-check (11 items — before submit)

1. Every output field format/naming fully specified (IDs, enums, exact literals)
2. Verifier only checks what instruction (or linked doc) states — no hidden literals
3. When multiple valid computations exist, instruction names **single canonical rule**
4. Duplicate/redelivery/edge cases described explicitly (dedup key, tie resolution)
5. Reasonable alternative implementation still passes — or instruction says only one is valid
6. No agent-readable file discloses bug, fix, or expected output
7. No undisclosed file steers agent toward non-golden answer
8. No malicious/destructive code; no prompt injection in env files
9. Every `instruction.md` rule traced against **real shipped fixtures** — no contradictions on actual data
10. `solution/solve.sh` output re-read line-by-line against instruction — every field described
11. For each assertion: "could someone fake this and still pass?" → **no**

### 4C. Official human reviewer playbook (Review Tasks + Errors & Examples)

> Sourced from the Dynamo learning platform **Review tasks** submenu
> (`/reviewing`, `/reviewing/guidelines`, `/reviewing/judgment`, `/reviewing/scoring`,
> `/reviewing/recording`) plus **Errors & Examples** practice pages. Use this when we are
> reviewing someone else's task, or when pre-reviewing our own task through an R1/R2 lens.

#### Reviewer scope and order of operations

Human review is **read-only judgment**, not another execution pass. The platform has already built
the image, run oracle/nop validation, run automated static/rubric checks, and executed pass@5. The
reviewer's job is to catch what machines miss: whole-task coherence, realistic expert difficulty,
ambiguity, verifier robustness, solution legitimacy, metadata fit, and whether pass@5 failures are
valid.

**Review the exact artifact:**
1. Read approved proposal + fellow notes.
2. Record the exact latest PR commit hash before judging.
3. Open `instruction.md`, `task.toml` (difficulty / solution / verification explanations),
   `environment/`, `solution/`, `tests/`, and Dockerfile.
4. Skim commit history for manufactured difficulty (for example, a clarifying rule removed so
   agents start failing).
5. Check prior reviewer feedback first; if required fixes were ignored, that is usually Reject.
6. Open pass@5 analysis and static-check notes. Treat LLM notes as a lead list, not ground truth.

**Trust boundaries:**
- Ignore duplicate-check, validation, proposal gate, and pass@2 as review scope. pass@2 is a cost
  gate only; if a task reached review with pass@5 in 0-2/5 and valid failures, pass@2 history is
  not a reason to send it back.
- Read static checks and automated rubric notes, but override them when your file-level read says
  they are wrong. Green automated review is a floor, not a sendable verdict.
- pass@5 at 0/5 is good only when the failures are valid wrong answers, not timeouts,
  ambiguity, verifier errors, or hidden-convention traps.

#### Judgment areas (what to audit)

**Whole task:** `instruction.md`, `solution/solve.sh`, tests, environment, and Dockerfile must all
serve the same task. The oracle must solve the stated problem, not a narrower problem that happens
to satisfy tests.

**Difficulty and realism:** Hard means real domain reasoning or method judgment, not busywork,
volume, obscure recall, or a kitchen sink of arbitrary interacting rules that is impossible to
audit. A realistic task asks for outputs a practitioner would actually want.

**Instruction:** Check for over-direction, ambiguity, hidden knowledge, contradictions, misleading
or irrelevant files, and answer leakage in comments/docstrings/READMEs/filenames. Omission is not
automatically ambiguity: it becomes a blocker only when a sound expert choice changes the graded
answer and nothing visible pins the intended choice.

**Verifier:** Every assertion must trace to the instruction or an agent-visible input; every
material requirement must have a discriminating assertion. Tolerances cannot be calibrated only to
the oracle: too tight false-rejects correct alternatives; too loose admits wrong answers. Reject
NaN/Infinity, enforce exact schema/key/order/shape where required, keep deterministic seeds/order,
and scan for injection or malicious fixture text.

**Solution:** The reference must genuinely derive the answer from visible inputs and perform every
required action. Hardcoded final tables, copied expected outputs, or a reference that reports a
problem without doing the required repair are review failures even if validation passed.

**Metadata:** `category` and `subcategory` are platform-seeded; do not reward drift. `task_objective`
and `artifact_type` must be non-empty lowercase snake_case arrays from
`.dynamo/diversity-taxonomy.toml` and must be best-fit labels, not merely valid strings. If the only
issue is platform category/subcategory mismatch but the PR task is otherwise deliverable: Accept
with score 3 to log metadata drift.

#### Valid vs invalid pass@5 failures

A failure is valid only when you can point to a concrete instruction sentence, input fact, or
standard domain rule proving the agent's decision was wrong. If a competent expert could defend
the agent's approach from the package as written, the failure is invalid and the task is
ambiguous, even if the trial-analysis panel calls it valid.

**Read the trial panel skeptically:** it summarizes per-trajectory rubric, fail reasons, golden vs
agent values, failing tests, golden approach, agent approach, and validity. It is an LLM first pass
and can be misled by a wrong `task.toml` difficulty explanation. If needed, pull full logs/artifacts
from View logs & artifacts -> trials -> Upload Harbor Output.

**Fast red flags:**
- Failing tests are only file existence, naming, ordering, or formatting: suspect an undisclosed
  convention.
- All agents converge on the same wrong-looking value: first check whether the golden answer or
  hidden convention is wrong.
- Failures are timeouts or productive but cut off: not valid stumps. Tell the fellow to move
  difficulty into reasoning, not compute time, and keep timeout <= 3600s.
- pass@5 3-5/5 solved: too easy; ask for real difficulty, not lower timeout or busywork.

#### Verdict and score calibration

**Accept** only when no issues block delivery. A clean task with minor typo / grammar / one tiny
untested requirement can still be Accept score 4. A perfect task is score 5. Category-only platform
mismatch is Accept score 3.

**Revise** for a real, fixable issue where the task stays genuinely hard after the fix. Feedback
must name file/criterion/line, explain why it blocks, and state the exact required change.

**Reject** when the difficulty is illegitimate or fixing the defect would make the task easy or
require a rebuild. Reject patterns:
- Models failed on an undisclosed verifier requirement, hidden threshold, naming/order convention,
  or ambiguous term whose clarification would make agents pass.
- Instruction/input data contains false or misleading information the agent had no reason to
  distrust.
- Red herrings deliberately steer a reasonable agent away from the golden answer.
- All failures are caused by over-tight verification rejecting valid answers.
- Prior required reviewer feedback was ignored or disputed without a real fix.

**Score is quality-on-arrival, separate from routing:**
- 5 Accept: no issues.
- 4 Accept: minor non-blocking issue.
- 3 Accept: only category/platform mismatch; or Revise for a fixable blocking issue that preserves
  difficulty.
- 2 Revise or Reject: major quality issue; choose Revise only if salvaged task remains hard.
- 1 Reject: bad faith, ignored valid feedback, spam, or severe misalignment.

#### HAI recording rules

Fill the HAI form in this order: reviewed PR commit hash, Standard Quality Score, Task Verdict,
Fellow Verdict, task notes/feedback.

**Do not click Approve unless Task Verdict is Accept with zero issues flagged.** Approve routes the
task forward; it is not a neutral submit button. For Revise/Reject, flag issues, leave feedback,
then use the gray send-back option when available.

Fellow verdict is about the contributor, not the task:
- Excellent: exceptional quality already.
- Trainable: good contributor who can improve.
- Misaligned: not following project guidelines / not qualified.

Always leave actionable feedback on Revise/Reject, both in the taxonomy comment field and as file
feedback bubbles when possible. Use the R1 Other comments field only for notes that are not meant
as fellow-facing feedback.

#### Errors & Examples review lessons

Use these as concrete review lenses:

- **Coherent instructions:** Every graded field, method choice, format, edge case, and tie-break
  must be stated or derivable. Pin only the deciding choice when multiple expert methods diverge.
  If two rules cannot both hold on the shipped data, the docs are not coherent even if each rule
  reads well alone.
- **Correct oracle:** Oracle passing validation is not enough. Re-read every output field, shape,
  tie-break, and ordering against the spec; expected values should be canonical under the stated
  contract, not merely internally consistent.
- **Sound verifier:** For each assertion ask "could someone fake this and pass?" Surface-only checks
  (row counts, types, broad aggregates) are not enough. Assert parsed values, exact key sets,
  schema, dtype, ordering, and rounding when those matter.
- **Protected truth:** The verifier must compare data the agent actually wrote against truth loaded
  independently. Never recompute expected values from `/app/data` after the agent can mutate it;
  never re-run agent-controlled code after `/tests` is mounted; guard every output path against
  symlinks and path escape.
- **Runnable realistic task:** If the agent must guess undocumented oracle quirks, the task is not
  honestly solvable. Difficulty must come from reasoning, not from matching a hidden convention.

**Practice case calibrations:**
- "Save cleaned data to the output folder" and "correct and well-formatted" are underspecified
  success criteria; exact paths and formats must be named.
- `RUN pip install pandas==2.2.2 pytest` is not fully pinned because `pytest` is unpinned.
- Extra `author_name` / `email` in `task.toml` violates Harbor schema / identity policy.
- `#!/bin/bash` in `solve.sh` is correct; do not flag it just for using bash.
- `test.sh` writing `echo 1 > /logs/verifier/reward.txt` is correct only when gated by real tests
  and fail-closed behavior.
- Duplicate data that docs say cannot exist is a contract defect even when the fix is obvious:
  the agent is told not to guard against it. Fix the documentation or data, and test the anomaly.
- Do not conflate contract failure with verifier failure: a contract can be false about the world
  while the checker is otherwise sound; a checker can test "at least N" when the rule is "exactly
  N" even if the contract is honest. Both must be audited independently.

---

- **Pipeline order per push** (summary): static + eval → similarity → validation → pass@2 → deep_review ∪ AVA (adversarial advisory) → tier1 (if prior QC fail) → qc_eval ∪ qc_exec → qc_gate → pass@5 → gate.
- **pass@5 fail taxonomy**: needs **≥3 counted fails with ≥1 anchor**. Anchor = a clean reward-0
  wrong answer OR a stuck wedge (zero output, approach not judged invalid). Soft timeouts
  (productive work cut off) only FILL once one good valid fail exists; in-progress timeouts and
  infra/setup errors don't count at all. **0/5 solved with 0 valid fails (all timeouts) BLOCKS**
  even at avg 0.000 — watch the breakdown line, not the pass fraction.
- **The gate is a noisy draw.** Each push redraws. Push-to-redraw is legitimate once per-trial
  fail odds ≥ ~20% (p≈0.4 → P(≥3/5)≈0.32 per draw); worthless below. Redraws are API-expensive
  (one session exhausted the monthly org LLM quota — all stages fail-closed for hours). Never
  push while trials are live (cancels the run); batch hardening into ONE push and build the next
  increment locally during the run.
- **pass@2 does not predict pass@5** (0/2 → 4/5-solved happened; the reverse too). pass@2 uses a
  rotating, sometimes weaker model. A 2/2-solved pass@2 is a genuine too-easy block — ratchet,
  don't re-roll. pass@2 daily cap: 6 runs/day/task, resets UTC midnight. A push while pass@2 is
  green but pre-trials REDRAWS pass@2.
- Fork authors cannot `/rerun` (needs upstream write; `gh run rerun` 404s) — a push to the fork's
  `submission` branch is the only redraw lever. Difficulty-neutral vehicle: README note.
- Diagnosis heuristics from the pass@2 "Agent Approach" section: solving fast → add derivation
  difficulty/breadth; timing out while productive → remove mechanical volume, keep derivation.
  Solve TIME (not just rate) is the go/no-go for the machinery lever.

---

## 5. Repo layout, workflow, commands

### Required layout (everything under `task/`)
```
task/
├── task.toml            # manifest — you fill metadata + timeouts
├── instruction.md       # the ONLY thing the agent sees; absolute /app/... paths
├── solution/solve.sh    # reference (Oracle) solution + helpers; NEVER in the agent image
├── environment/
│   ├── Dockerfile       # the SINGLE image (agent + verifier)
│   ├── .dockerignore    # REQUIRED if environment/ has subdirs (data/) — first commit
│   └── data/            # seed files COPYed to /app
├── tests/
│   ├── test.sh          # runs pytest, writes reward 1/0 to /logs/verifier/reward.txt, exits 0
│   └── test_outputs.py  # 1:1 with instruction.md; ground truth lives HERE, never environment/
└── .dynamo/ .github/ .harbor/   # provided — do not edit
```

### Core commands
```bash
# Fork + branch
gh repo fork handshake-project-dynamo/<repo> --clone
git checkout -b submission
# Local validation (from task/)
harbor run -p . --agent oracle    # must score reward 1.0
harbor run -p . --agent nop       # must score reward < 1.0
# Image cleanliness
docker run --rm <image>:dev /bin/bash -lc 'find / \( -name solve.sh -o -name test.sh \) 2>/dev/null'  # expect empty
# Sanity
python3 -m py_compile task/solution/*.py task/tests/*.py
git diff --check
# Submit + monitor
gh pr create --repo handshake-project-dynamo/<repo> --fill
gh pr checks 1 --repo handshake-project-dynamo/<repo> --watch
gh run view <run_id> --repo handshake-project-dynamo/<repo> --json status,conclusion,jobs
gh run view <run_id> --repo handshake-project-dynamo/<repo> --log-failed
gh pr view 1 --repo handshake-project-dynamo/<repo> --comments
```
- Always push to the same `submission` branch / same PR. When `origin` is the upstream (403s),
  push to the fork remote: `git push fork submission`.
- Read the PR comment + failed job logs before editing; fix the stated reason, not a guess.
- Sticky PR comments are edited in place (createdAt stays at first run) — check a run-specific
  detail, and read the JOB LOG for counts (sticky comments truncate finding text).
- `harbor run` drops a `jobs/` dir in the repo — delete before `git add -A`. Never stage
  `__pycache__`/`*.pyc` (fails `no_extraneous_files`).

### instruction.md / task.toml rules
- instruction.md: human-written, prompt-style (no headers/roleplay), absolute `/app/...` paths,
  names every output file + exact format, WHAT not HOW, ≤1,500 tokens.
- **LIVE-RUBRIC OVERRIDES (the cached official guide is stale on these):**
  - instruction.md must **NOT** end with the "You have N seconds…" sentence — the TB3 rubric
    fails `instruction_concision` on it. Follow the live scaffold over the guide.
  - **Never set `allow_internet = false`** — the live `open_internet` criterion fails offline
    requirements.
- task.toml: `category`/`subcategory` are pre-seeded — never edit; `model_tested`/`agent_tested`
  fixed; you set `task_objective` + `artifact_type` (snake_case arrays from
  `.dynamo/diversity-taxonomy.toml`), `expert_time_estimate_hours`, and the three explanation
  fields. No author identity anywhere. **Every count/statistic quoted in task.toml/README must
  match the actual shipped data — deep_review `metadata_reality_alignment` blocks on drift, and
  any fixture regeneration invalidates every quoted number.**
- Dockerfile: allowlisted base pinned by `@sha256:` digest; pin pip/npm exactly, never apt; no
  heredocs; `RUN mkdir -p /app`; never COPY `solution/` or `tests/`; static checks grep for the
  literal strings `solution/` and `tests/test.sh` even inside comments. Note: the static
  pip-pinning check tokenizes the whole RUN line — `pip install ... --retries 5` fails as
  "unpinned ['5']"; use `ENV PIP_RETRIES=5` instead.

---

## 6. Verifier-hardening kit (ship ALL of this from commit 1)

Each item below was earned by a past blocking round; the full combo pre-cleared AVA and qc_gate
first-try on four consecutive tasks.

1. **Pytest isolation** (defeats qc_gate E3 "harness plumbing exploit" — a root agent planting
   `/conftest.py`):
   ```bash
   /usr/bin/python3 -m pytest --noconftest -p no:cacheprovider --rootdir=/tests \
       --confcutdir=/tests -c /tests/verifier.ini --ctrf /logs/verifier/ctrf.json \
       /tests/test_outputs.py -rA
   ```
   Write `reward.txt = 0` FIRST (fail-closed); use the absolute interpreter (defeats PATH shims).
2. **Reference digest pins**: `tests/reference_pins.json` = authoring-time in-container SHA-256 of
   every reference-produced file per graded seed; verify-time grading fails closed unless output
   reproduces the pins (defeats interpreter trojaning — AVA `verifier_coverage`).
3. **Delete-oracle**: stage all fixtures + expected values in memory, then `os.remove` the
   reference + generator + ground truth + `__pycache__` from `/tests` BEFORE the first tool run
   (a delegating/copying tool then crashes → reward 0). Also run the tool on a pristine
   regeneration of the shipped fixture.
4. **Isolation of tool runs**: privilege-drop to uid 65534 (nobody), scrubbed env, isolated cwd,
   copied tool file, `/tests` + pristine fixture dirs chmod 0700, work dir chmod 0755
   (`tempfile.mkdtemp` creates 0700 — the nobody-user tool can't traverse it and `os.walk`
   silently returns nothing; only in-container testing catches this).
5. **Compute the reference BEFORE (or independently of) the agent-tool run** — never after the
   untrusted tool has touched the tree (held-out oracle poisoning).
6. **Anti-tamper**: O_NOFOLLOW on graded outputs, reject symlinks at artifact paths, pin all
   grading parameters from ground truth (never from agent-rewritable files), enforce set-equality
   both directions, hash-pin protected inputs, reject NaN/Infinity on graded numerics.
7. **Determinism**: no `os.urandom`/`secrets`/`SystemRandom`/unseeded randomness anywhere in the
   graded path (qc_gate fails nondeterministic graded data — even a vestigial `os.urandom(0)`);
   use ~16 fixed held-out grading seeds disjoint from shipped seeds (`tests/` overlays only at
   verify time, so fixed held-out seeds are already unseen). Exception: a single
   `random.SystemRandom()` verify-time *generalization probe* is a legitimate answer to AVA's
   "a lookup table would pass" — only after fuzzing reference vs referee (100k+ records, zero
   divergence), reporting the seed in the assertion message.
8. **§-maxima witness**: exercise the EXACT documented bounds (max chunk count, candidate count…)
   on the shipped fixture, machine-checked — the mutant sweep misses dimension/cap classes;
   AVA `sound_verifier` doesn't ("all seeds had max 3 but the contract guarantees ≤4 — a ≤3
   hardcode passes").
9. **Ship the mutant sweep as a verify-time test** (the reusable answer to an AVA
   `verifier_coverage` block): N single-rule source substitutions applied at verify time, each
   required to be REJECTED on shipped + one unseen seed (crashes count as detected), with
   anchor-match assertions so refactors can't disarm it, plus a non-vacuity test that every
   workspace witnesses each graded outcome.
10. Hygiene: `.dockerignore` + `.gitattributes` (`data/** binary`) + pinned base digest +
    py_compile + `git diff --check` in the first commit.

---

## 7. QC / AVA / deep_review fix patterns

> **Stage definitions:** Section 4A. **Official 30 checks, 5 strategies, AVA doctrine:** Section 4B. This section is the **fix cookbook** — apply the recipe matching the check ID from the sticky comment.

### The QC evaluation (30 official Major IDs; qc_eval runs ~37 variants; qc_gate adds execution probes — ANY Major fails)
Families: **A** solution/oracle correctness (oracle fails own verifier, incomplete reference,
hardcoded answers, hidden/privileged access, undocumented assumptions, edge-case bugs) ·
**B** contract coherence (ambiguity, contradiction, missing definitions, undocumented enforced
requirements, underdetermined mappings, unstated anomaly policy) · **C** verifier rigor (stub
output accepted, over-permissive tolerance, hardcodable held-out coverage, truth recomputed from
agent-writable inputs, NaN bypass, scoring mismatch) · **D** fixtures/determinism (degenerate or
malformed fixtures, build failures, nondeterminism, unseeded build-time randomness) · **E**
anti-cheat (readable oracle, unpinned inputs, harness exploits, root secrets, symlinks, unsafe
extraction, copied-oracle deliverables). Core principle: **everything graded must be derivable by
the agent from instruction.md + environment/ + shipped examples, and the verifier must
independently enforce every structural requirement, not a proxy.** "Near-correct / immaterial /
intended difficulty" are not valid defenses.

### qc_gate C3 (the clause-by-clause coverage prober) — recipes
The C3 prober iterates every normative SPEC clause and CRAFTS discriminating instances. Every
clause needs a deterministic discriminating fixture on every graded seed:
- **Layered precedence** → plant ONE key with a distinct value at EVERY layer (the prober mutates
  layer order).
- **Order-sensitive rules** → ≥3 elements under a NON-involutive permutation (2 elements are
  never enough: reversed == sorted).
- **"Summed over all X"** → a witness in each X-subclass the sum ranges over.
- **Boundary constants** → a fixture at exactly the boundary (a file of EXACTLY min_bytes; a
  commit at exactly `newest − keep_within`).
- **Every literal the contract spells out** → the prober tries case-fold and delimiter-position
  variants (`rfind` vs `find` on dots, uppercase literals) — witness those families pre-emptively
  (two-dot names, trailing-dot siblings, `Sandbox` vs `sandbox`).
- **`A and B` predicates** → plant (A,¬B), (¬A,B), (A,B).
- **Single-fixed-value parameters** → vary per held-out seed (anti-hardcode); which row/record
  drifts must vary per seed too.
- **Rarely-taken-branch constants** (reverse-engineering tasks) → deterministic boundary probes on
  a fixed stride so every threshold is straddled from both directions, RNG-stream-preserving;
  then check the OUTPUT distribution (clamp saturation destroys signal — keep clamped rows <10%).
- **Untestable conditionals** ("present iff…") → remove them (make dirs ALWAYS present) rather
  than witness them; for provably-equivalent rules, reword the clause as a *consequence* so a
  clause-prober doesn't find an unobservable requirement.
- Force coverage deterministically with `_self_check` asserts in the generator.

### AVA patterns (see also Section 4A — `ava_review`)
- AVA hunts **CONSTANT graded facts**: any rule whose correct answer is identical on every
  instance is hardcodable → draw a per-seed property vector and choose held-out seeds by SEARCH
  for property balance (each branch of every property ≥2× across graded seeds).
- AVA attack enumeration is **stochastic** — identical code can pass one task and block another.
  Pin/harden pre-emptively.
- AVA can block on noise (findings whose own evidence shows agreement) — hand-verify, push a
  benign redraw commit + explanatory PR comment; don't change grading.
- When an auditor flags a pattern, **remove the pattern entirely** — don't substitute a
  same-family pattern (swapping `importlib` for `exec(compile(...))` blocked harder; the fix was
  subprocess).
- Over-strong instruction claims ("single self-contained executable") create enforcement burden —
  delete the claim rather than police it.
- `no_false_rejection`: parse agent output leniently (`json.JSONDecoder.raw_decode` streaming,
  not line-splitting).
- deep_review blocks the mirror image of AVA: a decisive rule not discoverable → state it in the
  spec AND ship a witnessing sample. Fix deep_review *advisories* immediately — QC probes
  escalate them to blocks later.
- Adversarial cheat-pass reads the **git repo, not the container** — "generator/seeds are
  agent-visible" can be a false positive; verify the built image and never adopt
  nondeterministic-seed suggestions.

### tier1 mechanics (see also Section 4A — `tier1`)
- A D-finding naming a file (e.g. "D3 Environment Build Failure" logged for a transient infra
  flake) clears ONLY on a real diff to that exact file — an empty commit reads as "0 files =
  fix not attempted". Make a small defensible edit (`ENV DEBIAN_FRONTEND=noninteractive`,
  `PIP_NO_CACHE_DIR=1`…).
- tier1's base_sha is pinned at the finding commit and never advances; its cumulative diff
  truncates at ~60 files, so a regenerated fixture can push your fix out of view → "not
  attempted" → HOLD. Real fix: **shrink the cumulative diff itself** — `git checkout
  <pinned-base> -- <bulky fixture paths>` (grading is differential, so restoring an older frozen
  fixture is free). Land each QC-required fix in its own small commit; never bundle with fixture
  regeneration.

---

## 8. Local validation before every push (the first-commit-all-green recipe)

1. **Independent forward generator** that records design intent by construction, plus an
   **xcheck**: reference ≡ generator-intent across 40–105 seeds; promote the xcheck into the
   verifier as a test.
2. **Full mutant sweep** (30–90 single-rule mutants of the reference), with discipline:
   - Every mutant must die on the SHIPPED fixture AND ≥1 held-out seed (two-sided);
     bidirectional (every fixture also catches some mutant).
   - Include a **no-op control mutant that must score 1** (else a broken harness silently
     reports all mutants caught). Check mutant patches for build errors (an invalid-Python
     mutant is not "caught"). Hand-diff one mutant to sanity-check a 100% sweep.
   - A surviving mutant almost always means a fixture hole — fix by ADDING a witness, never by
     dropping the mutant; unless provably equivalent, then delete/reword the rule. Degenerate
     held-out fixtures (empty/one-item "bare" profiles with per-mutant seed sets) bind edge-case
     rules cheaply; mark them heldout-only.
   - Re-run the FULL sweep after EVERY generator change (RNG streams shift; witness geometry
     re-randomizes); re-scan seed properties too.
   - Rewrite crash-only mutants to produce output; ≥2 fixed seeds per mutant.
3. **Structural completeness invariants**: whenever an output enumerates/partitions the input,
   assert totality + disjointness ("every record is quarantined or surviving exactly once").
   Two same-author implementations can slip IDENTICALLY — differential agreement proves nothing.
4. **Fixture-authoring rules that recur**: construct witnesses parametrically from config values,
   not seed luck; reserve trap-hosting entities ("its only anchor is X") OUT of the random filler
   pool; realm/dir names must not sort in precedence order (else precedence is undiscriminated);
   the correct candidate must not sort first (rename `zz_…` to sort last); decoy keys before real
   keys; identical-start collision groups need explicit fixed entries, not rng; syntactically
   valid bad variants for malformed-input rules; route degenerate cases through the REAL code
   path; keep the decisive contract section past ~10KB (naive `cat` truncation is an accidental
   kill); a body shuffle can destroy order-sensitive gadgets — assert gadget properties in
   `_self_check`.
5. Staged **no-docker fallback** (when Docker is down): stage a fake `/app` in a temp dir,
   `sed 's#"/app#"<stage>/app#g'` the test file, copy tests/ helpers alongside, run pytest from a
   venv. Run harness tools from the dev dir with absolute paths (cwd resets between shell calls).
6. In-container: oracle 1.0 / nop 0.0 **with all hardening active** (deletion, privilege drop,
   planted `/conftest.py` + pytest.ini + PATH-shim attacks simultaneously); image scanned clean.
7. The solution's copy of the reference must be **regenerated after every reference edit** (a
   stale copy scored oracle 0 twice); it needs a shebang + `install -m 0755`.
8. **Frozen fixtures must never be regenerated from an evolved generator** (would expose held-out
   traps); the shipped tree is a frozen subset — restore, don't regenerate.

---

## 9. Engine porting / reskinning (the highest-yield workflow)

- A domain reskin of your own proven ALL-GREEN engine clears the similarity gate (UNIQUE) as long
  as domain + vocabulary + field names + prose differ. The similarity check compares against
  public TB2/TB3 only, not your Dynamo siblings.
- Build a full **vocabulary map** (every noun, extension, sidecar separator, record magic, status
  name, report key); optionally reorder binary headers/opcodes.
- **Always add 1–3 genuinely NEW rule families** (distinctness + fresh kill surface), and ship at
  the mold's FINAL post-ratchet strength, not its starting strength.
- Rename mechanically with ordered PLAIN string substitutions, longest/riskiest first (`signed`
  before `sign`; never regex `\b` — underscore compounds don't match). Hand-write
  CONTRACT.md / instruction.md / task.toml.
- ALWAYS re-run the full mutant sweep on the ported fixture — reskins reliably expose 2–8 real
  coverage holes.
- Typical accepted config: agent 3600s, verifier 300–1500s, held-out 4–5 seeds, differential
  grading on pristine copies, fixture ~300–700 files, report 13–23 exact counters.
- **Empirical addendum (a3f35ff chain, dynamo-64a5641, 2026-08-07): mechanical substitution beats
  self-match but is fragile in ways a green mutant sweep does NOT catch.** Confirmed on a single
  task across four consecutive reskins: every push that left `instruction.md` + `tests/test_outputs.py`
  byte-identical (or near-identical, joined bag-of-words cosine ≥0.9) to the immediately prior
  **evaluated** head blocked `cosine_similarity` in ~11s — including a pure bugfix commit with a
  correct, non-trivial code change. **This means every push needs a fresh identity shift, not just
  the first one after a block** — a follow-up "just fix the one bug" commit is not exempt.
  - Ordered plain-string substitution (as prescribed above) is real and works for `solve.py` /
    `tests/_*_kit.py` (Python double-quoted literals match the rule), but it silently **misses any
    bare-word literal that isn't inside a compound identifier** — table headers (`"plan\tfinish\t..."`
    with `finish` as a standalone token, not `finish_mode`), byte-marker constants (`b"BLOCK\n"`
    left un-renamed after `block`→`frame` only had compound rules), and — critically — **markdown
    backtick-quoted text in `instruction.md` is invisible to double-quote-literal rules** (`` `whole` ``
    in prose vs `"whole"` in Python never match the same substitution). Two separate pushes were
    blocked by Dynamo eval `#6 unambiguous` / `#13 test_instruction_alignment` from exactly this:
    the instruction disclosed one literal (e.g. a TSV column name) while the code/verifier emitted
    a different, stale one.
  - Substring collisions are common and dangerous: `base`→`X` breaks `import base64`; `strip`→`X`
    breaks `.strip()`; `ply`→`X` breaks `apply`; `plies`→`X` breaks `supplies`; `back`→`X` breaks the
    idiom "back into"; a protection-token pattern (`old→"@@TOK@@"` first, `"@@TOK@@"→old` last in the
    substitution list) is required for every renamed word that is a real-English-word substring.
  - **The two graded facets (`instruction.md`, `tests/test_outputs.py`) are safest when fully
    REWRITTEN from scratch each reskin, not mechanically substituted** — this is what the two
    pushes that passed cosine on the first try both did; the one push that used substitution on
    `instruction.md` introduced the header-mismatch defect. Code files (`solve.py`,
    `tests/_*_kit.py`) are fine to substitute since their literals are consistently double-quoted.
  - When two *different* concepts happen to share the same literal word pre-reskin (e.g. an output
    directory name `"stitched"` and an unrelated outcome-enum value also spelled `"stitched"`), a
    single substitution rule renaming one will silently corrupt the other. Grep every renamed
    bare-word literal's *other* occurrences before trusting the reskin.
  - **A "0 survivors" mutant-sweep result is not sufficient after a reskin** — report the **build
    count** too (how many of N mutation anchors' `old` string actually matched the post-reskin
    source) and treat `built < N` as a hole: the reskin silently no-opped an anchor whose literal
    it renamed. Port the mutation table through the same substitution list used for the reskin.
  - A cheap **self-similarity guard** (word-tokenized bag-of-words cosine, NOT punctuation-inclusive
    — that overstates similarity — of the new `instruction.md`+`tests/test_outputs.py` against the
    last 5–6 evaluated heads on the branch, HEAD included) run locally before every push predicts
    the gate outcome well: pushes that blocked measured ≥0.90 joined; pushes that passed measured
    ≤0.76. It is necessary-but-not-sufficient signal, not a guarantee, but catches the "I only
    changed the code, not the two graded files" mistake before wasting a push.
  - Every backtick/quoted key, enum, and container literal named in `instruction.md` should be
    grepped against the actual `solve.py` emission before pushing — do not trust memory when
    hand-writing the instruction fresh; a hand-written instruction can just as easily disclose a
    stale or simply wrong literal as a mechanically-substituted one did.

---

## 10. Infra / ops gotchas

- **Daytona outages** (`Failed to create snapshot: Access denied`, `DaytonaAuthorizationError`)
  recur for multi-hour stretches; zero task signal; ride out with empty-commit redraws on
  escalating backoff (~every 2h). Daytona snapshots are content-addressed — a Dockerfile change
  mints a fresh snapshot ID, sidestepping a poisoned cache.
- **Enforced cosine (`review / cosine_similarity`):** compares only `instruction.md` +
  `tests/test_outputs.py` (64 KiB cap), threshold usually `0.9`. Once the org flips this gate from
  shadow → enforced, it blocks **every** subsequent push until both facets clear. The checker can
  also match against this PR's **last ~3 commits** / stored lineage snapshots, so empty redraws,
  docstring-only edits, and tiny wording patches fail immediately even if an older sticky said
  UNIQUE. **Before every push**, agents must re-check the cosine sticky and confirm both compared
  files get a load-bearing contract change vs those recent SHAs (see `AGENTS.md` mandatory
  checklist). Sticky "too similar to a delivered Dynamo task" is a real flag — empty commits never
  clear it. Fix in one push that diverges from those recent SHAs: **new schema** graded
  artifact/contract (not another rename of the same flat sidecar) + instruction desk rewrite +
  solution/reference wiring + reshape `test_outputs.py` (module name/import style/test names), then
  Harbor oracle/nop. Sidecar rename chains (`*_audit` → `*_ledger` → `*_profile` without schema +
  prompt + entrypoint divergence) self-match the PR's last ~3 commits — see `AGENTS.md` hard ban.
  HTTP/401/503/000 or Actions download failures are infra, not duplicates. Shadow scores ≥0.9
  foreshadow the next enforced block.
  **Empirical correction (df4e109, 2026-08-07):** the "diverge vs recent SHAs" rule is NOT
  sufficient once a version has been ingested. On df4e109, after commit A passed cosine and ran
  pass@2, a later commit that (i) added genuinely NEW mechanics (`move` + `guard` subsystems),
  (ii) fully REWROTE `test_outputs.py`, and (iii) fully PARAPHRASED `instruction.md` STILL failed
  cosine. Embeddings match **meaning**, and it was the same task, so it self-matched ~1.0. Only a
  genuinely different task (new schema/domain/mechanics — effectively a rebuild) or a platform
  same-repo/self-exclusion fix escapes it. So: reword/rewrite is worth ONE attempt for real
  sibling overlap (move the shared verifier boilerplate into a private `tests/_harness.py` helper
  so the compared `test_outputs.py` facet is thin+distinct); if it still blocks, it is
  self-ingestion — **stop, flag the platform owner, wait.** Canonical detail: Section 4A
  `cosine_similarity`.
- **Similarity/static loop:** if one pushed SHA clears enforced similarity but fails static token
  count, do not make the next SHA a prompt-only trim. Preserve Qwen3 token margin and also reshape
  the compared verifier harness with a real coverage improvement; otherwise the unchanged verifier
  can compare against the prior PR SHA at ~1.0 and block before validation.
- Harbor first run: 10-min EnvironmentStartTimeoutError = cold docker cache (long base pull) —
  `docker build` manually to warm it; on macOS a dead Docker Desktop VM shows the same error.
- `docker run` heredoc stdin needs `-i`.
- Org LLM workspace budget can exhaust mid-month (`API Error: 400 … regain access on …`) — all
  LLM stages fail-closed; flag an admin; don't spam redraws.
- `ava_review` "Set the DYNAMO_EVAL_API_KEY repo/org secret" = platform provisioning gap; flag an
  admin.
- QC checks rollout (2026-07-26): un-submitted tasks must push a new commit (empty ok) to get the
  latest QC checks; stuck submitted tasks were auto-reprocessed — don't close the PR or recommit
  while processing.

---

## 11. Proposal & platform submission

### Proposal (approved before building)
Must explicitly cover: pre-seeded Category/Sub-Category verbatim (fetch task.toml via
`gh api repos/handshake-project-dynamo/<repo>/contents/...` — repos are private); the exact
professional who does this work; why it's valuable; synthetic-vs-real data and how synthetic
stays realistic; the specific pitfalls that cause wrong solutions (the mechanism, not "this is
hard"); the intended approach + key insight; expert time estimate ("~N h for a senior <role> who
holds the <X> insight"); exact output artifacts (paths/formats); exact verification method
(what's compared, tolerance and why); category justification. The proposal must match the
sub-category's center of gravity (a caption task under "Audio and music processing" is an
instant blocker — it must be real audio work).

### Platform form (after ALL-GREEN)
- **Artifact type** (multi-select): pick what the agent inspects/produces as end deliverables,
  never the incidental tool. Frequently used: `single_script_or_program`,
  `archive_or_compressed_artifact`, `media_artifact`, `generated_output_artifact`,
  `text_or_log_file`.
- **Task objective** (multi-select): the accomplish-verb; frequent: `recover_or_repair_artifact`,
  `analyze`, `transform`, `implement`, `generate`.
- **pass@ score** = the count of SOLVED trials from the latest non-superseded PR comment
  (0–2 is the GOOD outcome). Screenshot the pass@ comment and attach.

### PR monitoring
- When multiple GitHub accounts are cached locally, treat `gh auth switch` as global mutable
  state. Run private Dynamo PR polls as short serial commands prefixed with the intended account
  switch, e.g. `gh auth switch --hostname github.com --user utkarsha01 && gh pr checks ...`.
  Do not parallelize `gh` polling across accounts; GraphQL 404s may be account drift, not repo or
  pipeline failure.

### pass@ ambiguity fixes
- If pass@ feedback shows agents solved the main artifact but failed a report convention, pin that
  convention directly in the prompt and visible fixture notes. For path-valued fields, name the
  frame for each one: manifest-relative, output-root-relative, input-root-relative, or absolute.
- When the ambiguity fix makes the task easier, add a fair disclosed subsystem that interacts with
  real task behavior and is witnessed visibly and in protected tests. Avoid pure formatting ratchets.

---

## 12. Track record (calibration data)

| Task | Domain | Result | Winning lever |
|---|---|---|---|
| restitch | Recovery/repair | 1/5 (0.200) | Mold flagship: evidence consumption + floating-fragment assignment + FIX renames |
| shoot-mend | Recovery/repair | 1/5 (0.200) | 3 ratchets 4/5→3/5→1/5; report-side slips + mined offsets |
| resplice | Recovery/repair | 1/5 (0.200) | restitch reskin (audio); 14→17-count ratchet flipped a 2/2 |
| recue | Recovery/repair | 2/5 (0.400) | entanglement ratchet (3-step cue derivation); mutant-sweep-as-test cleared AVA |
| reweave | Recovery/repair | 1/5 (0.200) | MERGE grafts + locale routing × collision ordinals, one push 4/5→1/5 |
| remaster | Recovery/repair | (shipped) | reweave port + head/tail trim handles + MANIFEST.tsv; 8 pre-push sweep holes |
| rebank | Recovery/repair | (in flight) | binary deliverable + quarantine/graft; trim-by-fail-analysis |
| depot-mend | Release artifacts | 0/5 (0.000) | shoot-mend mold ported; value-source-differs report fields |
| finish-run | CI/CD | 1/5 (0.200) | depot-mend port; survived 3h Daytona outage + tier1 catch-22 |
| close-cycle | CI/CD | 0/5 (0.000) | finish-run reskin; reference-pins recipe born here |
| reforge | CI/CD | 1/5 (0.200) | first-commit all-green; restitch engine in CI skin |
| tier-collapse | CI/CD | 1/5 (0.200) | strata-squash engine in build-cache skin; sample-timing counters |
| trim-ledger | CI/CD | 1/5 (0.200) | spool-compact engine in run-ledger skin; forged-fin corrupt RUN record |
| relay-mend | Config repair | 0/5 (0.000) | port-rota engine + 3-pass scrub undone in reverse order |
| port-rota | Porting/migration | (shipped) | 7 guide-vs-corpus drifts; the QC/AVA/tier1 encyclopedia |
| legacy-accum-port | SW engineering | 0/5 (0.000) | binary32 double-rounding + signed-zero bit-exactness |
| infer-release-gate | CI/CD (RE) | 0/5 | first reverse-engineering clear; non-linear score wall |
| infer-rollout-gate | CI/CD (RE) | 0/5 (0.000) | 7-field profile; anchor-vs-timeout tuning saga |
| infer-release-promotion | CI/CD (RE) | (shipped) | boundary probes for rarely-taken branches; mutation-sweep-locally recipe |
| spool-compact | Archiving | 1/5 (0.200) | THE volume case study: ~18 distinct rules → 50-min solves |
| strata-squash | Archiving | 1/5 (0.200) | MOVE + keep ratchet flipped 3/5→1/5 in one push |
| lyrb-bundle-flatten | Format conversion | 2/5 (0.400) | accounting-report lever after render-volume plateaued |
| quire-convert | Format conversion | 0/5 (0.000) | NEW engine; >90%-budget do-not-ratchet rule validated |
| chunked-vault-recover | Recovery/repair | 1/5 (0.200) | v1 spec-task solved in 5 min → v2 mold port; filler-cut lesson |
| capture-reindex | Recovery/repair | (advanced) | sessions re-keyed the algorithm — kind beats quantity |
| atlas-rebake | Image processing | 0/5 (0.000) | mined per-rig colour bias; won by NOT ratcheting |
| studio-reflow | Batch rename | 2/5 (0.400) | breadth ratchet + idempotency traps; TB3 rubric deltas learned |
| redline-consolidation | (docs) | 1/5 (0.200) | full playbook from day one → first-commit all-green |
| rotate-sweep | File search | (grind) | subcategory near-unstumpable; glob traps; frozen-fixture rule |
| ferryman (455e837) | Games/sim | 0/5 | six constants deferred to a corpus that uniquely pins them |

**Bottom line:** what earns the score is breadth of exact-integer accounting + byte-exact naming +
operational irreversibility + evidence-mined parameters — agents solve every *intended* clever
crux; they die on peripheral exactness and on having destroyed their only copy of the data.
