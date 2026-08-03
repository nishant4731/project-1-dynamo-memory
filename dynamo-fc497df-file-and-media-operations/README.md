# Recover Design Task

This Harbor task asks the agent to implement `/app/recover_design.py`, a reusable Python tool that reconstructs a layered design contact sheet from a design-pack directory.

The pack combines palette revisions, cell event overrides, custom run-length fragment files, optional masks, geometric transforms, tone modes, alpha blending, clipping, and exact manifest accounting. Verification runs the submitted tool on both the visible `/app/design_pack` fixture and held-out packs, then compares byte-exact PPM output and strict JSON manifest fields against an independent reference.
