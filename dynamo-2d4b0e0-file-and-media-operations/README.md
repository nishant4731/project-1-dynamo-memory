# Locked Reel Recovery

This Harbor task asks the agent to recover a locked raw RGB24 inspection reel from a packetized video dump in `/app/data`.

The task combines media packet repair, point-in-time edit decisions, CRC validation, storage-to-display frame transforms, delta-coded frame reconstruction, and exact audit accounting. The submitted artifact must include the recovered reel, a manifest, a packet audit, and a reusable Python recovery program that the verifier runs against a protected variant fixture.

All task implementation lives under `task/`.
