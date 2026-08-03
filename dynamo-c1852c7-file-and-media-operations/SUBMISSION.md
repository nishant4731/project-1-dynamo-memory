# Handshake Dynamo Form — dynamo/recover-reel

PR status: **accepted**  
Date: 2026-07-29

---

## PR URL

```
https://github.com/handshake-project-dynamo/dynamo-c1852c7-file-and-media-operations/pull/2
```

## Accepted commit SHA

```
f8d285642b404349df38c26b14d7073d2a8e8e67
```

---

## Step 1 — Proposal

Keep the category/sub-category text the form already shows. Paste everything below into the rich text editor.

```
Category: File and Media Operations
Sub-category: Video Processing
Task: dynamo/recover-reel — Recover Reel

PR: https://github.com/handshake-project-dynamo/dynamo-c1852c7-file-and-media-operations/pull/2
Accepted commit: f8d285642b404349df38c26b14d7073d2a8e8e67

Who does this work and why it matters

A senior video/forensics engineer or streaming recovery engineer would do this when a surveillance or broadcast capture arrives as fragmented, lossy tile packets rather than a playable reel. The job is not just to render a video — it is to reconstruct the reel from packet evidence, prove which packets were used, report exact audit counters for compliance, and ship a reusable recovery tool for the same packet format. This mirrors real post-incident media recovery where checksums, revision conflicts, parity repair, coordinate remapping, and evidence handling all matter.

Synthetic data and realism

The workspace uses synthetic but realistic packetized monochrome surveillance data: a 16x12, 14-frame Y4M reel split into 4x4 tiles with multiple codecs (raw, rle, delta_prev, zigzag), FEC-style parity records, stale revisions, recalled rows, checksum failures, per-frame telemetry remapping, and a permanent packet-id veto ledger. No external services or live network data are required.

What the agent must produce

Four exact outputs:

1. /app/recovered/reel.y4m — byte-exact YUV4MPEG2 monochrome video (16x12, 14 frames, 5 fps)
2. /app/recovered/audit.json — forensic audit counters (decode rejects, selection counts, parity stats, telemetry modes, veto counts, consumed packet rows)
3. /app/recovered/lineage.json — packet provenance on display tiles (direct selections, parity repairs, frame deltas, packet-path hash)
4. /app/recovered/recover.py — reusable CLI: python3 recover.py INPUT_DATA_DIR OUTPUT_DIR

Why this is genuinely difficult

Wrong solutions look plausible but fail on peripheral exactness:

- Telemetry remapping: packet tile coords are sensor coords; display coords depend on per-frame forward vs mirror_x mode (greatest effective_from_frame <= f, file-order tie-break). Treating packet coords as display coords produces a valid-looking reel with wrong lineage.
- Permanent veto ledger: a veto is permanent even if a later confirm names the same packet_id. Agents that clear vetoes on confirm select wrong tiles.
- FEC parity repair: parity members must be remapped through telemetry; parity runs in packet-id order with chained repairs; only exactly-one-missing-member cases apply.
- Evidence consumption: after writing outputs, packet_log.jsonl must be deleted from the input directory. Skipping this leaves wrong consumed_packet_rows and breaks the reusable-tool contract.
- Exact accounting: audit and lineage JSON must match protected expected values field-for-field, including stage-sampled counters at decode/veto/selection/parity branches.

Intended solution approach

1. Load telemetry modes and build the permanent veto set from revision_ledger.jsonl.
2. Decode active tile records; map sensor to display coordinates per frame.
3. Drop checksum failures and vetoed packet_ids; select winners by (frame, display_tile) using highest revision, then lexicographically smallest packet_id.
4. Process parity records in packet-id order with remapped members; XOR-reconstruct missing tiles when exactly one member is absent.
5. Apply direct then parity replacements over inherited previous-frame state.
6. Emit Y4M, audit.json, lineage.json; install the same logic in recover.py; delete the consumed packet log.

Key insight: reconstruction, provenance, and evidence handling are three interacting subsystems — getting the video roughly right is not enough if telemetry, vetoes, or consumption are wrong.

Expert time estimate: ~5 hours for a senior video/forensics engineer who understands sensor-to-display remapping and packet-level provenance reporting.

Verification plan

The verifier rejects missing or symlinked outputs, compares exact Y4M bytes and exact audit/lineage JSON equality (including telemetry_mode_by_frame, vetoed_valid_tiles, consumed_packet_rows), asserts the shipped packet_log.jsonl was consumed (deleted), then runs the submitted recover.py on generated fixtures with mixed telemetry and vetoes, compares all outputs to an independent reference, and confirms the tool deletes each fixture packet log.

Category justification

This is core Video Processing under File and Media Operations: the agent decodes tile codecs, reconstructs a Y4M video reel, performs parity-based media repair, and produces media artifacts plus structured forensic reports — not generic file search or unrelated scripting.

Accepted result

The PR is marked accepted. The final pipeline passed static checks, duplicate/similarity review, validation, pass@2, deep review, adversarial review, AVA review, pass@5 trials, and the final gate.

pass@2: 1/2 passed
pass@5: 1/5 passed (avg@5 = 0.200)
Breakdown: 1 solved, 4 good valid failures, 0 soft-timeout failures

This satisfies the difficulty gate (0-2/5 solved with >=3 valid failures).
```

Then: **Save** → wait for "Changes saved" → **Submit**.

---

## Step 2 — Repository / workflow

PR is already complete and accepted. **Submit** this step.

---

## Step 3 — Artifact type (multi-select)

```
Media artifact
Generated output artifact
Single script or program
```

Then **Submit**.

---

## Step 4 — Task objective (multi-select)

```
Recover or repair artifact
Transform
Analyze
```

Then **Submit**.

---

## Step 5 — Screenshot + pass@ text

**Screenshot:** attach the latest pass@5 PR comment showing `pass@5: 1/5 passed`.

**Text field:**

```
pass@5: 1/5 passed (avg@5 = 0.200). Breakdown: 1 solved, 4 good valid failures, 0 soft-timeout failures.
```

Then: **Save** → **Changes saved** → **Submit** (only after screenshot is attached).

---

## Step 6 — Numeric pass@ score

```
1
```

Enter the **solved count** (1 out of 5), not 0.200 and not 4.

Then **Submit**.

---

## Step 7 — Stop

Do **not** click **Confirm time** unless you are ready to finalize compensation.

---

## Quick reference

| Field | Value |
|---|---|
| Repository | handshake-project-dynamo/dynamo-c1852c7-file-and-media-operations |
| Task name | dynamo/recover-reel |
| Category | File and Media Operations |
| Sub-category | Video Processing |
| pass@2 | 1/2 passed |
| pass@5 | 1/5 passed |
| avg@5 | 0.200 |
| Numeric score | 1 |
| Expert time | ~5 hours |
