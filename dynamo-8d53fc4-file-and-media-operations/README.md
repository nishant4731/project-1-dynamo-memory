# Cue Slate Recovery

This Dynamo task asks the agent to implement `/app/recover_cues.py`, a reusable Python tool that reconstructs cue metadata from damaged audio-session bundles.

The session data combines mono PCM WAV files with embedded bit slates, event-ledger corrections, revocations, device clock calibration anchors, trims, muted takes, and exact payload hashes. The shipped fixture lives under `/app/sessions/shoreline`; the verifier also builds hidden sessions that exercise the same public contract.

Verification runs the submitted script against the visible and hidden sessions, rejects missing or symlinked artifacts, and compares the produced JSON to an independent reference implementation.
