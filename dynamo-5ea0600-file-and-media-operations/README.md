# dynamo/recover-bounce

Recover a stereo mixdown from crashed DAW stem bounces with ledger supersession, latency offsets, bus routing, rendered-mix tap feedback, rotation authentication, equal-power panning, overlap headroom ducking, and evidence consumption.

## Overview

The agent builds `/app/recover_bounce.py`, a reusable CLI that reads a session directory (`manifest.json`, `ledger.tsv`, `latency.tsv`, `bus.tsv`, `tap.tsv`, `stems/*.wav`) and writes a stereo master WAV plus a forensic mix report. After success it deletes `stems/` so evidence cannot be replayed.

## Approach

The shipped session at `/app/session` exercises mono stem validation, current-row selection, an `active_span` set by a later-quarantined row, bar-aligned placement, bus route offsets, polarity flips, pan clamps, fades, pan weights via `isqrt`, rendered-state tap feedback, visible overlap ducking with `headroom_permille < 1000`, duplicate placement rejection, and exact JSON accounting. Hidden verifier fixtures add more overlap geometries, corrupt digests, revoked rows, bad-format/rate/trim/gain/length rejection paths, bus stale/HOLD traps, tap stale/BYPASS traps, same-start feedback ordering, and runtime-generated generalization probes.

## Environment

Python 3.13 slim image with pytest baked in. Session data lives under `task/environment/data/session/`.

## Verification

Harbor runs `task/tests/test_outputs.py` against the agent's `/app/recover_bounce.py` and `/app/session` outputs, then re-invokes the tool on independently generated hidden sessions compared to an inline reference implementation.
