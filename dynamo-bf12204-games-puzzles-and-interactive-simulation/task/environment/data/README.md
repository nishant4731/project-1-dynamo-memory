Scene rules for `/app/data/scene.json`:

- Coordinates are zero-based: `x` increases right, `y` increases down. Directions are `N`, `E`, `S`, `W`. Colors are bitmasks: red=1, green=2, blue=4.
- Choose exactly `optimizer.place_exactly` candidates, replacing each with one tile from `optimizer.choices`; unchosen candidates keep their original grid tile.
- The placement score is `1000003*energized_cells + checksum + 17*cycle_cutoffs + peak_bonus*peak_load`, with missing `peak_bonus` equal to 0.
  Break ties by the lexicographically smallest `(id, tile)` placement list sorted by `id`.
- Simulate ticks 0 through `max_ticks`. Add delayed releases, batch live entries by `(x, y, direction)` with ORed colors, then process batches by
  ascending `x`, `y`, and direction order `N`, `E`, `S`, `W`. Heat is updated immediately, so earlier batches affect later heat-sensitive tiles in the same tick.
- Drop repeated `(x, y, direction, color, tick mod 4)` states before heating and count them as cycle cutoffs. Outside-grid entries count as exits; `#` entries count as absorbed.
- `/` maps `N->E`, `E->N`, `S->W`, `W->S`; `\` maps `N->W`, `W->N`, `S->E`, `E->S`.
- `|` splits east/west beams north and south, otherwise passes. `-` splits north/south beams east and west, otherwise passes.
- `T` is `/` on even ticks and `\` on odd ticks. `O` is `|`, `-`, `.` for `tick mod 3` equal to 0, 1, 2.
- After heating, `M` uses `/` only if `red_hits + blue_hits > green_hits`; equality uses `\`.
- After heating, `F` keeps only incoming color channels whose per-channel hit count at that cell is odd; even channels are removed.
- `Q` toggles `color ^= 1 << ((x+y+tick+direction_order) mod 3)` after heating/load, stops if zero, then turns clockwise when the tick load so far is odd, otherwise counterclockwise.
- `C` turns clockwise; `A` counterclockwise. `P` emits red left, green straight, and blue right. `R` rotates color left once (`red->green->blue->red`) and passes.
- `D` schedules one beam at `t + 1 + ((red_hits + 2*green_hits + 3*blue_hits + color + direction_order) mod 3)`, one step forward in the same
  direction, with color rotated left `delay-1`; releases after `max_ticks` are ignored.
- Digits are portals. Use the largest portal revision `(effective_tick, sequence)` whose effective tick is no later than the current tick.
  Before any revision is effective, that digit acts as `.`. If a digit has no revisions and exactly two final-grid cells after placements, use those
  as a fallback portal pair with `color_xor = 0`; otherwise it has no fallback.
