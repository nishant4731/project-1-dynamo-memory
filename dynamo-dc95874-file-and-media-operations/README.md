# Poster Ledger Recovery

This Harbor task asks an agent to recover a 128 by 96 RGBA campaign poster from a visible studio asset packet. The packet contains a point-in-time canvas record, an asset event ledger, a registration-mark ledger, PNG layer assets, masks, and a stale preview manifest that is intentionally not authoritative.

The intended solution selects the approved press-channel asset for each layer slot as of the approval cutoff, accounting for revocations and tie-breaks, then renders the selected layers with crop, transform, mask, opacity, backdrop-dependent underprint halftone processing, and straight-alpha source-over, multiply, and screen blending. It then derives registration-mark residues from the rendered canvas, solves the fixed-size modular subset constraint before compositing the selected mark rectangles, and applies a stateful serpentine press-compensation pass driven by the selected mark IDs.

Verification checks both requested outputs: `/app/recovered/final.png` and `/app/recovered/provenance.json`. The tests validate the provenance schema, selected asset IDs, and selected registration marks, recompute the final raw RGBA pixel hash, probe decisive pixels that cover the image-processing rules, and verify that the provenance hashes match the submitted files.
