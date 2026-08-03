# OrbitCam Recovery Dynamo Task

This repository contains a Harbor task for the File and Media Operations / Video Processing category.

The task asks an agent to recover canonical grayscale video frames from an unordered OrbitCam archive. The archive includes stale records, future corrections, voided candidates, point-in-time tie-breaking, underdetermined finite-field repairs with a global residue and motion objective, final calibration/stabilizer/echo ledgers, and four frame encodings: raw bytes, RLE, modulo deltas, and mirrored XOR payloads.

The agent must produce:

- `/app/output/recovered_timeline.json`
- `/app/output/contact_sheet.pgm`

The verifier checks that both outputs are regular files, hash-pins the archive inputs, independently recomputes the canonical recovered timeline from the archive, validates every recovered frame field and aggregate digest, and verifies the binary PGM contact sheet by header, dimensions, and pixel hash.

The environment uses the approved Ubuntu 24.04 base image and bakes Python, pytest, and pytest-json-ctrf at build time. The agent-visible archive lives under `task/environment/data/archive`; verifier tests live under `task/tests`.
