A texture-packing tool must fit a set of textures into a fixed GPU memory page. Each texture can be stored in one of several compression variants, and you must pick exactly one variant per texture.

The input comes from a legacy streaming manifest. Besides memory fit and quality loss, the chosen variants must preserve four published manifest-compatibility registers used by an existing incremental patcher and runtime cache: a page-table bucket, a rolling manifest checksum, an adjacent-texture seam bucket, and a second-order adjacent-window bucket. Their formulas are part of the manifest ABI and are supplied below; they are required compatibility constraints, not optional post-processing checks.

Write a self-contained Python program at `/app/solve.py`, invoked as `python3 -S /app/solve.py <instance.json> <out.json>`, that reads an instance and writes the optimal selection. The `-S` flag disables site-packages, so rely only on the Python standard library and code in `/app/solve.py`; do not depend on installed optimizer, SAT/SMT/ILP, or constraint-programming packages. Hidden instances vary texture count, variant count, moduli, and upload period, so solve from the spec rather than enumerating every selection.

`instance.json` (all keys normative):

- `budget`: integer, the page size in blocks.
- `tier1_count`: integer, the exact number of tier-1 variants to select.
- `residue_mod`: integer modulus for the manifest page-table bucket.
- `residue_target`: integer target residue the selected page-table bucket must match.
- `checksum_mod`: integer modulus for the rolling manifest checksum.
- `checksum_target`: integer target rolling manifest checksum.
- `neighbor_mod`: integer modulus for the adjacent-texture seam bucket.
- `neighbor_target`: integer target adjacent-texture seam bucket.
- `window_mod`: integer modulus for the second-order adjacent-window bucket.
- `window_target`: integer target second-order adjacent-window bucket.
- `load_period`: integer number of cyclic upload slots.
- `streak_penalty`: integer multiplier for contiguous tier-1 selections; it may be zero.
- `peak_penalty`: integer multiplier for the busiest upload slot; it may be zero.
- `upload_spread_penalty`: integer multiplier for cumulative in-order upload imbalance; it may be zero.
- `tier1_by_family`: object mapping each texture family to its exact tier-1 pick count. The values sum to `tier1_count`.
- `tier1_cost_by_family`: object mapping each texture family to the exact total `cost` from chosen tier-1 variants. It has the same keys as `tier1_by_family`.
- `assets`: array of textures in rendering order. Each has `id`, `family`, and `variants`; each variant has integer `cost`, `loss`, `tier` (`0` or `1`), `residue`, and `upload`.

Choose exactly one variant per texture so that all of these hold exactly:

- the chosen variants' `cost` values sum to exactly `budget` (the page must be filled with no waste and no overflow), and
- exactly `tier1_count` of the chosen variants have `tier` equal to `1`.
- for every family named in `tier1_by_family`, exactly that many chosen variants from textures in that family have `tier` equal to `1`.
- for every family named in `tier1_cost_by_family`, the chosen tier-1 variants from textures in that family have `cost` values summing to exactly that family's target.
- the manifest page-table bucket equals `residue_target`, where:

      page_signature = sum((texture_position + 1) * chosen_variant.residue for each texture) % residue_mod

  `texture_position` is 0-based in the `assets` array, so the first texture has multiplier 1, the second has multiplier 2, and so on.
- the rolling manifest checksum equals `checksum_target`. Start `rolling_checksum = 0`, then process textures in array order and update:

      rolling_checksum = (rolling_checksum * (chosen_variant.residue + 2) + chosen_variant.cost + chosen_variant.upload) % checksum_mod

- the adjacent-texture seam bucket equals `neighbor_target`. Start `neighbor_signature = 0`. For each texture after the first, let `previous_residue` be the residue of the variant chosen for the immediately preceding texture, and update:

      neighbor_signature = (neighbor_signature + (texture_position + 1) * (previous_residue + 1) * (chosen_variant.residue + 3)) % neighbor_mod

  The first texture contributes nothing to `neighbor_signature`.
- the second-order adjacent-window bucket equals `window_target`. Start `window_signature = 0`. For each texture after the second, let `two_back_residue` and `previous_residue` be the residues of the variants chosen two positions back and one position back, respectively, and update:

      window_signature = (window_signature * (chosen_variant.residue + 5) + (texture_position + 1) * (two_back_residue + 1) * (previous_residue + 2) + chosen_variant.upload) % window_mod

  The first two textures contribute nothing to `window_signature`.

Among all selections satisfying all exact constraints, output one that minimizes the total effective quality loss, defined as:

    total_loss = sum(chosen variants' loss) + max_tier1_streak * streak_penalty + peak_upload_load * peak_penalty + cumulative_upload_spread * upload_spread_penalty

where `max_tier1_streak` is the length of the longest contiguous sequence of textures (in array order) for which a tier-1 (`tier == 1`) variant was chosen. (If `tier1_count == 0`, `max_tier1_streak` is 0.) Every instance has at least one feasible selection.

For `peak_upload_load`, assign each chosen variant to upload slot `(texture_position + chosen_variant.residue) % load_period`, sum the chosen variants' `upload` values per slot, and take the maximum slot sum. Slots with no assigned upload have load 0.

For `cumulative_upload_spread`, process textures in array order using the same upload-slot rule. After each assignment, add its `upload` to the running slot load, compute `current_spread = max(slot_loads) - min(slot_loads)`, and sum those values over every texture position. This penalizes transient upload imbalance, not only the final busiest slot.

Write `<out.json>` as a JSON object with a single key `selection`: an object mapping each texture `id` to the integer index (0-based, into that texture's `variants` array) of the chosen variant. For example: `{"selection": {"tex00": 2, "tex01": 0, ...}}`.

Grading, per instance: the selection must choose exactly one valid variant per texture, satisfy all exact constraints, and achieve the minimal feasible `total_loss`. Any instance where the selection is infeasible or not minimal fails.
