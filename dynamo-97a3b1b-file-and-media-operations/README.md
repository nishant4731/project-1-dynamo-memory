# Session Mix Rebuild

This Harbor task asks the agent to implement `/app/rebuild_mix.py`, a reusable Python program that reconstructs mono 16-bit PCM session mixes from DAW-style cue packets.

The visible fixture lives in `task/environment/data/session-visible`. It contains event logs, asset mappings, clip files, stale decoy paths, and optional sidecar TSVs for gains, envelopes, offsets, and mix modes. The task is designed around exact integer audio compositing, event-state recovery, source resolution from authoritative metadata, and in-place repair semantics that empty `clips/` after restoration.

Verification is fully programmatic. The tests check that the submitted tool is executable, accepts exactly one session argument, has already restored `/app/data/session-visible`, and then rebuilds a copied visible session plus generated hidden sessions. Each run is compared byte-for-byte against an independent reference WAV and exact manifest counters, including hidden witnesses for tie-breaks, delete wins, DPCM decoding, under/over paint order, transformed offsets, envelopes, and clipping/rounding behavior.
