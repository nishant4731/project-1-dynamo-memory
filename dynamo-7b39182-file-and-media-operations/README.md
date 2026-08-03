# Reel Repair Dynamo Task

This repository contains a Harbor task for the Project Dynamo Video Processing subcategory. The task asks an agent to implement `/app/repair_reels.py`, a reusable repair tool for corrupted video reel workspaces.

The tool validates event digests, rewrites scene aliases, derives source-frame corrections from verified clip anchors, applies take-rate packing with splice pads, lane-scoped edit accounting, same-clip overlap eviction, lane duration budgets, and writes both a repaired timeline CSV and an accounting report.

The verifier runs the submitted program on deterministic protected workspaces and compares the outputs against an independent reference calculation. The visible sample at `/app/data/reel_lab` is included only for inspection during the agent run.
