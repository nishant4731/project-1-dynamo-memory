# Rollcall Reel Recovery

This Harbor task asks the agent to recover a small grayscale video reel from a custom packet stream. The agent-visible data contains tile packets, row parity packets, and a cut plan with point-in-time cutoffs. A correct solution must parse the packet format, ignore packets published after each cutoff, reject CRC-bad payloads, recover exactly one bad or missing tile per row with parity, zero-fill unrecoverable rows, and produce a deterministic PGM contact sheet with a JSON manifest.

The verifier checks the manifest schema, frame hashes, parity-repair accounting, PGM dimensions, contact-sheet layout, and exact media bytes. Ground truth hashes live only in `task/tests/`, which Harbor overlays at verification time.
