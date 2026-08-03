# AlbumSplice Session Repair

This Harbor task asks the agent to create `/app/salvage_session.py`, a reusable Python CLI for repairing crashed AlbumSplice audio session directories. The tool validates binary packet records, derives recorder clock offsets from anchor evidence, reconstructs parity-backed chunks, applies time-gated edits, cross-chunk taps, feedback folds, and ramp envelopes, writes exact mono PCM16 WAV stems, and emits a canonical JSON repair report.

The shipped fixture lives in `task/environment/data/session`. The verifier runs the submitted CLI against both the shipped session and deterministic protected sessions with different sample rates, track counts, chunk counts, source offsets, parity repairs, tombstones, transforms, edit timing, taps, folds, ramps, and rescue-window candidate rejects. Expected WAV and JSON outputs are computed in verifier code, and the submitted tool is run as an unprivileged user so it cannot inspect protected verifier files.
