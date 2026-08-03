# Reel Recovery Dynamo Task

This repository contains a Harbor task for recovering a canonical video master from a packetized frame archive.

The task asks the agent to parse `/app/archive/session.json` and `/app/archive/packets.jsonl`, reject corrupt or stale frame packets, apply pre-freeze supersession rules, reconstruct missing frames from XOR parity blobs, and render the recovered frame sequence as `/app/recovered_master.ppm` with a provenance report at `/app/recovery_report.json`.

The environment uses the approved pinned Ubuntu base image, bakes in Python and pytest for verification, and copies only the agent-visible archive data into `/app/archive`. The verifier is kept under `task/tests/`; it checks artifact safety, report schema, selected packet provenance, sprite dimensions, frame ordering, per-frame RGB hashes, and the submitted sprite digests.
