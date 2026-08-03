# Feature Lens

This Harbor task asks an agent to implement a reusable sparse-feature triage CLI for an interpretability audit bundle. The visible bundle provides calibration records and labels from one synthetic-but-realistic model inspection run; the verifier checks that the submitted tool infers the bundle-specific integer rulebook and applies it to candidate features.

The task lives under `task/`. The verifier validates the visible outputs, then runs the submitted `/app/audit_rulebook.py` on hidden bundles with different global weights, profile thresholds, source bonuses, method/profile offsets, duplicates, and invalid rows.

The environment is Python-only on the approved Ubuntu base image with pinned pytest dependencies. Ground truth and hidden fixture generation remain in the verifier overlay, not in the agent image.
