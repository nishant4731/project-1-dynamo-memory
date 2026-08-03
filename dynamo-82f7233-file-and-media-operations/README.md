# dynamo/repair-reel — Repair Reel

Repair a monochrome Y4M surveillance reel from fragmented tile packets with three-axis telemetry remapping (`forward`, `mirror_x`, `mirror_y`), four tile codecs (`raw`, `rle`, `delta_prev`, `invert`), FEC-style parity repair, permanent packet-id vetoes, and evidence consumption.

## Overview

The agent receives a synthetic packetized video workspace under `/app/data/` and must produce four outputs under `/app/repaired/`: a byte-exact Y4M reel, forensic audit JSON, packet-provenance lineage JSON, and a reusable `repair_reel.py` CLI that deletes the consumed packet log after writing outputs.

## Approach

Reconstruction combines sensor-to-display coordinate remapping per frame, checksum-validated tile decoding, revision-based selection with permanent vetoes, ascending-order parity repair with chained same-frame fills, and exact-integer audit counters sampled at each pipeline branch.

## Environment

Ubuntu 24.04 with Python 3 and pytest. Shipped fixture: 16×12 monochrome reel, 14 frames, ~180 tile/parity records with mixed telemetry modes, codec types, revision contests, and parity chains.

## Verification

The verifier checks exact shipped Y4M bytes and audit/lineage JSON equality, confirms packet-log consumption, and runs the submitted tool on deterministic generated held-out fixtures with varied dimensions/frame counts and independent reference recomputation.
