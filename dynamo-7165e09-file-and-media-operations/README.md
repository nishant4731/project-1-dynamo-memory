# recover-rvc-video

Recover a short grayscale video clip from a damaged custom container (`RVC4`), then
build a residue-constrained delivery reel from it. Outputs are byte-exact YUV4MPEG2
(Y4M) streams plus a delivery plan JSON.

## Overview

The agent is given `/app/data/clip.rvc`, a little-endian binary container that stores
frames in **decode order** with three frame types — intra (`I`), forward-predicted
(`P`), bi-predicted (`B`) — trailing per-group XOR parity records, and a **delivery
section**. The agent must write a reusable program `/app/out/recover.py` (driven by
`RVC_INPUT`/`RVC_OUTDIR`) and produce `/app/out/clip.y4m`, `/app/out/delivery.y4m`,
and `/app/out/plan.json`.

## Approach

0. **Apply the correction ledger** per target frame — events in ascending `seq` (ties by
   file order); `SET` replaces the working payload, `CLEAR` resets it to the frame's base
   payload (not "undo last SET") — yielding each frame's authoritative payload.
1. **Recover** erased payloads (`flags` bit 0) from the group's GF(2⁸) parity block
   (reduction poly `0x11B`) by solving the linear system `XOR_j gfmul(C[r][j], p_j) ==
   parity_r` for the erased payloads — *before* decoding (up to R erasures/group).
2. **Decode** in decode order: `I` = raw luma (new anchor); `P` = `(anchor + residual) mod 256`
   (new anchor); `B` = `(pred + residual) mod 256` where `pred` is the **distance-weighted**
   average `(d1·A0 + d0·A1 + (d0+d1)//2)//(d0+d1)` of the two most recent anchors (`d0`/`d1`
   are display-index distances), and is never itself an anchor.
3. **Reorder** the frames into ascending `display_index` and emit `clip.y4m` (Cmono Y4M).
4. **Delivery reel**: choose one candidate per slot to maximize total score subject to
   `(sum of chosen weights) mod M == D`, breaking ties by lexicographically-smallest
   candidate-index sequence. Write `plan.json` and render the chosen frames to
   `delivery.y4m`.

## Why it is hard

The visible clip is only `I`/`P` with small non-wrapping deltas, no erasures, an **empty
ledger**, and a delivery **modulus of 1** — so decode order equals presentation order,
clamping equals modulo, bi-prediction weighting is irrelevant, parity and ledger are unused,
and a greedy max-score pick is already valid. Every common shortcut yields the correct
visible output and gives no signal. The reusable solver is re-run on a **hidden** container
combining several independent latent cruxes: `B`-frame reordering at **unequal anchor
distances** (simple averaging is wrong), modulo-256 residual wraparound, a **two-erasure
GF(256) parity group** whose erased frames include an anchor (single-XOR cannot recover it
and the leading parity-row subset is singular), a **correction ledger** whose events are
shuffled relative to `seq` and whose `CLEAR` resets to base (not undo-last), and a
**prime-modulus** delivery whose greedy selection is invalid over a **~6.2×10⁹**-combination
space (forcing a residue DP with a canonical tie-break). All rules are fully disclosed; the
difficulty is getting every coupled rule right with no visible case that exercises any of
them.

## Environment

Single Ubuntu 24.04 image (digest-pinned) with `python3` and `pytest` baked in. The visible
container is copied to `/app/data`; no ground truth is present in the agent image.

## Verification

`task/tests/test_outputs.py` computes ground truth with an independent implementation
(decode + residue DP) over protected container copies overlaid at `/tests` (never the
agent-writable `/app/data`). It checks the three artifacts are real, non-empty, non-symlink
files; byte-matches the two Y4M streams and value-matches `plan.json`; and re-runs the
agent's `recover.py` on both the protected visible container and the hidden container,
matching all artifacts for both. Exact comparison is fair because the integer decode,
parity, rounding, ordering, Y4M framing, and delivery objective (with a canonical tie-break)
are fully specified with no tolerances or alternate valid outputs.
