# Session Reel Repair

This Harbor task asks the agent to implement `/app/restore_session.py`, a reusable Python CLI for rebuilding a canonical mono WAV reel from ledgered audio chunks.

The shipped session contains WAV shards plus tab-separated ledger and calibration files with stale revisions, a revoked chunk, one digest-corrupt chunk, a duplicate slot, trim guards, polarity and scale transforms, per-session bias drift, adjacent-slot boundary repair, and silence gaps. Hidden stress sessions also include raw patch and slot-adjustment sidecars. The correct solver must select current ledger, calibration, patch, and adjustment rows, normalize and validate chunk audio, derive and apply a seven-lane bias vector, repair adjacent used-slot boundaries, resolve duplicate slots, synthesize gaps, write a restored 8000 Hz PCM WAV, and emit an exact JSON accounting report.

Verification runs the submitted CLI on the visible session and on three deterministic hidden sessions generated at verify time. The verifier computes expected WAV samples and report values independently, checks report schema exactly, and rejects symlinked outputs.
