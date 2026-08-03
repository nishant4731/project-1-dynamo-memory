# Prism Relay Dynamo Task

This repository contains a Harbor task for the Games, Puzzles, and Interactive Simulation category.

Agents must implement a reusable calibrated relay simulator, solve the visible Prism Relay scene pack, and produce both `/app/results.json` and executable `/app/prism_relay.py`. The verifier checks exact visible rendering and then runs the submitted simulator on protected generated scenes.

The challenge is built around interacting simulation requirements: calibration-table lookup, delayed split beams, saturating state merges, pre-render dampers, post-render collectors, exact frame rendering, objective optimization, and deterministic tie-breaks.
