Write Python 3 CLI `/app/salvage_session.py`. Verifier:
`python3 /app/salvage_session.py /app/data/session`. Argument: session root.
Write `/app/data/session/restored/report.json` and
`/app/data/session/restored/<track>.wav`; generated roots use their own
`restored/`.

Inputs: `manifest.json` (`case_id`, `sample_rate`, `chunk_frames`,
`track_chunks`, `sources`; ignore hints), `registry.tsv`
(`path`, `packet_id`, `sha256`), packets, and `evidence/*.tsv`. Packet bytes:
`ASPKT1\n`, compact JSON header line, newline, payload.

Intake:
- Unreadable path or file SHA mismatch: increment `rejected_file_hash`, discard.
- Other invalid packet adds `rejected_payload_hash`: bad magic/header/JSON,
  id mismatch, unknown `kind`, bad length/digest, nonempty tombstone.
- Valid `data`: `len(payload) == frames * 2` and payload SHA matches. Valid
  `tombstone`: empty payload and empty-payload SHA. Valid `parity`: payload length
  is `frames * 2` before repair.

Recovery:
- Source offset uses accepted `data` named in `anchors.tsv`: most common
  `observed_tick - local_tick`, smallest on ties. Sources without accepted anchors
  have no offset: omit from `source_offsets` and ignore their packets.
- Candidate tick is `local_tick + source_offset`. Known-offset `data` and
  `tombstone` packets are direct candidates.
- Repair `parity` only when every `basis_packet_ids` entry names accepted `data`.
  Missing, rejected, tombstone, or parity basis ids are unrecoverable: add
  `rejected_payload_hash`, queue no candidate. Otherwise XOR parity with basis
  payloads; matching `repair_payload_sha256` becomes repaired data, else add
  `rejected_payload_hash`.
- `windows.tsv`: `track`, `seq`, `start_tick`, `end_tick`. If any window exists for
  a chunk, keep only inclusive-window candidates; each discard adds `window_rejects`.
- Select per `(track, seq)` by max `(global_tick, revision, packet_id)`. Selected
  tick means that `global_tick`. No candidate means silence fill.

Render tracks sorted by name, seq increasing. Samples are signed 16-bit LE.
Division truncates toward zero; clip each intermediate to `[-32768,32767]`. `%`:
Python/Euclidean modulo: positive modulus yields `0..modulus-1`, even for negatives.

- Base: for non-tombstones decode payload, apply `reverse` first when present, and
  let `invert` set initial polarity.
- Sidecar rows below are eligible only when track/seq match and
  `effective_tick <= selected tick`; sort by `(effective_tick, row order)`.
- `edits.tsv`: `track`, `seq`, `effective_tick`, `op`, `value`. `gain_delta`
  changes `gain_milli`; nonzero `invert` flips polarity. Count eligible
  rows, including tombstones, then apply polarity and `trunc(sample * gain_milli / 1000)`.
- `taps.tsv`: `track`, `seq`, `effective_tick`, `source_track`, `source_seq`,
  `phase`, `stride`, `gain_milli`. After edits, non-tombstone only. Count rows whose
  source already rendered. Add
  `trunc(source[(i * stride + phase) % chunk_frames] * gain_milli / 1000)`; clip.
- `folds.tsv`: `track`, `seq`, `effective_tick`, `lag`, `gain_milli`, `rounds`.
  After taps, non-tombstone only. Count each row once; each round scans left-to-right
  from `lag`, adding `trunc(current[i - lag] * gain_milli / 1000)`; clip.
- `ramps.tsv`: `track`, `seq`, `effective_tick`, `start_gain_milli`, `end_gain_milli`.
  After folds, non-tombstone only. Gain at `i` is
  `start + trunc((end - start) * i / max(1, chunk_frames - 1))`; apply, divide by
  1000, clip. Count each row.
- `stitches.tsv`: `track`, `seq`, `effective_tick`, `source_track`, `source_seq`,
  `shift_mod`, `gain_milli`, `invert_on_odd`. After ramps, non-tombstone only. Count
  only if source rendered earlier with non-null tick. With Euclidean `%`, compute
  `shift = (target_tick - source_tick) % max(1, shift_mod)`. Add
  `trunc(source[(i + shift) % chunk_frames] * gain_milli / 1000)`; negate when
  `invert_on_odd` and `target_tick + source_tick` is odd. Clip.
- Tombstones render silence and count tombstones. Missing candidates render silence
  and alone add `silence_fills`.

Outputs:
- WAV: RIFF/WAVE PCM, mono, width 2, no metadata chunks, manifest sample rate,
  exactly `chunk_frames * track_chunks[track]` frames.
- `report.json`: sorted-key compact UTF-8 JSON plus trailing newline. Keys:
  `case_id`, `sample_rate`, `chunk_frames`, `source_offsets`, `totals`, `tracks`.
- `source_offsets`: only source names with known offsets.
- `totals`: positive counters only: `valid_records`, `rejected_file_hash`,
  `rejected_payload_hash`, `window_rejects`, `parity_repairs`, `silence_fills`,
  `tombstones`, `edits_applied`, `taps_applied`, `folds_applied`, `ramps_applied`,
  `stitches_applied`. `valid_records` counts every intake-valid packet, including
  parity later failed/unselected. `parity_repairs` counts only repaired
  parity chunks that become final selected candidates.
- `tracks` is an object keyed by track. Each value has `frames`, `pcm_sha256`,
  `peak_abs`, `repaired_chunks`, `silence_chunks`, `selected`, `edits_applied`,
  `taps_applied`, `folds_applied`, `ramps_applied`, `stitches_applied`, `tombstones`.
  `pcm_sha256` hashes raw PCM; `peak_abs` is max absolute sample; `repaired_chunks`
  is repaired seqs; `silence_chunks` includes tombstone and missing-candidate seqs.
- `selected`: one object per seq with `seq`, `packet_id`, `source`, `global_tick`;
  missing-candidate silence uses JSON null for the last three fields.
