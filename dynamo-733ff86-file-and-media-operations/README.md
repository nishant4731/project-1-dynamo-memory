# Reel Recovery Dynamo Task

This repository contains a single Harbor task in `task/`. The task asks an agent to recover a damaged tiled grayscale video reel from fragment records, telemetry, revision metadata, and parity groups.

The environment ships only the visible input data under `/app/data`. The verifier keeps the expected reel digest and summary constants in `task/tests/expected_summary.json`, which is overlaid only at verification time. The reference solution reconstructs the video by validating CRCs, applying phase-based tile coordinate mapping, decoding fragment payloads, resolving revisions, repairing missing tiles with XOR parity, and writing `/app/recovered/reel.gray` plus `/app/recovered/reel_summary.json`.

Validation targets both artifacts: the verifier rejects missing or symlinked outputs, checks the full raw reel digest and selected pixel probes, and requires exact summary fields for scene cuts, brightness, discarded fragments, and parity-recovered tiles.
