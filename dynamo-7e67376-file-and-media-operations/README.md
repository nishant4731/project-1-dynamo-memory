# AFR Master Recovery

This Harbor task asks the agent to rebuild a mono WAV master from a synthetic failed AFR audio transfer. The agent receives a ledger, a compact custom audio block format description, and chunk files with revision, checksum, polarity, chained-codec, and parity-recovery traps.

The task is designed around media-forensics style recovery work: choose authoritative transfer rows, reject corrupted decoded audio by canonical hash, ignore retracted or orphaned material, recover a two-slot erasure with XOR plus GF(256) parity, decode later chained QAD4 blocks from the restored predecessor state, and emit both the restored WAV and a structured recovery report.

Verification is deterministic and byte-level. The tests validate the WAV container parameters, the exact raw PCM digest, the report schema, the selected source list, and the parity-recovered blocks, while rejecting missing or symlinked outputs.
