# Repair Video Deltas

This Harbor task asks the agent to recover a grayscale video clip from a damaged packet export. The export contains binary packet records with absolute tiles, XOR-delta tiles, packet revisions, malformed records, overlapping regions, and deterministic source tie-breaks.

The agent must write `/app/recover_clip.py`, run it against `/app/export`, and produce binary PGM frames plus a JSON summary in `/app/recovered`. The verifier checks the shipped recovery exactly and then runs the submitted solver against additional generated exports to ensure the implementation is reusable rather than hardcoded.

The environment uses the approved Ubuntu 24.04 base image and bakes in `pytest` plus `pytest-json-ctrf`; verification performs no install-time setup.
