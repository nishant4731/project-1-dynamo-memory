# Audio Ledger Restore

This Harbor task asks the agent to implement `/app/restore_masters.py`, a reusable Python tool that reconstructs mono 16-bit WAV masters from a damaged audio packet session and then deletes the session packet evidence.

The shipped session contains registry, trim, ledger, and packet files. Correct restoration requires point-in-time ledger evaluation with same-tick sequence ordering, equal-revision path selection, packet checksum validation, codec decoding, checksum-anchored repair masks chosen among competing anchors, one highest-revision chained XOR parity recovery pass at a time, cutoff-valid trim selection, deterministic WAV writing, an exact trailing-newline JSON manifest with audit counters, and deletion of `packets/` after success.

Verification regenerates the shipped seed plus hidden sessions, runs the submitted tool on pristine copies, rejects missing or symlinked deliverables, requires packet evidence removal, and compares every recovered media artifact exactly.
