# Restore Reel — Video Processing Task

Restore a crashed monochrome broadcast reel from fragmented tile packets stored in JSONL logs. The agent must decode four tile codecs (raw, RLE, delta-from-previous-frame, zigzag), map sensor coordinates through per-frame orientation modes (forward, mirror_x, mirror_y), honor a permanent fragment veto registry, reconstruct missing tiles via XOR parity chains, emit an exact YUV4MPEG2 reel plus audit and provenance reports, and ship a reusable `restore_reel.py` CLI that consumes the fragment log after writing outputs.

## Approach

Synthetic packetized monochrome video (16×12, 14 frames, 4×4 tiles) with FEC-style parity, revision contests, recalled rows, checksum traps, orientation schedule ties, and veto ledger traps. Difficulty comes from compound exact-integer accounting (20+ independent counters), byte-exact Y4M output, sensor-to-display remapping under three orientation modes, and evidence consumption (first draft run destroys graded state).

## Environment

Ubuntu 24.04 with Python 3. Shipped inputs: `manifest.json`, `fragment_log.jsonl`, `orientation_schedule.jsonl`, `recall_registry.jsonl` under `/app/data`.

## Verification

Oracle/nop via Harbor. Verifier checks exact Y4M bytes, audit/provenance JSON equality, fragment log consumption, and differential grading of `restore_reel.py` on held-out generated fixtures with mixed orientations, vetoes, and non-default geometry/fps.
