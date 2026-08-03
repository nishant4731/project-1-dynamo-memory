Write a reusable Python 3 script at `/app/recover_video.py`.

The script is invoked as `python3 /app/recover_video.py <clip_dir>`. A clip directory contains `ledger.tsv` and payload files below `payloads/`. The script must create or replace `<clip_dir>/recovered/`, then write recovered grayscale frame files and `<clip_dir>/recovered/manifest.json`.

`ledger.tsv` is tab separated with this header: `shot frame part row_start row_end width height revision valid_from_ms expires_ms mode payload sha256`. Paths in `payload` are relative to the clip directory. Frame display time is `frame * 40` milliseconds. A ledger row is eligible only when its payload file exists, the SHA-256 of the payload bytes equals `sha256`, `valid_from_ms <= display_time`, and `expires_ms` is `-` or `display_time < expires_ms`.

Rows describe horizontal bands of one frame: `row_start` is inclusive and `row_end` is exclusive. For each `(shot, frame, part)` choose the eligible row with the highest `revision`; if those tie, choose the lexicographically smallest `payload` path. The chosen bands for a frame must cover rows `0..height-1` exactly once, with one shared `width` and `height`. If a frame's chosen bands do not have exact coverage, disagree on dimensions, or cannot decode to their required lengths, skip that frame: write no PGM for it, do not count its bands in `selected_parts`, and do not make it the previous recovered frame.

Decode each chosen payload into exactly `width * (row_end - row_start)` grayscale bytes:
`raw` is stored directly. `rle` is byte pairs of `(count, value)` and expands by repeating each value `count` times. `delta_xor` stores each byte XORed with the byte at the same pixel position in the previous recovered frame of the same shot; if there is no previous frame, use zero bytes. Previous frame means the immediately preceding numeric frame that was recovered for that shot.

Write each recovered frame as binary PGM `P5` to `<clip_dir>/recovered/shot_<shot>_frame_<NNN>.pgm`, where `<NNN>` is the zero-padded three-digit frame number. The PGM bytes are `P5\n<width> <height>\n255\n` followed by the row-major grayscale payload.

Write `manifest.json` as UTF-8 JSON with exactly two top-level keys: `frames` and `report`. `frames` is sorted by `shot` then numeric `frame`; each entry has `shot`, `frame`, `width`, `height`, `sha256`, and `mean_luma`, where `sha256` is the digest of the raw frame bytes and `mean_luma` is integer floor of average luma. In `report`, `ledger_rows` is the number of non-header rows parsed, `hash_rejected` counts rows rejected for a missing payload or SHA mismatch, `time_rejected` counts hash-valid rows rejected by the validity window, `selected_parts` counts chosen bands used in written frames, and `frames_written` counts PGM frames written.
