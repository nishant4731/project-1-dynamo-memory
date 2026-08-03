# Design Atlas Recovery

This Harbor task asks the agent to recover a crashed design export into a reusable CLI, an exact SVG atlas, and an audit report.

The visible bundle in `/app/design_drop` contains board revisions, unsorted layer events, point-in-time color-token history, and hashed SVG path fragments. A correct solution must implement `/app/recover_design.py`, run it for the visible bundle, and preserve the documented byte-level SVG and JSON formats.

Verification checks both the visible requested outputs and hidden design-drop fixtures. The tests independently replay the versioning rules, reject missing or symlinked artifacts, and compare the generated `atlas.svg` and `report.json` bytes exactly.
