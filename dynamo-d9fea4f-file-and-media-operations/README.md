# Sheet Restore

This Harbor task asks the agent to implement `/app/restore_sheet.py`, a reusable Python CLI that repairs crashed sticker-sheet workspaces into an exact RGBA `sheet.png` plus a structured `ledger.json`.

The task is in the File and Media Operations category, Image and design processing subcategory. The shipped workspace includes multi-probe calibration for per-layer offset inference, an uncalibrated visible stamp layer, unknown-layer orphans, out-of-order placement events, point-in-time supersession, superseded-event accounting, calibration evidence consumption, deletion, an invisible layer, transforms, masks, opacity, clipping, and cross-layer stacked pieces.

Verification stages reference outputs for the visible workspace and deterministic held-out workspaces, removes the reference generator before invoking the agent script in an isolated subprocess, and compares exact PNG pixels plus the parsed ledger while rejecting missing or symlinked outputs.
