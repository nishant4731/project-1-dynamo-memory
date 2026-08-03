# Embermaze Simulator

This Harbor task asks the agent to infer a compact grid-world simulation engine from calibration traces, implement a reusable `/app/solver.py`, and produce the visible `/app/answer.json`.

The verifier checks the visible scenario and also runs the submitted solver on protected generated scenarios with different calibrated constants, which makes answer hardcoding and visible-constant hardcoding fail.
