# dynamo/recover-field

Recover a progressive monochrome surveillance reel from an interlaced field spool.

## Overview

The agent receives a synthetic field-capture workspace: separate top and bottom half-height luma fields stored as packetized records with multiple codecs, weave modes, horizontal phase remapping, permanent custody vetoes, and XOR parity repair. The job is to deinterlace into a 16×12, 10-frame Y4M reel, emit exact forensic audit counters and field-level provenance, ship a reusable `recover.py` CLI, and consume the field spool evidence after writing outputs.

## Approach

1. Load weave and phase maps plus the permanent veto ledger.
2. Decode active field records; drop checksum failures and vetoed packet IDs.
3. Select winners by `(frame, field_type)` using highest revision, then lexicographically smallest `packet_id`.
4. Process parity records in packet-id order on raw pre-phase bytes; XOR-reconstruct missing halves.
5. Apply the frame phase mode, weave top/bottom into progressive frames.
6. Write Y4M, audit.json, lineage.json; install recover.py; delete field_spool.jsonl.

## Environment

Ubuntu 24.04 with Python 3 and pytest (verifier deps baked at build time). Shipped data lives in `/app/data/`; outputs go to `/app/recovered/`.

## Verification

The verifier checks exact Y4M bytes and exact audit/lineage JSON against protected expected values, asserts the shipped field spool was consumed, then runs the submitted `recover.py` on generated fixtures with mixed weave modes (blend, bob_top, bob_bottom), phase remapping (mirror_h), vetoes, delta_prev, and parity repair — comparing all outputs to an independent reference.
