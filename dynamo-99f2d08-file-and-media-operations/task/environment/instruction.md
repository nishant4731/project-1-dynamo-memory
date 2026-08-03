Reconstruct the badge artwork described by `/app/design/canvas.txt`, `/app/design/palette_history.csv`, `/app/design/sprites.stencil`, and `/app/design/placement_audit.csv`.

Create exactly these three outputs:

`/app/restored_badge.ppm`: an ASCII PPM image in `P3` format with the canvas width, height, max value `255`, and the final RGB pixels.

`/app/restoration_report.json`: UTF-8 JSON object with these keys:
- `cutoff`: the cutoff timestamp from `/app/design/canvas.txt`.
- `canvas`: object with integer `width` and `height`.
- `active_layers`: array of effective non-repair audit layer ids in render order.
- `omitted_layers`: array of layer ids whose latest row at or before the cutoff is `delete`, sorted by the row number of that delete row.
- `selected_repairs`: array of selected repair candidate ids in increasing `group` order, or `[]` if no repair candidates file exists.
- `pixel_sha256`: lowercase SHA-256 hex digest of the raw RGB bytes from `/app/restored_badge.ppm` in row-major order.
- `sample_pixels`: object mapping each requested `x,y` sample from `/app/design/canvas.txt` to its final lowercase `#rrggbb` value.

`/app/replay_design.py`: a reusable Python script. Running `python3 /app/replay_design.py <design_dir> <ppm_out> <report_out>` must render any design directory with the same file names and rules into the two requested output files. Use it to produce `/app/restored_badge.ppm` and `/app/restoration_report.json`.

Rendering rules:

The canvas starts as the background color in `/app/design/canvas.txt`. Only audit rows with `time` less than or equal to the cutoff are eligible; later rows are drafts and must be ignored. For each `layer_id`, keep only its latest eligible row by timestamp, breaking equal-timestamp ties by larger `row`. A latest `delete` row omits that layer. A latest `place` row is rendered.

`/app/design/sprites.stencil` contains sprites. Each sprite begins with `sprite <id> <width> <height>`, followed by exactly `<height>` run-length encoded rows, then `end`. In a row, a decimal count followed by a symbol repeats that symbol; a symbol without a count repeats once. `.` is transparent. All other symbols are ink codes.

For every rendered placement, resolve each ink code using `/app/design/palette_history.csv` at the placement row's own timestamp, not at the cutoff and not at the newest palette row. Use the latest palette row for that ink whose `time` is less than or equal to the placement time, breaking same-time ties by larger `row`.

Placement coordinates are integers. `anchor=topleft` means `x,y` is the sprite's top-left pixel. `anchor=center` means the top-left pixel is `x - width // 2, y - height // 2`. Pixels outside the canvas are clipped. Render effective placements sorted by increasing `z`; ties use increasing audit `row`.

If `placement_audit.csv` includes `transform`, apply it to the sprite before anchoring. Valid values are `none`, `flip_h`, `flip_v`, `rot90`, `rot180`, and `rot270`. `rot90` is clockwise; `rot270` is counterclockwise. Anchoring uses the transformed width and height.

If `placement_audit.csv` includes `blend_mode`, compute the blend source for each channel before applying opacity: `normal` uses `src`; `multiply` uses `floor(src * dst / 255)`; `screen` uses `255 - floor((255 - src) * (255 - dst) / 255)`. Then composite that blend source over the current canvas with `opacity_pct / 100`. For each RGB channel, after every pixel placement compute `floor(blend_source * alpha + dst * (1 - alpha) + 0.5)`. Do not premultiply across layers or defer rounding.

If `placement_audit.csv` includes `clip_rect`, a non-empty value is `x:y:w:h` in canvas coordinates; draw only pixels whose final canvas coordinate satisfies `x <= px < x + w` and `y <= py < y + h`. If it includes `ink_opacity`, a non-empty value is `INK=pct|INK=pct`; multiply the placement opacity by that ink's percentage before compositing pixels with that ink. Inks not listed use 100%.

If `/app/design/repair_candidates.csv` exists, select exactly one candidate from every integer `group` before rendering. Its required columns are `row,candidate_id,group,cost,residue,time,sprite,x,y,anchor,z,opacity_pct,transform,blend_mode,clip_rect,ink_opacity`. It may also include optional columns `requires` and `conflicts`; each optional value is empty or a `|`-separated list of `candidate_id` strings. A selection is feasible only if every selected candidate's `requires` ids are also selected and none of its `conflicts` ids are selected. Infeasible selections must be ignored even if their residue, cost, or id tie-break rank would otherwise be better. If `/app/design/repair_pair_penalties.csv` exists, its rows have `candidate_a,candidate_b,cost_delta,residue_delta`; each row applies exactly once when both candidate ids are selected, regardless of their order, adding `cost_delta` to total cost and `residue_delta` to the residue sum before taking the modulus. `selected_repairs` contains the selected `candidate_id` strings. `canvas.txt` then contains `repair_modulus` and `repair_target`. For a feasible selection, compute `score = (sum(candidate residue) + sum(selected pair residue_delta)) mod repair_modulus`; circular distance is `min((score - target) mod modulus, (target - score) mod modulus)`. Choose the feasible selection with smallest circular distance, then smallest total `cost` including pair `cost_delta`, then lexicographically smallest selected candidate ids compared in increasing `group` order. Render selected candidates as extra `place` rows using the candidate CSV columns, after applying the same transform, clip, ink opacity, blend, z, and row ordering rules.
