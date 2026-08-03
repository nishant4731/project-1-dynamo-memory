# Layered Preview Recovery

This Harbor task asks an agent to recover a flattened RGBA preview from a damaged design packet. The packet provides a sprite atlas and a JSON layer stack with crops, flips, quarter-turn rotations, optional masks, opacity, clipping, and `normal`/`multiply`/`screen` blend modes.

The reference solution parses the packet, applies the transforms in the documented order, composites every pixel with the specified integer straight-alpha formulas, writes `/app/recovered/final.png`, and derives `/app/recovered/report.json` from the final pixel buffer.

Verification loads the submitted artifacts, rejects missing files or symlinks, compares the final PNG semantically pixel-for-pixel against the hidden expected render, and checks the audit report schema and values exactly.
