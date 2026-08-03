Recover the release master for the archived session in `/app/vault`.

The archive contains segment containers, parity sidecars, a shuffled edit ledger, and a format note at `/app/vault/FORMAT.txt`. Treat `/app/vault/FORMAT.txt` as normative for the segment container, parity, codec, mid/side channel, punch edit, and ledger cutoff rules. The preview WAV in the vault is only a rough engineer bounce and is not authoritative.

Produce exactly three files:

`/app/restored_master.wav`: a stereo PCM WAV assembled from the release-valid segment for each slot in ascending slot order, after applying every release-valid punch-family edit described by `/app/vault/FORMAT.txt`. It must use the sample rate, channel count, sample width, and frame count implied by the vault metadata.

`/app/restoration_report.json`: UTF-8 JSON with this exact top-level schema:

`wav_sha256`: lowercase SHA-256 hex digest of `/app/restored_master.wav`.

`sample_rate`: integer sample rate.

`channels`: integer channel count.

`frames`: integer total number of stereo frames in the restored master.

`slot_sequence`: an array in playback order. Each item must contain `slot`, `segment_id`, `take_id`, `source`, `codec`, and `channel_mode`. Use `source` value `direct` when the segment payload passed its manifest CRC as stored, and `parity_repaired` when the segment payload had to be reconstructed from a parity sidecar before decoding.

`repaired_segments`: sorted array of segment IDs whose stored payload was missing or failed its manifest CRC and was reconstructed from parity.

`applied_punch_ids`: array of release-valid punch-family event IDs in the order they were applied.

`ignored_event_ids`: sorted array of ledger event IDs ignored because they occurred after the release cutoff or because a `select` or punch-family event referenced a take revoked at or before the release cutoff.

`/app/recover_vault.py`: a reusable Python 3 program that accepts exactly three positional arguments: input vault directory, output WAV path, and output report JSON path. It must apply the same recovery rules to any vault with the format described by `/app/vault/FORMAT.txt`. The submitted `/app/restored_master.wav` and `/app/restoration_report.json` must be produced by this program from `/app/vault`.
