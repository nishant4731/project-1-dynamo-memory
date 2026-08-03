# Recover Badge Atlas

This Harbor task asks the agent to recover a release-ready badge atlas from an archived design package. The visible package contains temporal palette records, temporal placement records, digit-alpha masks, and release metadata. The agent must render the frames in release order and produce a reusable renderer, a P3 image atlas, and a JSON audit report.

The main challenge is choosing the authoritative design state for each release and implementing the full package format rather than tuning to one export: records must be both effective by the design time and published by the export time, selectors can include or exclude frames, symbol rows may be plain or run-length encoded, candidate layers may require exact modular subset selection, revoked placements disable entities, late corrections cannot be applied retroactively, and all transformed masks must be alpha-composited with the documented integer renderer.

The environment uses the pinned Ubuntu base image with Python and pytest dependencies baked in. Verification independently re-renders the expected frames from `/app/design_bundle`, compares the requested `/app/recovered/atlas.ppm` pixels exactly, checks the report schema, checksums, non-background counts, and inclusive bounding boxes, and runs the submitted `/app/recovered/render_bundle.py` on verifier-only bundles that exercise disclosed edge cases.
