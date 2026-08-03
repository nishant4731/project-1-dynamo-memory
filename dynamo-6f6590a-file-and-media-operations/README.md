# Atlas Rebuild Task

This repository contains a Harbor-format Project Dynamo task in `task/`.

The task asks the agent to implement `/app/rebuild_atlas.py`, a reusable Python CLI that rebuilds an RGBA design atlas from a workspace containing a layout file, a manifest event log, and PNG fragments. Correct reconstruction requires multi-format PNG decode (including interlaced and non-RGBA sources), decoded-pixel SHA-256 validation, cutoff filtering, deterministic event ordering, transforms, transparent gutters, evidence consumption of fragments, and an exact multi-stage JSON report.

The verifier runs the submitted CLI against a pristine copy of the shipped `/app/studio_case` workspace and against held-out workspaces generated at verify time. It compares decoded RGBA atlas bytes and exact report semantics, requires fragments/ to be emptied, and rejects missing or symlinked outputs.
