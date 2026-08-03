# Vault Filter Contract

Build `/app/filter_vault.py` as a reusable Python 3 command invoked with an input
vault and an output directory. For the visible task the invocation is
`/app/filter_vault.py /app/vault /app/filtered`.

Inputs are TSV files `/app/vault/manifest.tsv`, `/app/vault/profiles.tsv`,
`/app/vault/renewals.tsv`, `/app/vault/overrides.tsv`,
`/app/vault/receipts.tsv`, `/app/vault/media_ops.tsv`,
`/app/vault/bundles.tsv`, marker files below
`/app/vault/markers`, and payload files named by manifest `relpath`. TSV
headers define field names.

## Manifest And Payload Validation

A manifest row is malformed unless `seq`, `revision`, `priority`, and
`declared_size` are decimal integers. Count and ignore malformed rows. For each
`record_id`, choose the well-formed manifest row with greatest `revision`, then
latest `seen_at`, then greatest numeric `seq`; other well-formed rows are
rejected as `superseded_manifest`.

Resolve the selected `relpath` under the input vault. Reject as `unsafe_path` if
it is absolute, empty, contains `.` or `..`, escapes the vault, or crosses any
symlink component. A safe target that is missing or not a regular file is
`missing_file`.

After path checks, apply these rejection stages in this order: size or sha256
mismatch is `digest_mismatch`; no profile for `region` is `unknown_region`;
lower-case extension not in `allowed_exts` is `extension_reject`; size outside
inclusive `min_size` and `max_size` is `size_reject`; payload bytes not starting
with `magic_hex` are `magic_reject`.

## Overrides, Renewals, And Staleness

Override rows are valid only when `status` is `active`, `priority_delta` is an
integer, `/app/vault/markers/<override_id>.mrk` exists, and that marker's sha256
equals `marker_sha256`; invalid rows increment `invalid_overrides`. For each
record, keep the valid override with latest `issued_at`, then lexical
`override_id`. Apply it only when `issued_at >= captured_at`: non-`-`
`tag_override` replaces the tag, `priority_delta` changes base priority, non-`-`
`stale_before` replaces the stale floor, and the id is reported. Otherwise keep
the original fields and report `override_id = null`.

Renewal rows use the same marker/status rule, with integer `bonus` and
`/app/vault/markers/<renewal_id>.mrk`; invalid rows increment `invalid_renewals`.
For each record, keep the valid renewal with latest `issued_at`, then lexical
`renewal_id`. Apply it only when `issued_at >= captured_at`: set `effective_time`
to `issued_at`, set `effective_priority` to base priority plus `bonus`, and
report the id. Otherwise use `captured_at`, base priority, and
`renewal_id = null`. If `effective_time` is before the stale floor, reject as
`stale_without_renewal`.

## Receipt Proofs, Media Operations, And Bundle Promotions

Receipt rows are checked only for records that have survived manifest, path,
payload, profile, override, and renewal processing. A row in `receipts.tsv` is
invalid when `status` is not `active`, integer fields fail to parse,
`window_start < 0`, `window_len <= 0`, `window_stride <= 0`, the sampled window
extends past the payload byte length, `/app/vault/markers/<receipt_id>.mrk` is
missing, the marker sha256 differs from `marker_sha256`, or `proof16` is wrong.
Invalid rows increment `invalid_receipts`; valid rows increment
`valid_receipts`.

For proof validation, sample payload bytes at offsets `window_start`,
`window_start + window_stride`, and so on while the offset is less than
`window_start + window_len`. `proof16` is the first 16 lowercase hex characters
of sha256 over UTF-8 text joining `receipt_id`, `record_id`, the selected
payload's full sha256, sampled bytes as lowercase hex, and `issued_at` with
`|`.

