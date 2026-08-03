Create executable Python 3 CLI `/app/recover_bounce.py`.

Run: `python3 /app/recover_bounce.py INPUT_DIR OUTPUT_WAV REPORT_JSON`.

Shipped input is `/app/session`; write `/app/session/master.wav` and `/app/session/mix_report.json`. `INPUT_DIR` has `manifest.json`, `ledger.tsv`, `latency.tsv`, `bus.tsv`, `tap.tsv`, and `stems/`. If `stems/` is missing at startup, exit nonzero and write no outputs. On success, write both outputs, then recursively delete `INPUT_DIR/stems/`. Do not modify the five metadata files.

Schemas:
- `manifest.json`: `sample_rate`, `channels`, `bar_samples`, `headroom_permille`.
- `ledger.tsv`: `event	stem_id	revision	state	track	start_bar	trim_head	trim_tail	gain_num	gain_den	phase	pan_permille	sha16`
- `latency.tsv`: `event	stem_id	revision	status	extra_samples`
- `bus.tsv`: `event	stem_id	revision	status	lane	polarity_flip	pan_delta	slip_mod`
- `tap.tsv`: `event	stem_id	revision	status	tap_sample	gain_step`

For every TSV, a stem's current row is max `(revision,event,file_row_index)`, numeric ascending comparison, where later file rows have larger indexes. Non-current rows count toward that file's ignored/stale counter. Current ledger rows contribute only when `state=ACTIVE`; other current ledger rows increment `revoked_current`. Current latency rows contribute only when `status=KEEP`; others increment `latency_rows_ignored`. Current bus rows contribute only when `status=ROUTE`; others increment `bus_rows_ignored`. Current tap rows contribute only when `status=TAP`; others increment `tap_rows_ignored`. Missing route defaults to `lane=0, polarity_flip=0, pan_delta=0, slip_mod=1`; missing tap means `tap_gain=1, tap_level=0`.

`active_span` is max `start_bar` over all current `ACTIVE` ledger rows, including later rejects; use `-1` if none.

For each current `ACTIVE` stem, read `INPUT_DIR/stems/<stem_id>.wav`; require mono 16-bit PCM at manifest `sample_rate`. Trim `trim_head`/`trim_tail`; apply `phase` (`1` or `-1`) and exact integer gain `sample*gain_num//gain_den`, rejecting non-divisible products, out-of-int16 samples, and lengths other than 480. Left-rotate by `(abs(event)+track*7+start_bar*3)%480`. Authenticate with SHA-256 of little-endian signed int32 `active_span` plus rotated little-endian int16 frame bytes; compare first 16 lowercase hex chars to `sha16`.

Quarantine missing/bad WAVs, bad trim/gain/length/range/digest stems, and duplicate `(track,start_bar)` losers. `digest_rejects` counts rejected current `ACTIVE` stems except duplicate losers. Duplicate resolution uses ledger `(track,start_bar)` before route offsets; lexicographically smallest `stem_id` wins.

For winners: `bus_offset=0` if `slip_mod<=1`, else `(abs(bus event)+lane*track+start_bar)%slip_mod`. `start_sample=start_bar*bar_samples+extra_samples+bus_offset`. Fade with `fade_in=16+(start_bar%8)` and `fade_out=16+(track%8)`: at index `j`, multiply by `(j+1)//fade_in` when `j<fade_in`, and by `(480-j)//fade_out` when `j>=480-fade_out`. After fades, if `polarity_flip` is odd, reverse and negate. Clamp `pan_permille+pan_delta` to `[0,1000]`; weights are `isqrt((1000-pan)*1000)` and `isqrt(pan*1000)`. L/R contributions are `sample*weight//1000` using signed floor division.

Mix through the last occupied frame in ascending `(start_sample,track,stem_id)`. Before a tapped winner contributes, read current pre-clip mix at `start_sample+tap_sample`, after earlier winners only. If the frame is out of range or unoccupied, `tap_level=0,tap_gain=1`; otherwise `tap_level=abs(left_mix)+abs(right_mix)` and `tap_gain=2+((tap_level+abs(tap event)+gain_step)%3)`. Multiply that winner's L/R contributions by `tap_gain` before overlap handling; `tap_adjusted_samples` counts adjusted contribution frames, not channels. If a destination frame is already occupied, multiply the new contribution by `headroom_permille//1000` before adding and increment `overlap_ducked_samples`. After summing, clip stereo samples to int16; `clipped_frames` counts frames where either channel clipped, and `pre_clip_peak` is max absolute pre-clip channel sum.

`OUTPUT_WAV`: stereo interleaved 16-bit PCM at manifest `sample_rate`.

`REPORT_JSON`: UTF-8 JSON with exactly `sample_rate`, `channels`, `bar_samples`, `frames_written`, `stems_used`, `quarantined_stems`, `stale_ledger_rows`, `revoked_current`, `digest_rejects`, `duplicate_placement_rejects`, `latency_rows_ignored`, `bus_rows_ignored`, `tap_rows_ignored`, `headroom_permille`, `pre_clip_peak`, `clipped_frames`, `overlap_ducked_samples`, `tap_adjusted_samples`, `stem_placements`, `route_checksum`, `tap_checksum`, `active_span`, `consumed_evidence`.

`stems_used` is winner ids in mix order; `quarantined_stems` sorted ids; `frames_written` output frame count; `consumed_evidence` true iff `stems/` was deleted. Each `stem_placements` entry has `stem_id`, `track`, `start_bar`, `start_sample`, `rotation`, effective `pan_permille`, `lane`, `bus_offset`, `tap_gain`, `tap_level`. `route_checksum`: start 0, for each winner add `(start_sample%1009)*(lane+1)+rotation*(pan_permille+1)+bus_offset`, modulo `1000003`. `tap_checksum`: start 0, for each winner with current `TAP` add `(tap_level%1009)*tap_gain+abs(tap event)+(start_sample%997)`, modulo `1000003`.
