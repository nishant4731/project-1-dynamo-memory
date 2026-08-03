Implement executable `/app/repair_atlas.py`, invoked as:

`/app/repair_atlas.py <session_dir>`

Run it once on `/app/session`. Success leaves `/app/session/atlas.ppm`, `/app/session/trace.tsv`, and `/app/session/report.json`.

`manifest.json` has `width`, `height`, `background`, `record_salt`, `patch_salt`, `anchor_salt`, `tap_salt`. Ledgers live in `<session_dir>/fragments/`: required `records.tsv`; optional `patches.tsv`, `anchors.tsv`, `taps.tsv`. The visible packet includes `/app/session/fragments/FORMAT_NOTES.txt` as a reminder of tie cases.

Initialize counters to zero, `assets_rendered=[]`, and set `evidence_removed` true only in the final report after cleanup. Count every physical record row in `records_total`.

**Records**

`records.tsv` header:

`record_id asset_id rev known_at z x y transform blend alpha w h retired payload_sha payload_hex mask_sha mask_hex`

Reject to `records_rejected_checksum` on any bad integer, bad hex, `len(payload)!=w*h*3`, `len(mask)!=w*h`, SHA-256 mismatch for payload or mask, `w<=0`, `h<=0`, `alpha` outside `0..255`, `retired` not `0`/`1`, transform outside `{identity, flip_x, flip_y, rot90}`, or blend outside `{over, add, replace}`. Valid `retired=1` rows only increment `records_retired`.

For each asset, select the non-retired row with greatest `(known_at, rev, record_id)`. Other valid non-retired rows for that asset increment `records_shadowed`. `records_selected` is selected asset count.

**Patches**

`patches.tsv` header: `patch_id asset_id known_at dx dy channel delta check`

Sort by `(int(known_at), patch_id)`. Token:

`sha256(patch_salt|patch_id|asset_id|known_at|dx|dy|channel|delta)[:16]`

Fields use parsed integers joined with literal `|`. Apply only if token matches, asset is selected, `(dx,dy)` is inside the original untransformed source grid, and `channel` is `0`, `1`, or `2`. Add `delta` to that source channel and clamp to `0..255`. Accepted/rejected rows increment `patches_applied`/`patches_rejected`.

**Anchors**

`anchors.tsv` header: `anchor_id source_asset target_asset priority dx dy check`

Sort by `(int(priority), anchor_id)`; rows whose priority cannot parse sort last and are then rejected. Token:

`sha256(anchor_salt|anchor_id|source_asset|target_asset|priority|dx|dy)[:16]`

Rows with parse/token failure or unselected source/target increment `anchors_rejected`. A valid row means `target final origin = source final origin + (dx,dy)`. Non-conflicting accepted rows increment `anchors_applied`; valid rows contradicting an already implied relation increment `anchors_conflicts` and are ignored. Accepted anchors form constrained groups: the lexicographically smallest asset in each group keeps its original selected `(x,y)`, and all others move to the unique origin implied by offsets. Unanchored singletons keep selected `(x,y)`.

**Draw And Taps**

Draw selected assets sorted by `(z, known_at, asset_id)`. Transform RGB and mask before drawing: `identity` unchanged; `flip_x` reverses rows; `flip_y` reverses row order; `rot90` rotates clockwise.

`taps.tsv` header: `tap_id asset_id after_asset dx dy canvas_x canvas_y channel gain_num gain_den check`

Parse/group rows by `asset_id` in `tap_id` order. Token:

`sha256(tap_salt|tap_id|asset_id|after_asset|dx|dy|canvas_x|canvas_y|channel|gain_num|gain_den)[:16]`

Parse/token failures increment `taps_rejected`. For parsed rows, first check whether `after_asset` has already drawn; if not, increment `taps_ignored_future` and skip all other checks. Otherwise require transformed-source `(dx,dy)`, in-canvas `(canvas_x,canvas_y)`, channel `0..2`, and `gain_den > 0`; failures increment `taps_rejected`. Accepted taps run before compositing that asset:

`source[dy][dx][channel] = clamp(source[dy][dx][channel] + canvas[canvas_y][canvas_x][channel] * gain_num // gain_den)`

Increment `taps_applied`.

**Composite And Outputs**

Start canvas from `background`. For each transformed pixel landing in-canvas, compute `a = alpha * mask // 255`; skip `a<=0`. Otherwise increment `pixels_composited`, then blend per channel: `over=(src*a+dst*(255-a))//255`; `add=min(255,dst+src*a//255)`; `replace=src`.

Before blending, if an earlier composited pixel touched that canvas cell, increment `overlap_pixels` and append to `trace.tsv` one tab-separated row in compositing order:

`asset_id local_x local_y canvas_x canvas_y pre_rgb post_rgb`

`pre_rgb` and `post_rgb` are six lowercase hex digits. `trace.tsv` is LF-only TSV with that exact header, even when there are no rows. After each asset draws, append its `asset_id` to `assets_rendered`.

`atlas.ppm` is binary P6: `P6\n<width> <height>\n255\n` plus row-major RGB bytes. `report.json` has exactly these keys: `canvas_sha256`, `trace_sha256`, `assets_rendered`, `records_total`, `records_selected`, `records_rejected_checksum`, `records_retired`, `records_shadowed`, `patches_applied`, `patches_rejected`, `anchors_applied`, `anchors_rejected`, `anchors_conflicts`, `taps_applied`, `taps_ignored_future`, `taps_rejected`, `pixels_composited`, `overlap_pixels`, `evidence_removed`. Count fields are JSON integers; `canvas_sha256` hashes full PPM bytes and `trace_sha256` hashes full trace TSV bytes.

Write PPM and trace, delete `<session_dir>/fragments/` entirely, then write the final report.