For each record, among valid receipt rows with `issued_at >= effective_time`,
apply the row with latest `issued_at`, then lexical `receipt_id`. Apply receipts
before stale filtering: add `priority_delta` to `effective_priority`, replace
the tag when `tag_override` is not `-`, replace the stale floor when
`stale_before` is not `-`, report `receipt_id`, increment `receipts_applied`,
and add the delta to `receipt_bonus_total`. Valid receipts older than the
record's current `effective_time` count as valid but do not apply.

Media operation rows are checked only for records that have survived receipt
processing and stale filtering. Rows in `media_ops.tsv` have header `op_id`,
`record_id`, `issued_at`, `opcode`, `offset`, `length`, `arg_hex`,
`priority_delta`, `tag_override`, `marker_sha256`, `status`. A row is invalid
when `status` is not `active`, integer fields fail to parse, `opcode` is not
`mask`, `xor`, or `clip`, `offset < 0`, `length <= 0`,
`/app/vault/markers/<op_id>.mrk` is missing, or the marker sha256 differs from
`marker_sha256`. `mask` and `xor` require nonempty lowercase-even hex
`arg_hex`; `clip` requires `arg_hex = -`.

For each surviving record, examine rows for that record ordered by `issued_at`,
then `op_id`. Valid rows older than the current `effective_time` increment
`valid_media_ops` but do not apply. For rows with `issued_at >= effective_time`,
validate the byte range against the payload state after earlier applied media
operations for that record; out-of-range rows are invalid. Apply valid rows in
that order: `mask` replaces the range with repeated `arg_hex` bytes, `xor`
XORs the range with repeated `arg_hex` bytes, and `clip` removes the range.
Each applied row adds `priority_delta` to `effective_priority`, retags when
`tag_override` is not `-`, appends its `op_id` to the accepted entry's
`media_ops`, increments `media_ops_applied`, adds to `media_priority_total`,
and contributes its byte-length change to `media_bytes_delta`. Transformed
payload bytes, not raw payload bytes, are used for bucket byte-size ranking,
copying, report `bytes`, and `media_digest`.

Bundle rows are validated once after candidate construction and before bucket
caps. A row in `bundles.tsv` is invalid when `status` is not `active`, integer
fields fail to parse, `min_members <= 0`, `/app/vault/markers/<bundle_id>.mrk`
is missing, or the marker sha256 differs from `marker_sha256`. Invalid rows
increment `invalid_bundles`; valid rows increment `valid_bundles`.

Bundle eligibility is computed from the candidate state before any bundle is
applied. A candidate is eligible when its current `region` and `tag` exactly
match the bundle row and its current `effective_priority >= min_priority`. A
bundle activates only when at least `min_members` candidates are eligible. For a
candidate eligible for multiple active bundles, choose highest `min_members`,
then highest `priority_delta`, then lexical `bundle_id`. Apply the chosen
bundle by adding `priority_delta` to `effective_priority`, replacing the tag
when `tag_override` is not `-`, reporting `bundle_id`, incrementing
`bundles_applied`, and adding the delta to `bundle_bonus_total`. Bundle retags
affect bucket caps and copy paths.

## Bucket Selection And Copy Names

Bucket survivors by `(region, tag)`. Retain at most profile `group_cap` records
per bucket, ordered by higher `effective_priority`, later `effective_time`,
larger byte size, then lexical `record_id`. Dropped survivors are `cap_dropped`.

Copy accepted payloads to `/app/filtered/accepted/<region>/<tag>/<stem>__NN<ext>`
for the visible run, or the equivalent accepted tree below the requested output
directory. Lower-case and sanitize `region`, `tag`, and stem by replacing runs
outside `[a-z0-9._-]` with `_`, trimming `_`, and using `unnamed` if empty.
Extension is lower-case text after the final dot; no dot or only a leading dot
means no extension. `NN` is a two-digit counter per `(region, tag, sanitized
lower-case original basename)`, assigned in accepted order from `01`. For
example, the first accepted `Sun.Frame.JPG` copy uses `sun.frame__01.jpg`,
with two underscores before the counter.

## `/app/filtered/report.json`

Write compact sorted-key JSON followed by exactly one newline. Top-level keys are
`accepted`, `rejections`, and `summary`.

