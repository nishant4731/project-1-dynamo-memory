# Handshake Dynamo Form — dynamo/recover-atlas

PR status: **accepted**  
Date: 2026-08-01

---

## PR URL

```
https://github.com/handshake-project-dynamo/dynamo-1f78c32-machine-learning-and-ai/pull/1
```

## Accepted commit SHA

```
0320f12caaaa52c495ce92c5f10ae078fb6147c4
```

---

## Step 1 — Proposal

Keep the category/sub-category text the form already shows. Paste everything below into the rich text editor.

```
Category: Software Engineering
Sub-category: data recovery / event-log parsing / algorithmic reconstruction
Task: dynamo/recover-atlas — Recover Atlas

PR: https://github.com/handshake-project-dynamo/dynamo-1f78c32-machine-learning-and-ai/pull/1
Accepted commit: 0320f12caaaa52c495ce92c5f10ae078fb6147c4

What this task actually is

Deterministic software engineering: parse and validate a JSONL event store, identify affine adapter parameters from calibration probes over mod 1000003 (system identification, not statistical learning), apply documented tie-break rules, and propagate vectors through a finite-field graph to exact integer counters and probe outputs. There is no model training, autoencoders, PCA, clustering, contrastive learning, or embedding optimization.

Who does this work and why it matters

A data-recovery or platform-forensics engineer rebuilds a crashed event-sourced index from logs when only partially corrupted records remain. The deliverable is a reusable recovery CLI plus an exact audit JSON.

Documented conventions (no undisclosed oracle secrets)

Every convention the verifier checks is stated in the agent-visible instruction; /app/atlas/README.md points back to it:

1. Event digest (instruction.md): digest equals the first 20 hex characters of SHA-256 over the JSON object without digest, sorted keys, compact separators (",", ":").
2. Signed coordinates (instruction.md): subtract field_modulus 1000003 only when residue > 500001.
3. Bucket token (instruction.md): mix = sum((i+3)*s[i]) mod 997; bits has bit i set when s[i] < 0; norm = (sum(abs(s[i])) // 113) mod 251; format B{mix:03d}-{bits:02x}-{norm:03d}.
4. Output schema and all 14 report counter definitions (instruction.md).
5. Atlas README (/app/atlas/README.md): calibration-driven adapter inference, event-order propagation, mixer edges, fill tie-break including record_id, counters computed from all records.

Concrete adapter-lane example (the crux that trips agents)

For model m0 coordinate lane 0 on a visible calibration row with tick=18, the card has bias=6526, drift=9, gain=5, sign=-1, and encoded_delta[0]=33788. The correct decode evaluates raw = mod(33788 - 6526 + drift_dir * 9 * 18) before gain inversion and sign routing to match the signed true_delta. Agents that treat drift as a constant additive shift (ignoring * tick) get zero matching policies across all 87 calibration rows even when visible propagation looks correct.

Corpus bounds (tractability)

Visible atlas: 155 event rows, 87 calibration rows, ~42 KiB total. Protected hidden atlases: dimension 5–7, ≤211 event rows, ≤99 calibration rows, ≤54 KiB each. Policy search is at most 7 routing targets × 8 drift/gain/sign modes per coordinate checked against ≤99 rows — well within the verifier's 20 s subprocess timeout per atlas (180 s verifier budget total).

What the agent must produce

1. /app/recover_atlas.py — reusable CLI: python3 /app/recover_atlas.py <atlas_dir> <output_json>
2. /app/atlas_answer.json — exact recovery report for the visible corpus in /app/atlas

Why this is genuinely difficult

- Adapter parameter identification from calibration probes (constrained search, not ML training).
- Dimension generalization: visible dim=6; hidden tests use dim=5 and dim=7; hardcoding range(6) crashes on hidden corpora.
- Mixer edges: dst = src + mix*pivot + delta; recover any missing endpoint via field inverse of mix.
- Fill tie-breaks and partial repair with record_id as final tie-break.
- Exact accounting: all 14 report counters must match reference outputs field-for-field.

Intended solution approach

1. Validate digests per the documented SHA-256 rule; drop retractions; order by (tick, seq, record_id).
2. Identify adapter policies from calibration rows (unique policy matching every row, drift scaled by tick).
3. Repair null edge coordinates via documented fill tie-breaks.
4. Propagate through ordinary and mixer edges until convergence.
5. Emit signed probe vectors, documented bucket tokens, and exact report counters in recover_atlas.py.

Expert time estimate: ~4 hours for an engineer experienced in event-log recovery and finite-field graph propagation.

Verification plan

The verifier uses an independent reference_recover() implementing the same fully specified deterministic rules:

- Compares visible /app/atlas_answer.json with recursive type-strict JSON equality on every schema field, probe, token, and report counter.
- Rejects symlinked, malformed, or stub outputs.
- Runs the submitted tool on three protected generated atlases. Each hidden corpus varies all 14 report counters (for example unfilled_edges 3–4, deferred_edges 2–3, conflict_edges 2–3, bad_digest 4–6), so partially correct solvers cannot pass by hardcoding common visible values.
- Confirms digest, signed-coordinate, and token rules follow instruction.md — no undisclosed convention is required.

Category justification

Software Engineering — data recovery / event-log parsing / algorithmic reconstruction. The work is deterministic parsing, constrained parameter identification, and graph propagation over a prime field, not representation learning.

Accepted result

The PR is marked accepted. The final pipeline passed static checks, duplicate/similarity review, validation, pass@2, deep review, adversarial review, AVA review, pass@5 trials, and the final gate.

pass@2: 0/2 passed
pass@5: 0/5 passed (avg@5 = 0.000)
Breakdown: 0 solved, 5 good valid failures, 0 soft-timeout failures

This satisfies the difficulty gate (0-2/5 solved with ≥3 valid failures).
```

Then: **Save** → wait for "Changes saved" → **Submit**.

---

## Step 2 — Repository / workflow

PR is already complete and accepted. **Submit** this step.

---

## Step 3 — Artifact type (multi-select)

```
Single script or program
Dataset or tabular file
Generated output artifact
```

Then **Submit**.

---

## Step 4 — Task objective (multi-select)

```
Implement
Recover or repair artifact
Analyze
```

Then **Submit**.

---

## Step 5 — Screenshot + pass@ text

**Screenshot:** attach the latest pass@5 PR comment showing `pass@5: 0/5 passed`.

**Text field:**

```
pass@5: 0/5 passed (avg@5 = 0.000). Breakdown: 0 solved, 5 good valid failures, 0 soft-timeout failures.
```

Then: **Save** → **Changes saved** → **Submit** (only after screenshot is attached).

---

## Step 6 — Numeric pass@ score

```
0
```

Enter the **solved count** (0 out of 5), not 0.000 and not 5.

Then **Submit**.

---

## Step 7 — Stop

Do **not** click **Confirm time** unless you are ready to finalize compensation.

---

## Quick reference

| Field | Value |
|---|---|
| Repository | handshake-project-dynamo/dynamo-1f78c32-machine-learning-and-ai |
| Task name | dynamo/recover-atlas |
| Category | Software Engineering |
| Sub-category | data recovery / event-log parsing / algorithmic reconstruction |
| pass@2 | 0/2 passed |
| pass@5 | 0/5 passed |
| avg@5 | 0.000 |
| Numeric score | 0 |
| Expert time | ~4 hours |
