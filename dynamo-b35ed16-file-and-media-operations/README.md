# Recover Video Reel

This Harbor task asks the agent to recover a raw RGB24 delivery master from an archive reel and a fragment catalog. The visible inputs are synthetic but model realistic video handoff defects: out-of-order catalog rows, post-cutoff revision decoys, bad full-frame transfers, duplicate fragments, XOR parity repair for missing frame halves, and whole-frame delta revisions.

The oracle in `task/solution/solve.py` derives the answer from the shipped data. The verifier hash-pins the agent-visible inputs, checks the recovered master by exact stream and per-frame digests, and validates the JSON report against the catalog selection and delta-provenance rules.
