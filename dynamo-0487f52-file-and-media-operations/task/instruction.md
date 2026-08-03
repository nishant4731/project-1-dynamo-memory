Create `/app/recover_spool.py`, a reusable command-line recovery tool:

`python3 /app/recover_spool.py INPUT_DIR OUTPUT_DIR`

The shipped crash image is `/app/data/session`; the visible fixture includes `FORMAT_NOTES.txt`, which is part of the task contract. Use those notes as the detailed schema and arithmetic reference for every input directory the verifier gives your tool, even when a protected directory only contains the data tables themselves.

Your tool must reconstruct the grayscale luma journal and write exactly these outputs for the visible run under `/app/recovered`:

- `/app/recovered/movie.y4m`
- `/app/recovered/report.json`
- `/app/recovered/ledger.tsv`
- `/app/recovered/contact.pgm`
- `/app/recovered/scan.tsv`

The input manifest supplies frame geometry, frame count, FPS, neutral byte, salt, and the valid source names. Recovery has six decision stages:

1. Authenticate anchors and infer each source's integer tick-to-frame offset by majority vote, breaking ties toward the smaller offset.
2. Authenticate byte repairs, packet drop gates, packet leases, frame operations, and post-render stencils with the salt formulas in `/app/data/session/FORMAT_NOTES.txt`; for duplicate sidecar rows with the same documented identity key, keep max `(known_at, rev, id)` and count the other valid rows as superseded.
3. Read `packets.jsonl` in full. Reject non-committed rows, unknown or offset-less sources, invalid target frames or rectangles, gate-overlapping packets, and otherwise geometry-valid packets that are not covered by any selected lease for the same source/tick/sequence.
4. Decode the remaining packet payloads, apply selected byte repairs before packet hash validation, reject codec/hash failures, keep the latest valid duplicate packet per identity, and paint selected packets into neutral staging frames in canonical order.
5. Render final frames in frame order using selected frame operations, then current-bus taps, then threshold stencils. Taps read the already-rendered output bus at their execution point; stencils run after all base placements and taps.
6. Emit the movie, JSON report, ordered ledger, PGM contact sheet, and TSV scan, then delete consumed evidence files from the input directory.

The consumed evidence files are `anchors.tsv`, `packets.jsonl`, `repairs.tsv`, `gates.tsv`, `leases.tsv`, `ops.tsv`, `taps.tsv`, and `stencils.tsv`. Leave `manifest.json` and fixture notes alone.

Artifact formats are exact. `movie.y4m` is mono YUV4MPEG2 with a `YUV4MPEG2 W{width} H{height} F{fps_num}:{fps_den} Ip A1:1 Cmono\n` header followed by `FRAME\n` and row-major luma bytes for each frame. `ledger.tsv` is LF text with header `kind<TAB>id<TAB>frame`, then rows for painted packets, selected frame ops, successful taps, and pixel-changing stencils in emission order; tap ledger rows use the tap's `write_frame` value as the `frame` column, not `after_frame`. `contact.pgm` is binary P5: final frames tiled row-major into `ceil(sqrt(frames))` columns, with one neutral separator row or column between neighboring tiles. `scan.tsv` is LF text with header `frame<TAB>sha256<TAB>non_neutral<TAB>min<TAB>max<TAB>mean_floor<TAB>bbox`; each row summarizes one final frame. Compute `min`, `max`, and `mean_floor` over every pixel in the frame, including neutral pixels. Only `bbox` uses the literal `empty` for a frame with no non-neutral pixels; otherwise it is comma-separated `min_x,min_y,max_x,max_y`, the pixel-coordinate extremes of all non-neutral pixels.

`report.json` must be canonical JSON written with sorted keys, compact separators, and a final newline. It must contain strict integer counters for every accepted and rejected stage named in `FORMAT_NOTES.txt`, object `source_offsets`, object `frame_sha256` keyed by stringified decimal frame indexes, plus lowercase hex `ledger_sha256`, `contact_sha256`, and `scan_sha256` over the exact secondary artifact bytes. Boolean or float substitutes for integer counters are not acceptable.
