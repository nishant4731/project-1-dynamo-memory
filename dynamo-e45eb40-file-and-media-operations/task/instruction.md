Create executable Python 3 program `/app/restore_session.py`.

Run:

`python3 /app/restore_session.py INPUT_DIR OUTPUT_WAV REPORT_JSON`

`INPUT_DIR` contains `ledger.tsv`, `calibration.tsv`, `chunks/`, and may contain `patches.tsv` and `adjustments.tsv`. Rebuild the canonical mono 16-bit PCM WAV reel at 8000 Hz into `OUTPUT_WAV`, write `REPORT_JSON`, and leave every input file and chunk unchanged.

TSV headers:

- `ledger.tsv`: `event	chunk	revision	state	slot	trim_left	trim_right	scale	polarity	sha16`
- `calibration.tsv`: `event	tap	revision	status	observed	canonical`
- optional `patches.tsv`: `event	chunk	revision	status	start	stride	values`
- optional `adjustments.tsv`: `event	slot	revision	status	shift	gain_numer	gain_denom`

Current-row rule for chunks, taps, `(chunk,start)` patches, and slots: highest numeric `revision`; tie larger numeric `event`; tie later file row. Non-current rows are ignored.

Only current ledger rows with `state` `ACTIVE` may contribute. Current non-`ACTIVE` rows count as revoked. `active_span` is the max numeric `slot` over all current `ACTIVE` rows, including later-quarantined rows; if none, `-1`.

For each current `ACTIVE` chunk, read `chunks/<chunk>.wav`. Before trimming, apply current patch rows with `status` `APPLY` for that chunk: split comma-separated signed integer `values`; add value `j` to raw sample index `start + j * stride`. `start >= 0`, `stride > 0`, all referenced indexes must exist, and patched raw samples must remain int16. Current patch rows with other statuses are ignored.

Then trim `trim_left` samples from the start and `trim_right` from the end. Undo storage transform: multiply each trimmed sample by `polarity` (`1` or `-1`), then divide by integer `scale`. `scale` must be non-zero, all divisions exact, and normalized samples must remain int16. The normalized frame must be exactly 320 samples.

Left-rotate the normalized frame by the per-row offset determined by that row's `event` and `slot`; signed events use absolute magnitude. Recover the exact offset rule by matching candidate rotations against `sha16`. Authenticate before calibration: SHA-256 over little-endian signed 32-bit `active_span` followed by little-endian signed 16-bit rotated samples; first 16 lowercase hex chars must equal `sha16`. Quarantine on missing WAV, bad WAV params, invalid patch, trim/scale/exactness/clip/length failure, or digest mismatch.

If several valid candidates share a numeric `slot`, keep the lexicographically first `chunk` string by Unicode code point and quarantine the rest.

Calibration: current rows with `status` other than `KEEP` are ignored. For each current `KEEP`, lane is `(tap + active_span) % 7`; lane bias is `observed - canonical`. If several current `KEEP` rows map to one lane, use the smallest numeric `tap` and ignore the rest. Inputs provide at least one `KEEP` for every lane 0..6. `bias_vector` lists lanes 0..6.

Assemble slots `0..max_used_slot`; missing slots are 320 zeros. For a used slot, subtract `bias_vector[(slot * 320 + sample_index) % 7]` from each rotated sample. Then apply current adjustment row with `status` `KEEP` for that slot, if any: left-rotate by `shift % 320`, multiply by `gain_numer`, divide by non-zero `gain_denom`; all divisions exact and adjusted samples int16. Current adjustments with other statuses are ignored.

`pre_crossfade_peak` is max absolute used-slot sample after bias and adjustment, before boundary repair; if no used slots, `0`. Boundary repair runs only between adjacent used numeric slots. `blend_width = 4 + (active_span % 5)` if `active_span >= 0`, else `0`. For each repaired boundary, append the right-hand slot number and the pre-blend sum of the left slot's last `blend_width` samples plus right slot's first `blend_width` samples. For `k = 0..blend_width-1`, blend pair `left[320-blend_width+k]`, `right[k]` into `trunc_toward_zero((2*left + right) / 3)`; write that value into both paired positions. Never blend across gaps or change slot length.

`REPORT_JSON` is UTF-8 JSON with exactly these keys:

`sample_rate`, `frames_written`, `chunks_used`, `quarantined_chunks`, `stale_rows_ignored`, `revoked_current`, `digest_rejects`, `duplicate_slot_rejects`, `gap_slots`, `calibration_rows_ignored`, `patch_rows_ignored`, `patches_applied`, `adjustment_rows_ignored`, `bias_vector`, `adjusted_slots`, `crossfade_boundaries`, `boundary_raw_sums`, `rotation_offsets`, `pre_crossfade_peak`, `active_span`, `blend_width`

Meanings:

- `sample_rate`: integer `8000`
- `frames_written`: output sample count
- `chunks_used`: winning chunk ids in ascending slot order
- `quarantined_chunks`: sorted chunk ids from current `ACTIVE` rows rejected by validation or duplicate-slot loss
- `stale_rows_ignored`: non-current ledger rows
- `revoked_current`: current non-`ACTIVE` ledger rows
- `digest_rejects`: integer count of current `ACTIVE` rows rejected before duplicate-slot resolution
- `duplicate_slot_rejects`: integer count of valid candidates dropped only by duplicate-slot resolution
- `gap_slots`: ascending slots filled with silence
- `calibration_rows_ignored`: non-current calibration rows plus current non-`KEEP` plus same-lane `KEEP` rows not selected
- `patch_rows_ignored`: non-current patch rows plus current non-`APPLY`; `0` if absent
- `patches_applied`: current `APPLY` patch rows applied before validation, including later-rejected candidates
- `adjustment_rows_ignored`: non-current adjustment rows plus current non-`KEEP`; `0` if absent
- `bias_vector`: seven integers, lanes 0..6
- `adjusted_slots`: ascending used slots receiving current `KEEP` adjustment
- `crossfade_boundaries`: ascending right-hand slots repaired
- `boundary_raw_sums`: pre-blend edge sums aligned with `crossfade_boundaries`
- `rotation_offsets`: offsets for `chunks_used`, same order
- `pre_crossfade_peak`, `active_span`, `blend_width`: integers defined above
