The transparent source art for the Aurora badge icon atlas was lost. Rebuild the atlas state that was approved for the ship cutoff in `/app/data/export_index.json`.

The files in `/app/data/proofs/` are flattened contact-sheet exports over known matte colors. `/app/data/export_index.json` gives each proof path, matte RGB value, sheet transform, grid geometry after undoing the transform, tile order, and ship cutoff. `/app/data/revision_log.csv` gives tile revision events in audit-export order, not chronological order.

Use the newest complete paired proof snapshot whose `snapshot_time` is not later than the ship cutoff. A complete pair is a snapshot that has exactly two proof exports; snapshots with fewer or more than two exports are not complete pairs and must be skipped. Newer prototype proofs are not part of the requested shipping art.

Recover the straight-alpha RGBA pixels for every tile from the paired matte exports, undo each proof's own declared `sheet_transform` before slicing, discard gutters and calibration strokes, and assemble the tiles in the manifest's row-major order with no padding. The two exports in a pair may use different transforms. The `sheet_transform` value can be `identity`, `flip_x`, `flip_y`, or `rotate_180`; `flip_x` mirrors left-right across the vertical axis, `flip_y` mirrors top-bottom across the horizontal axis, and `rotate_180` applies both flips. Apply the inverse transform so `grid_after_untransform` addresses the corrected sheet. Paired `matte_rgb` values differ in every channel.

For each pixel channel, the flattened byte obeys `p = (alpha * foreground + (255 - alpha) * matte) / 255`, rounded into the proof image. Given the two matte observations for the same source pixel, estimate alpha separately for red, green, and blue with `alpha_estimate = 255 - 255 * ((p_first - p_second) / (matte_first - matte_second))`, using unclamped real values. Sort the three alpha estimates, take the middle value, then round and clamp it once to a 0-255 integer byte. Use that integer alpha byte to recover each foreground channel from each matte observation with `foreground_estimate = (255 * p - (255 - alpha) * matte) / alpha`; average the two foreground estimates for that channel, then round and clamp to a byte. If alpha rounds to 0 or 1, write `(0, 0, 0, 0)` for that pixel.

Create these files:

`/app/recovered/aurora_atlas.png`: RGBA PNG, exactly the `width` and `height` in `output_canvas`, containing only the recovered transparent tiles.

`/app/recovered/recovery_summary.json`: JSON object with exactly these top-level keys:
- `canvas`: object copied from `output_canvas`.
- `cutoff`: the ship cutoff string.
- `tile_order`: array copied from the manifest tile order.
- `revision_by_tile`: object mapping every tile name to the `approved` revision with the greatest `effective_at` timestamp that is not later than the cutoff; if identical timestamps exist for the same tile, the later row in the file wins. Object keys must appear in the same order as `tile_order`.
- `alpha_coverage`: object mapping every tile name to the count of pixels in that tile whose recovered alpha is at least 128. Object keys must appear in the same order as `tile_order`.

`/app/recovered/recover_atlas.py`: a reusable Python 3 CLI implementing the same recovery contract. When run with no arguments it must read `/app/data` and write `/app/recovered`; it must also accept `--data-dir DIR` and `--out-dir DIR` so the same code can recover another directory with the same `export_index.json`, `revision_log.csv`, and `proofs/` layout.

All JSON keys and tile-order arrays must use the same names and ordering as the manifest. Do not include prototype or rejected revisions in the shipping atlas.