Accepted entries are ordered by `region`, `tag`, higher `effective_priority`,
later `effective_time`, then `record_id`. Each entry has `record_id`, `source`,
`output`, `region`, `tag`, `effective_time`, `effective_priority`, `renewal_id`,
`override_id`, `receipt_id`, `media_ops`, `media_chain_digest`, `media_digest`,
`bundle_id`, `bytes`, and `audit_token`.

`source` is the manifest `relpath` value verbatim. `output` is the copy
destination with the output directory prefix removed; for example, remove
`/app/filtered/` from a visible copied file path.

`audit_token` is the first 16 lowercase hex characters of sha256 over UTF-8 text
joining `record_id`, `source`, `output`, `effective_time`, decimal
`effective_priority`, decimal `bytes`, `receipt_id` or `-`, `bundle_id` or
`-`, `media_chain_digest`, and `media_digest` with `|`. `media_digest` is the
full lowercase sha256 of the copied payload bytes. `media_chain_digest` is the
full lowercase sha256 of applied `media_ops` ids in order, each followed by one
newline; with no media operations, hash the empty string.

`summary.accepted_audit_digest` is the full lowercase sha256 of ordered
`audit_token` values plus one newline after each token; with no accepted files,
hash the empty string.

`rejections` arrays are `malformed_manifest`, `superseded_manifest`,
`unsafe_path`, `missing_file`, `digest_mismatch`, `unknown_region`,
`extension_reject`, `size_reject`, `magic_reject`, `stale_without_renewal`, and
`cap_dropped`. `superseded_manifest`, `unsafe_path`, `missing_file`,
`digest_mismatch`, `unknown_region`, `extension_reject`, `size_reject`,
`magic_reject`, and `stale_without_renewal` store `seq` strings.
`malformed_manifest` stores `seq` strings too, except short malformed rows store
`line:<line_number>`. `cap_dropped` stores `record_id`.

`summary` has integer counters for every rejection key plus `manifest_rows`,
`selected_manifest`, `valid_renewals`, `invalid_renewals`, `valid_overrides`,
`invalid_overrides`, `overrides_applied`, `valid_receipts`, `invalid_receipts`,
`receipts_applied`, `receipt_bonus_total`, `valid_media_ops`,
`invalid_media_ops`, `media_ops_applied`, `media_priority_total`,
`media_bytes_delta`, `valid_bundles`, `invalid_bundles`, `bundles_applied`,
`bundle_bonus_total`, `accepted_files`, `copied_bytes`, and
`accepted_audit_digest`.

## Secondary Views

Write `/app/filtered/audit.tsv` as tab-separated LF rows with header `kind`,
`id`, `reason`, `path`, `fingerprint`. Accepted rows come first in accepted
order: `accepted`, `record_id`, `-`, `output`, `audit_token`. Rejected rows
follow rejection-key and array order: `rejected`, array value, reason key, `-`,
and the first 16 lowercase hex characters of sha256 over UTF-8 text joining
`rejected`, that id, that reason, and `-` with `|`.

Write `/app/filtered/decision_trace.ndjson` as compact sorted-key JSON lines with
LF after every line. Accepted events come first with increasing `sequence` from 0
and fields `kind = accepted`, `id = record_id`, `output`, and `audit_token`.
Continue the sequence for rejected events in `/app/filtered/audit.tsv` order;
each has `kind = rejected`, `id`, `reason`, and `fingerprint`.

Write `/app/filtered/bucket_rollup.tsv` as tab-separated LF rows with header
`region`, `tag`, `accepted_count`, `copied_bytes`, `max_effective_priority`,
`audit_digest`. Emit one row per accepted `(region, tag)` bucket, ordered
lexically by `region` then `tag`. Counts and bytes cover accepted entries in
that bucket; `max_effective_priority` is the bucket maximum. `audit_digest` is
the full lowercase sha256 of that bucket's accepted `audit_token` values in
report order plus one newline after each token.
