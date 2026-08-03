`/app/data/reel.rgb` is an uncompressed RGB24 archive reel. `/app/data/reel_spec.json` gives its `width`, `height`, `archive_frame_count`, `master_frame_count`, and `delivery_cutoff`. Each archive frame is exactly `width * height * 3` bytes. `/app/data/fragment_catalog.csv` maps `archive_index` values to the slot, revision, fragment part, effective timestamp, capture timestamp, and quality status for that archive frame.

Recover the delivery master as it existed at the delivery cutoff and write two files:

`/app/recovered_master.rgb`: raw RGB24 frames for slots `0` through `master_frame_count - 1`, in ascending slot order, using the same width and height as the archive reel.

`/app/recovery_report.json`: UTF-8 JSON with exactly these top-level keys: `width`, `height`, `frame_count`, `cutoff`, `master_sha256`, `frames`. `frames` must be a list in ascending slot order. Each frame entry must have exactly `slot`, `revision`, `method`, and `source_archive_indices`.

Use only catalog rows with `status` equal to `ok` and `effective_at` at or before `delivery_cutoff`. For each slot, the authoritative revision is the highest remaining numeric revision. If multiple ok rows exist for the same slot, revision, and part, use the row with the latest `captured_at`; if that still ties, use the lowest `archive_index`.

Assemble each authoritative frame this way. A `FULL` part contains the whole frame and takes precedence over all other parts; report method `full` and source indices `[FULL]`. A `DELTA` part contains a whole-frame bytewise XOR delta from the previous numeric revision for the same slot to the current revision. If there is no usable `FULL` and a usable `DELTA` exists, first assemble the previous revision using these same rules, XOR that full previous-revision frame with the `DELTA` frame, report method `delta`, and list the previous revision's source indices in their normal order followed by `[DELTA]`.

A `LEFT` part stores the left half of the frame in the left half of its archive frame, with zero padding on the right. A `RIGHT` part stores the right half in the right half of its archive frame, with zero padding on the left. A `PARITY` part stores, in the left half of its archive frame, the bytewise XOR of the true left and right halves. If there is no usable `FULL` or `DELTA`, use `LEFT` plus `RIGHT` when both are available and report method `left_right` with indices `[LEFT, RIGHT]`. If exactly one half is missing and `PARITY` is available, recover the missing half by XORing the known half with the parity half; report `left_parity` with indices `[LEFT, PARITY]` or `right_parity` with indices `[RIGHT, PARITY]`.

`master_sha256` in the report must be the lowercase SHA-256 hex digest of `/app/recovered_master.rgb`. Timestamps in the catalog and spec are UTC ISO-8601 strings ending in `Z`.
