# Calibrate Cairns

This Harbor task asks the agent to implement a reusable solver for a compact board-and-card simulation. The agent receives calibration replays and puzzle queries in `/app/data`, must infer the hidden simulation profile, then optimize every fixed-order hand placement.

The reference solution writes two artifacts:

- `/app/answer.json`, the solved visible puzzle bundle.
- `/app/profile.json`, the inferred profile constants plus a calibration replay residual audit.
- `/app/solver.py`, a reusable CLI that accepts `INPUT_DIR OUTPUT_JSON` and solves other bundles with the same schema.

Verification hash-pins the shipped visible data, checks the visible answer/profile JSON with strict type-aware equality, and runs the submitted solver on protected hidden profile variants with different constants and board topologies. Calibration includes same-row and same-column glyph pulse probes, non-dot terrain pulse probes, and two rank orderings for each adjacent pair so drift residues, pulse coefficients, and the `min(previous_rank,current_rank)` link multiplier are pinned by visible score evidence as well as charge transitions. Hidden expectations are snapshotted before the submitted solver runs, and hidden inputs are hash-checked afterward to reject mutation. The environment uses the shared Harbor image model with pytest baked into `task/environment/Dockerfile`.
