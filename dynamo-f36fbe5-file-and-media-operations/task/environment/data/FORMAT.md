# Atlas Packet Format

This file is normative for `/app/rebuild_atlas.py`.

## Inputs

Each packet directory contains `manifest.json`, `events.tsv`, `pieces/`, and optional sidecar TSVs. `manifest.json` has `case_id`, `rows`, `columns`, `tile_size`, `cutoff`, and `background_rgba`. The starting atlas is straight RGBA, sized `columns*tile_size` by `rows*tile_size`, filled with `background_rgba`.

`events.tsv` columns are `event_id,slot_id,row,col,layer,asset_id,version,known_at,action,path,transform,opacity,source_hint`; ignore `source_hint`. Rows with `known_at > cutoff` are future rows. Visible `void` rows count as ignored events and do not update layer state. For each `(slot_id, layer)`, choose the non-void row with greatest `(known_at, version, event_id)`. A selected `delete` means absent. A selected `place` means render. If `assets.tsv` exists with `asset_id,path`, selected place rows load the resolved asset path and ignore event `path`; otherwise use event `path`.

Optional sidecars use `(slot_id, layer)` keys; later duplicate-key rows win. Supported sidecars: `patches.tsv` has `opacity`; `shifts.tsv` has `dx,dy` and defaults to `(0,0)`; `blends.tsv` has `mode` (`over` or `under`, default `over`); `masks.tsv` has `path`; `windows.tsv` has `x0,y0,x1,y1`; `tints.tsv` has signed `dr,dg,db`; `anchors.tsv` has `ax,ay`; `feedback.tsv` has `tx,ty,channel,gain_num,gain_den`.

Pieces are RGBA `.png` files or `.rle` files. RLE format is `PXRA1 <w> <h>` on the first line, followed by row-major `r,g,b,a count` runs; packet RLE pieces are tile-size squares.

## Rendering

For each selected place layer, apply operations in this order: patch opacity, alpha scale, mask, window, tint, transform, shift/anchor placement, optional feedback, then compositing. Alpha scale is `floor(alpha*opacity/255)`. Masking multiplies source alpha by the untransformed mask alpha with floor `/255`. A window keeps only half-open source coordinates `[x0,x1) x [y0,y1)`. Tint changes only pixels with alpha > 0 and adds `dr,dg,db` to straight RGB with saturating clamp to `0..255`, not modulo wrap. Transforms are `none` or `|`-separated `rot90`, `rot180`, `rot270`, `flipx`, `flipy`; rotations are counterclockwise, `flipx` maps x to `width-1-x`, and `flipy` maps y to `height-1-y`.

The placement offset starts with sidecar shift `(dx,dy)`. After transforms, remap that vector by applying each transform op's forward vector mapping in reverse operation order: `rot90` maps `(dx,dy)` to `(-dy,dx)`, `rot270` to `(dy,-dx)`, `rot180` to `(-dx,-dy)`, `flipx` to `(-dx,dy)`, and `flipy` to `(dx,-dy)`. If an anchor is present, transform source-space `(ax,ay)` through the same left-to-right transform pipeline to `(tx,ty)`, then add `(ax-tx, ay-ty)` to the placement offset. The final destination is `(col*tile_size + dx, row*tile_size + dy)` and pixels outside the atlas are clipped.

Paint selected place rows by `(layer, blend_rank, known_at, slot_id)`, where `blend_rank` is `0` for `under` and `1` for `over`. Feedback runs after destination is known and before the layer is composited: for every transformed source pixel with alpha > 0 whose destination is in bounds, sample the current atlas at `((dest_x+x+tx) mod atlas_width, (dest_y+y+ty) mod atlas_height)`, read component `channel` (`r`, `g`, `b`, or `a`), compute `delta=floor((component-128)*gain_num/gain_den)`, add it to all source RGB channels with the same `0..255` clamp, and leave alpha unchanged.

Composite in straight RGBA but use integer premultiplied Porter-Duff math for `over` and `under`: premultiply each RGB channel by alpha using floor `/255`; every blend divide by 255 also floors; un-premultiply back to straight RGB with round-half-up. A source pixel with `sa==0` leaves the destination unchanged; an `under` source below `da==255` is a no-op. Do not use floats, `Image.paste`, or `alpha_composite`. Save `restored_atlas.png` with Pillow defaults and no `optimize`.

## Restored Artifacts

`restored_occupancy.pgm` is a binary PGM alpha plane for the final atlas: bytes start with ASCII header `P5\n<width> <height>\n255\n`, followed by one row-major byte per atlas pixel equal to that pixel's final alpha value.

`restored_layer_audit.tsv` is tab-separated with LF (`\n`) line endings and header `paint_index,slot_id,layer,event_id,mode,asset_path,dest_x,dest_y,width,height,visible_pixels,feedback_pixels`. Emit one row per composited placed layer in paint order. `paint_index` is zero-based; `asset_path` is the resolved relative piece path; destination and dimensions are the final transformed placement rectangle; `visible_pixels` counts in-bounds transformed source pixels with alpha > 0 after mask/window/tint/transform/feedback; `feedback_pixels` is that layer's adjusted-pixel count or 0.

`restored_cell_index.tsv` is tab-separated with LF (`\n`) line endings and header `row,col,placed_layers,crop_sha256,alpha_sum,nonzero_alpha_pixels,opaque_alpha_pixels`. Emit rows in row-major cell order. For each tile-size crop from the final atlas, `placed_layers` is the number of composited placed layers whose original `(row,col)` is that cell, `crop_sha256` is SHA-256 of the crop's raw RGBA bytes, and the three alpha fields summarize the crop's final alpha bytes.

`restored_manifest.json` is pretty JSON with sorted keys, two-space indentation, and one trailing newline. Keys are `case_id`, `atlas_sha256`, `occupancy_pgm_sha256`, `cell_index_sha256`, `total_slots`, `visible_events`, `future_events_ignored`, `void_events_ignored`, `superseded_events`, `selected_events`, `placed_layers`, `deleted_layers`, `png_sources`, `rle_sources`, `transform_ops`, `opacity_scaled_layers`, `patch_overrides`, `shifted_layers`, `masked_layers`, `windowed_layers`, `tinted_layers`, `anchored_layers`, `clipped_layers`, `feedback_layers`, `feedback_pixels`, `under_blends`, `occupied_slots`, `stacked_cells`, `empty_slots`.

Hashes are SHA-256 of the written PNG, PGM, and cell-index TSV bytes. Counts: `total_slots=rows*columns`; `visible_events` is rows with `known_at<=cutoff`; `future_events_ignored` is rows with `known_at>cutoff`; `void_events_ignored` is visible voids; `superseded_events` is visible non-void rows not selected; `selected_events=placed_layers+deleted_layers`; source counts use the resolved extension; `transform_ops` counts atomic non-`none` ops; `opacity_scaled_layers` counts final opacity not 255; sidecar counters count placed events using that sidecar or under mode; `feedback_pixels` counts adjusted in-bounds nontransparent source pixels; `shifted_layers` counts final offset after shift and anchor not `(0,0)`; `clipped_layers` counts transformed rectangles crossing atlas bounds.

`occupied_slots` counts cells with at least one placed layer, `stacked_cells` counts cells with at least two, and `empty_slots=total_slots-occupied_slots`. All count values are integers.
