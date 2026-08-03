Produce the calibrated output bundle for the signed-packet board stored in `/app/data/scene.json`.

The complete contract is the rulebook at `/app/data/README.md`. It defines the coordinate system, legal tile alphabet, batching order, counters, checksums, JSON field shapes, score formula, and PPM raster layout. Follow that file when this short prompt omits a detail.

`/app/render` must contain only:

- `tuning.json`
- `flow_report.json`
- `phase_report.json`
- `mosaic.ppm`
- `solver.py`

Select exactly `optimizer.place_exactly` candidate ids and assign each selected id one tile from `optimizer.choices`. Compare all legal selections by the documented score; for an equal score, sort each placement list by `(id, tile)` and choose the lexicographically smallest list. Build every report and the picture from this winning board.

Hidden scenes may make the raw candidate/tile product too large to enumerate within the verifier budget. The README rule about candidates that are never entered by packets is part of the contract; a reusable solver must still choose their placement rows by the tie-break when they fill unused selection slots.

Three order-sensitive points are easy to get wrong:

- Arrivals sharing a tick are handled as grouped batches in the README order. Count an accepted batch's visit and flux before stateful tiles branch or emit later packets.
- Tile `G` uses strict comparison after that flux update: `cell_flux > optimizer.gradient_threshold` grows charge and turns right; equality follows the damped left-turn path.
- Tile `T` re-enters the same cell at `tick + 2` as a normal future entry. Its release direction is based on the scheduling tick and the direction that entered `T`, then the current tile at that same cell is processed again.
- The PPM canvas starts as the renderer `background`; the margin outside the grid rectangle is never repainted as gridline or cell interior.

Copy reusable Python into `/app/render/solver.py`. It must export `solve_scene(scene_path, output_dir)` and importing it must not run a solve. The verifier imports that function for new valid scenes with different timing collisions, margins, candidate choices, arrow retargeting, delayed/split packets, gradient thresholds, zero-charge visits, larger sparse candidate sets, and placement ties, so a solution tied to the visible input is not acceptable.
