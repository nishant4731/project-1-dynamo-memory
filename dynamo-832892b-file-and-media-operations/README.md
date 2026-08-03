# dynamo/mend-scan

Mend a monochrome scan reel from fragmented tile packets with orientation remapping, permanent veto ledger, XOR parity repair, and forensic audit reporting.

## Overview

The agent receives a synthetic broadcast-scan workspace under `/app/data/` containing a manifest, packet log, orientation telemetry, and revision ledger. It must reconstruct a 16×12, 14-frame Y4M monochrome video, emit exact audit and lineage JSON, and install a reusable `mend_scan.py` CLI that generalizes to fresh workspaces and consumes the packet log after writing outputs.

## Approach

The reference solution decodes four tile codecs (raw, rle, delta_prev, zigzag), maps sensor coordinates to display coordinates via per-frame orientation modes, applies permanent packet-id vetoes, selects winners by revision then packet_id, processes XOR parity chains in packet-id order, and reports stage-sampled counters at every pipeline branch.

## Environment

Ubuntu 24.04 with Python 3 and pinned pytest. Shipped data lives in `task/environment/data/` as JSONL manifests and packet records.

## Verification

The verifier checks exact Y4M bytes, audit/lineage JSON equality against protected expected values, evidence consumption of the shipped packet log, and runs the submitted tool on three independently generated held-out fixtures with mixed orientation modes and veto traps.

## CI Note

The current submission commit includes the QC feedback fixes for telemetry tie-breaking and verifier harness isolation; this root note is outside the agent image and exists only to redraw an infra-tainted pass@2 check.
