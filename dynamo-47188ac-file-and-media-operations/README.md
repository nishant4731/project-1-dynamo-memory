# Camera Drop Repair

This Harbor task asks the agent to implement `/app/recover_camera.py`, a reusable Python repair program for crashed tiled grayscale video drops.

The shipped fixture contains a small synthetic capture drop with camera-local epoch anchors, tiled frame fragments, mixed raw/xor/RLE packing, stale previews, invalid payload hashes and decoded-frame CRCs, an unsynced epoch, out-of-range candidates, per-fragment luma correction, and a missing tile. The submitted program must turn any matching drop into an exact grayscale YUV4MPEG2 stream plus a repair report.

Verification runs the submitted program on the visible drop and on fresh held-out drops generated at verification time, then compares the produced Y4M bytes and JSON counters against an independent reference implementation of the documented rules.
