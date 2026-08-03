# Charged Marble Lattice

The scene is a rectangular grid. Coordinates are zero-based with `x` increasing rightward and `y` increasing downward. Direction order is `N`, `E`, `S`, `W`. A marble packet has a cell, direction, and signed charge.

## Optimization

Choose exactly `optimizer.place_exactly` cells from `optimizer.candidate_cells`. Replace each chosen cell with one tile from `optimizer.choices`; unchosen candidates keep the grid tile. Output placements sorted by `id`. Maximize:

`10000019*visited_cells + trail_checksum + 101*collision_count + stability_bonus*steady_span - 997*leak_count - 193*blocked_count`

If `optimizer.stability_bonus` is absent, use `0`. `steady_span` is the longest consecutive run of ticks whose tick load is nonzero and at most `optimizer.steady_load_cap`; if the cap is absent, `steady_span` is `0`. Break equal scores by the lexicographically smallest sorted placement array, comparing each `(id, tile)`.

Verifier scenes may have many candidate cells and legal tiles. A full combination/product scan is not a required or reliable strategy. A selected candidate changes the replay only if a packet actually enters that cell during that board's simulation; candidates never entered by any packet still count toward `place_exactly`, and their ids/tiles are chosen only by the score tie-break.

## Simulation

Simulate integer ticks `0` through `max_ticks`. Initial sources enter at tick `0`. Releases scheduled after `max_ticks` are ignored.

For each tick:

1. Add scheduled delayed releases for the tick.
2. Batch live packets by `(x, y, direction)`. A batch charge is the clamped sum of charges to `[-9, 9]`. A batch formed from `n` packets adds `n-1` to `collision_count`.
3. Process batches by ascending `(x, y, direction_order)`.
4. Outside-grid entries add one `leak_count`. Wall entries (`#`) add one `blocked_count`.
5. Accepted entries update cell flux immediately: `cell_flux[x,y] += abs(charge)`. A zero-charge batch has flux `0` but still counts as an accepted visit for stateful tile decisions.
6. The tick load contribution of an accepted batch is `(abs(charge)+1)*(x+3)*(y+5) + 11*(direction_index+1) + accepted_visits_for_cell_after_this_batch`.

Tile effects are applied after the immediate flux and visit update:

- `.` no change.
- `^`, `>`, `v`, `<` set the outgoing direction.
- `/` reflects `N->E`, `E->N`, `S->W`, `W->S`.
- `\` reflects `N->W`, `W->N`, `S->E`, `E->S`.
- `L` turns left.
- `R` turns right.
- `B` reverses direction and negates charge.
- `A` increases charge one step away from zero, clamped to `[-9, 9]`; zero becomes `1`.
- `D` moves charge one step toward zero and increments `damped_count`; if the result is zero, the batch is absorbed.
- `C` turns right when the accepted visit count for the cell is odd, otherwise left.
- `F` passes unchanged when `(charge + tick + accepted_visits_for_cell_after_this_batch)` is even; otherwise it reverses direction, moves charge one step toward zero, increments `damped_count`, and absorbs the batch if the result is zero.
- `G` compares the cell's final flux after this batch to `optimizer.gradient_threshold`, defaulting to `6`. If the flux is greater than the threshold, it turns right and moves charge one step away from zero. If the flux is equal to or below the threshold, it turns left, moves charge one step toward zero, increments `damped_count`, and absorbs the batch if the result is zero.
- `T` schedules the batch as a new entry to the same `(x, y)` cell at `tick + 2`, with charge unchanged. The release direction is computed from the direction the batch had when it entered `T`: turn right if that scheduling tick was odd, and left if it was even. The released entry is then grouped and processed normally on its release tick, including flux, visit, checksum, and the current tile effect at that same cell. It increments `delay_count` when scheduled and does not also move on the scheduling tick.
- `S` splits into three packets for `tick + 1` after moving one cell in each outgoing direction: forward with the same charge, left with charge moved one step toward zero, and right with charge moved one step away from zero.

Non-absorbed, non-delayed, non-split batches move one cell in their outgoing direction and enter on `tick + 1`.

`trail_checksum` is updated for every accepted batch:

`(trail_checksum + (tick+1)*97 + (x+1)*31 + (y+1)*43 + (direction_index+1)*17 + (charge+11)*13 + accepted_visits_for_cell_after_this_batch*7) % 1000003`

`tick_checksum` is updated after each tick with nonzero load:

`(tick_checksum + (tick+1)*131 + load*17 + live_batches_processed*19) % 1000003`

`live_batches_processed` means every grouped batch processed during that tick, including batches that later leak outside the grid or hit a wall.

`visited_cells` is the number of cells with positive final flux. `total_flux` is the sum of final flux. `active_ticks` counts ticks with nonzero load. `first_active_tick` and `last_active_tick` are `-1` if no tick is active. `peak_tick` is the earliest tick with maximum load, or `-1` if all loads are zero.

## Artifacts

Write JSON with sorted keys, no indentation, normal integers, and no extra keys. JSON is minified: use no whitespace between tokens, equivalent to Python `json.dumps(payload, sort_keys=True, separators=(",", ":"))`.

`tuning.json`:

`{"placements":[{"id":str,"tile":str}],"score":int}`

`flow_report.json`:

`{"blocked_count":int,"collision_count":int,"damped_count":int,"leak_count":int,"top_cells":[{"flux":int,"x":int,"y":int}],"total_flux":int,"trail_checksum":int,"visited_cells":int}`

`top_cells` contains up to eight positive-flux cells sorted by descending `flux`, then `y`, then `x`.

`phase_report.json`:

`{"active_ticks":int,"delay_count":int,"first_active_tick":int,"last_active_tick":int,"peak_load":int,"peak_tick":int,"steady_span":int,"tick_checksum":int,"top_ticks":[{"load":int,"tick":int}]}`

`top_ticks` contains up to eight nonzero-load ticks sorted by descending `load`, then ascending `tick`.

## PPM Raster

Write `/app/render/mosaic.ppm` as ASCII P3:

`P3`

`<width> <height>`

`255`

Then one image row per line, with RGB integers separated by single spaces.
End the file with a newline after the final image row.

Renderer settings live in `scene["renderer"]`: `cell_size`, `margin`, `background`, `wall`, `gridline`, `hot`, and `candidate`.
The image width is `2*margin + grid_width*cell_size + (grid_width+1)`.
The image height is `2*margin + grid_height*cell_size + (grid_height+1)`.
Pixels in the margin band outside the grid rectangle use `background`. Gridline pixels use `gridline`. Interior wall pixels use `wall`. Interior non-wall pixels use `background + min(255, flux*hot)` per channel, clamped to `255`. Candidate cells with zero flux add the `candidate` color offset before clamping.
