# Badge Recovery Dynamo Task

This Harbor task asks an agent to reconstruct a badge artwork from custom design inputs:
a canvas spec, point-in-time palette history, RLE stencil sprites, and a placement audit log.

The intended solution parses design packages, resolves each layer's effective audit row at the
cutoff, looks up ink colors at each placement timestamp, applies transforms and blend modes,
selects optional repair candidates with a global modulo objective, composites the sprites with
clipping, per-ink opacity, and integer alpha rounding, and writes:

- `/app/restored_badge.ppm`
- `/app/restoration_report.json`
- `/app/replay_design.py`

The verifier parses the submitted PPM semantically, hashes the raw RGB pixels, checks sample
pixels and report fields, rejects symlink or placeholder artifacts, and runs the submitted
renderer on a hidden design package. The task difficulty comes from stale audit/palette rows,
same-time revision semantics, repair optimization, transforms, blend modes, and generalized
replay rather than hidden formatting requirements.
