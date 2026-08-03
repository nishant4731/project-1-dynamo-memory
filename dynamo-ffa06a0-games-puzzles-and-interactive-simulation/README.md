# Lumen Circuit Replayer

This Harbor task asks the agent to recover and implement a deterministic pixel-art puzzle-board renderer from calibration scenes. The agent must render `/app/data/scene.json` to a binary PPM image, typed JSON report, and intervention forecast, and must also provide `/app/renderer.py` as a reusable CLI for unseen scenes.

The challenge is in the interaction between inferred profile tables and the renderer lifecycle: event ordering, actor movement, mirrors, digit portal-pair selection, prism energy changes, collisions, flare pulses, heat accumulation, what-if stamp forecasting, pixel blending, and exact report counters. The verifier checks the visible output and runs the submitted renderer on protected hidden scenes.

The environment is pure Python on the approved Ubuntu base image with pytest baked at build time. No solution or verifier truth is copied into the agent image.
