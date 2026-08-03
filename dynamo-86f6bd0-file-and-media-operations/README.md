# Archive Master Recovery

This Dynamo task asks an agent to recover a byte-exact stereo release master from a damaged audio vault. The visible data in `task/environment/data/` contains custom segment containers, parity sidecars, a shuffled edit ledger with punch-in edits, and a stale preview bounce.

The task tests audio/media file recovery, binary container parsing, CRC validation, XOR parity repair (including dual-missing cross-group chains), multi-hop delta decoding, mid/side stereo conversion, channel-selective punch replacement, blend floor-division edits, cutoff-based edit-ledger interpretation, and reusable script implementation. The expected outputs are `/app/restored_master.wav`, `/app/restoration_report.json`, and `/app/recover_vault.py`.

The reference solution lives in `task/solution/` and derives the output from the vault data. The verifier in `task/tests/` checks the requested artifacts, rejects symlink shortcuts, validates the WAV metadata and digest, checks the report's release and punch-edit decisions, and re-runs the reusable program on four protected vaults generated at verify time.
