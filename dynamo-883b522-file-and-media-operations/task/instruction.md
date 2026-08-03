Build a reusable program at `/app/solve.py`, then use it to assemble the composite described by `/app/composite_job/manifest.json`.

The program must accept exactly three arguments: the job directory, an output composite PGM path, and an output selection JSON path.

The manifest has `grid` (`rows`, `cols`, `tile_height`, `tile_width`), an integer `target_key` in `[0, 255]`, integer bonuses `peak_bonus` and `median_bonus` (both >= 0), and `cells`: a list of `rows * cols` cells in row-major order (the cell at grid position `(r, c)` is at index `r*cols + c`). Each cell has `candidates`, a non-empty list of tiles; every tile is a `tile_height`-by-`tile_width` grid of integer pixel values in `[0, 255]` (row-major).

For a tile, its tone is the sum of all its pixel values, and its sharpness is the total variation: the sum, over every horizontally adjacent and every vertically adjacent pixel pair within the tile, of the absolute difference of the two pixels.

Choose exactly one candidate tile for every cell. Consider the cells as a sequence in row-major order. The sequence maintains a running phase `m` in `{0, 1, 2}`, initialized to `m = 0` before cell 0. For cell `j` with running phase `m`, choosing a tile with raw tone `t` and sharpness `s` yields an effective tone `t_eff = (t + m * s) mod 256`, and updates the phase for cell `j+1` to `(m + t) mod 3`. Let the prefix residue after cell `j` be `(t_eff_0 + t_eff_1 + ... + t_eff_j) mod 256`. Define `peak` as the maximum prefix residue over `j = 0 .. N-1`. Define `median` as the lower median of the `N` prefix residues after sorting them in nondecreasing order, at index `(N-1)//2`. Define `total_sharpness` as the sum of the chosen tiles' sharpness.

Your selection must satisfy the constraint that the final prefix residue (after the last cell) equals `target_key`. Among all selections satisfying the constraint, MAXIMIZE the objective `total_sharpness + peak_bonus * peak + median_bonus * median`. At least one selection satisfying the constraint always exists.

Write the assembled composite to the given path as a valid binary `P5` PGM (max value 255) with dimensions `(rows * tile_height)` rows by `(cols * tile_width)` columns; the chosen tile for cell `(r, c)` occupies rows `[r*tile_height, (r+1)*tile_height)` and columns `[c*tile_width, (c+1)*tile_width)`.

Write the selection report to the given JSON path as UTF-8 JSON with exactly these keys: `chosen_indices` (a list of `rows * cols` integers in row-major cell order, each the chosen candidate's index within its cell's `candidates`), `total_sharpness`, `peak`, `median`, `objective` (the achieved `total_sharpness + peak_bonus * peak + median_bonus * median`), and `tone_key` (the final prefix residue, which must equal `target_key`).

If several selections achieve the same maximum objective, choose the one whose `chosen_indices` list is lexicographically largest. The composite and `chosen_indices` must describe that same selection, and `objective` must equal the true constrained maximum.
