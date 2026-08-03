# Inspect Atlas

This Harbor task asks the agent to build a reusable Python CLI for sparse-feature interpretability inspection. The tool must recover the active probe profile, infer pack-specific integer attribution coefficients from calibration traces, apply feature/profile metadata normalization, handle checksum/correction-row anomalies, and produce exact target plus counterfactual intervention reports for both the shipped pack and hidden verifier packs.

Verification compares exact JSON/CSV artifacts and runs the submitted CLI on protected generated packs with different dimensions, probe profiles, coefficients, and anomaly placement.
