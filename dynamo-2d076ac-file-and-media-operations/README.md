# Loop Recovery Dynamo Task

This Harbor task asks the agent to recover current loop masters from damaged RIFF/WAVE files. The agent must write a reusable Python CLI, parse RIFF chunks through EOF, select one complete release bundle as of a fixed cutoff, apply timestamped sample repairs, and emit both a deterministic manifest and clean WAV files.

The task lives entirely in `task/`. The environment bakes in Python and pytest dependencies, copies only the agent-visible WAV session data into `/app/data`, and keeps verifier fixtures hidden until grading.

Verification checks the shipped outputs and runs the submitted `/app/recover_session.py` on unseen RIFF fixture sets with split data chunks, odd padding, late-published and future-effective decoys, incomplete or unrepaired newer bundles, void takes, revision ties, overlapping repairs, non-default plan parameters, and a bundle-id tie-break.
