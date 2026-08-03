# Reel Recovery

This Harbor task asks the agent to implement `/app/recover_reels.py`, a reusable Python tool that reconstructs horizontal PPM review-reel strips from clip-frame files, edit decisions, and point-in-time approval logs.

The environment ships a deliberately simple visible `reel_lab` fixture under `/app/data`. The verifier also runs the tool on deterministic hidden fixtures generated at verify time that exercise interacting authority traps, then checks PPM strip digests and the full accounting summary.

The main challenge is applying the authority rules together under held-out cases: embedded frame metadata beats filenames and sidecars, binary PPM raster boundaries must not be over-skipped, approval and frame revisions are selected as of each cut time with disclosed tie-breaks, later cut rows supersede earlier rows, multi-digit slots sort numerically, corrupt frames are ignored, missing or revoked takes become black placeholders, and independent summary counters must be sampled at the correct decision points.
