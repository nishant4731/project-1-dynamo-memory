# Recover Design Proof

This Harbor task asks the agent to recover a final package-design contact sheet from a synthetic export packet. The visible packet contains a layout, an authority ranking, a bitemporal revision ledger, proof-variant candidates, a modular proof contract, and PNG tile assets with both straight and premultiplied-alpha encodings.

The reference solution selects the correct ledger row for each tile as of the release cutoff, repairs premultiplied RGBA assets, computes candidate proof residues, solves the global row/column/sheet variant contract, applies the declared transforms, composites the contact sheet, and writes both a structured manifest and reusable solver that audit the chosen records and rendered pixels.

Verification pins the visible input bundle by hash, rejects missing or symlinked outputs, independently solves the proof contract from the task data, compares raw RGBA hashes for image content, checks the manifest schema and values against the instruction, and runs the submitted solver on an additional same-schema packet.
