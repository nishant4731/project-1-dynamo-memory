Rebuild `/app/design_packet` (`atlas.png`, `layers.json`). JSON has canvas/background, `symbols`, `layers`, report samples. Start with `canvas.background` or transparent `[0,0,0,0]`; layers may exceed bounds.

Produce:

- `/app/recovered/final.png`: RGBA PNG.
- `/app/recovered/report.json`: exactly `canvas_size`, `nontransparent_bbox`, `visible_pixels`, `alpha_sum`, `channel_sums`, `weighted_checksum`, `sample_rgba`.
- `/app/recovered/renderer.py`: exposes `render_packet(packet_dir, output_dir)`, creates missing `output_dir`, renders same-schema packets, stdlib only, reads/writes only there.

Rules:

- Process layers in order; skip hidden/disabled.
- Normal layers have `rect`; groups have `layers`, `size`.
- Polygon layers have `polygon`, `size`, `fill`, no `rect`. Build transparent `size`; per pixel test `(0.25,0.25)`, `(0.75,0.25)`, `(0.25,0.75)`, `(0.75,0.75)` with even-odd fill; boundary inside. RGB is `fill`; alpha `(fill_alpha * covered_subpoints) // 4`.
- Groups render children to transparent `size`, then composite at group `position`; group `opacity`/`blend` apply there.
- `symbols` is a JSON object keyed by name. Symbol-use layers have `use` naming one top-level `symbols` key; render its `layers` to its `size`, then composite like a group. `child_offsets` maps descendant `id` to `[dx, dy]`; add to that descendant's `position` for this use only. Offsets do not resize or mutate later uses.
- Crop `rect` `[x, y, width, height]` from the atlas.
- If normal layer `nine_slice` `[left, top, right, bottom]` and `target_size` `[width, height]` exist, resize crop to `target_size` before flips, rotation, masks, repeat. Copy corners; stretch edges/center by `source_start + ((dest_index - dest_start) * source_span) // dest_span`.
- Apply `flip_x`, then `flip_y`, then `rotate_cw`. `rotate_cw` is one of `0`, `90`, `180`, or `270`.
- `position` is destination top-left of transformed crop.
- If `mask_rect` exists, crop it, apply same nine-slice resize/flips/rotation, then source alpha is `(source_alpha * mask_alpha) // 255`.
- If `mask_mode` is `"luminance"`, use `(77 * r + 150 * g + 29 * b) // 256` from mask pixels. Missing means `"alpha"`.
- Apply layer opacity after the mask using `(alpha * opacity) // 255`.
- If `repeat` is `[columns, rows]`, repeat transformed crop in x/y before compositing. Mask repeats too.
- If `displace_rect` and `displace_scale` are present, crop/resize/transform/repeat that map like the source before masks. Pixel `(x,y)` samples from `x + ((r - 128) * displace_scale) // 128`, `y + ((g - 128) * displace_scale) // 128`, clamped.
- If `tint` is present as `[r, g, b, a]`, multiply source RGBA channels using `(value * tint_channel) // 255` after masks, repeats, or offscreen rendering, before opacity.
- If `channel_matrix` has four `[r,g,b,a,bias]` rows, after tint and before opacity replace RGBA with `clamp((r0*r + g0*g + b0*b + a0*a + bias) // 256,0,255)` per row. Shadows ignore it.
- If a non-group, non-symbol, non-`warp_quad` layer has `shadow`, render it first. `shadow` has `offset`, `blur_radius`, `color`. From post-mask/repeat alpha, shadow alpha is `((sum alpha in the clipped square radius) // pixel_count * color_alpha) // 255`; RGB is `color` RGB. Composite at `position + offset` with normal blend and layer opacity.
- If `warp_quad` is present, ignore `position` and project the transformed/repeated source with an 8-DOF homography into canvas-space `[top_left, top_right, bottom_right, bottom_left]`. For each destination pixel center inside it, inverse-project to unit source `(u, v)`; no bilinear quad interpolation. Sample `int(u * width), int(v * height)` clamped, then apply mask, tint, channel matrix, opacity, blend, source-over.
- Clip pixels outside the canvas.

Blend/composite use straight RGBA 0-255. For source `S`, destination `D`, alpha `Sa`/`Da`, first compute blended color `B` for every source pixel, even when `Da` is zero:

- `normal`: `B = S`
- `multiply`: `B = (S * D) // 255`
- `screen`: `B = 255 - ((255 - S) * (255 - D) // 255)`
- `difference`: `B = abs(D - S)`
- `overlay`: if `D < 128`, `B = (2 * S * D) // 255`; otherwise `B = 255 - (2 * (255 - S) * (255 - D) // 255)`

Then source-over:

- `out_a = Sa + (Da * (255 - Sa)) // 255`
- If `out_a` is zero, RGB `[0, 0, 0]`.
- Otherwise `out_c = (B_c * Sa * 255 + D_c * Da * (255 - Sa)) // (out_a * 255)` for each RGB channel, clamped after division.

Report:

- `canvas_size`: `[width, height]`.
- `nontransparent_bbox`: `[min_x, min_y, max_x_exclusive, max_y_exclusive]` over alpha > 0, or `null`.
- `visible_pixels`: alpha > 0 count.
- `alpha_sum`: alpha sum.
- `channel_sums`: JSON object exactly `{"r": r_sum, "g": g_sum, "b": b_sum, "a": a_sum}` over the full canvas, not a list.
- `weighted_checksum`: `sum((x + 1) * 3 * r + (y + 1) * 5 * g + (x + y + 2) * 7 * b + (x + 1) * (y + 1) * a)` over every final pixel, modulo `1000000007`.
- `sample_rgba`: sample point from `layers.json`, key `"x,y"`, value final `[r, g, b, a]`.
