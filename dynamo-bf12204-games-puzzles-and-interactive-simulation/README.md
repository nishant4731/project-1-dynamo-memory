# Beam Heatmap Dynamo Task

This repository contains a Harbor task in `task/` for the Games, Puzzles, and Interactive Simulation category.

The agent receives a laser-puzzle scene in `/app/data/scene.json`, optimizes the disclosed lens-placement candidates, and must produce five artifacts:

- `/app/render/placements.json`
- `/app/render/beam_report.json`
- `/app/render/temporal_report.json`
- `/app/render/final.ppm`
- `/app/render/solver.py`

The challenge is combining a combinatorial placement search with a deterministic beam simulation: simultaneous batching, RGB channel merging, portals, splitters, prisms, time-dependent mirrors, phase gates, heat-history filters, tick-load-dependent turns, delay queues, cycle cutoffs, modulo-checksum scoring, temporal peak bonuses, temporal accounting, and exact P3 heatmap rasterization. The verifier checks the requested outputs by parsing the placement report, simulation reports, and image, then comparing the optimal score, beam accounting, rendered pixel digest, dimensions, and representative cell colors. It also imports the submitted `solver.py` and runs the same solver entry point against hidden scenes covering portal timing, placed digit portals, ordered memory updates, final-tick delayed releases, prism batching, checksum-residue wrap, peak-aware optimization, exit accounting, zero-color portal stops, phase/filter/color-rotation/tick-load tiles, saturated rendering, inert filler tie-breaks, digit-pair filler compression, and wide-component optimizer state compression to reject visible-instance hardcoding, local-only component scoring, stale portal topology, greedy caps, and global product shortcuts.
