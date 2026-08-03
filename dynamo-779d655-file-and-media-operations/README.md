# Design Freeze Recovery

This Dynamo task asks the agent to recover a frozen layered design contact sheet from a messy export. The visible inputs are a freeze manifest, an unordered NDJSON layer event stream, plain-text Netpbm color/alpha tiles, and row-parity repair bundles for damaged media.

The intended solution reconstructs damaged bundle rows, rebuilds the point-in-time layer state, ignores future-published records and exact duplicate replays, applies deletes, renders transformed and clipped tiles with deterministic integer alpha compositing, packs the artboards into a contact sheet, and emits an audit report.

The verifier parses only the requested `/app/recovered/contact_sheet.ppm` and `/app/recovered/report.json` outputs. It checks exact row-major RGB hashes, repair hashes, event accounting, visible-layer order, per-artboard hashes, non-background counts, and top palette summaries.
