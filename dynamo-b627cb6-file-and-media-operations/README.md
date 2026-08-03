# Dynamo Reel Recovery

This Harbor task asks the agent to recover a canonical RGB video timeline from a custom binary reel and a publication ledger with cutoff-time corrections.

The agent-visible inputs live in `task/environment/data/`. The reference solution parses the reel, validates CRCs, decodes raw/RLE/XOR-RLE frame records, applies manifest supersession semantics, and writes `/app/recovered/timeline.json` plus `/app/recovered/contact_sheet.ppm`.

Verification is handled by `task/tests/test_outputs.py`, which rejects missing, empty, or symlinked outputs and checks exact timeline evidence, scene cuts, and the binary PPM contact sheet digest.
