# Atlas Repair Task

This repository contains a Project Dynamo Harbor task in `task/`.

The task asks agents to implement `/app/repair_atlas.py`, a reusable Python CLI that repairs corrupted image-design atlas sessions. A session contains manifest metadata and fragment TSV streams for asset records, patches, relative anchors, and stateful taps. The tool must reconstruct an exact binary PPM atlas, emit an overlap trace plus strict JSON audit report, and remove the evidence directory after successful repair.

The verifier checks the visible repaired session against a protected pristine fixture, validates strict report types and symlink-free outputs, and runs the submitted CLI on generated hidden sessions with varied geometry, transforms, blends, tie-breaks, rejection paths, patches, anchors, taps, and overlap patterns.
