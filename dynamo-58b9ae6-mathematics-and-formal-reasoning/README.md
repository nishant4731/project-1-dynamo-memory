# Orbit Solver Dynamo Task

This repository contains a single Harbor task under `task/`.

The task asks the agent to create `/app/orbit_solver.py`, a Python program that solves JSON instances of an exact tree optimization problem. A plan chooses one option at every tree node, must hit a target residue modulo `modulus`, and minimizes base cost plus a weighted maximum root-to-leaf load.

The environment ships only Python, pytest, the CTRF pytest plugin, and public sample cases at `/app/data/public_cases.json`. The reference solution installs a reusable dynamic-programming solver as the requested artifact.

Verification runs the submitted solver on hidden instances, recomputes the metrics from the reported choices, and independently computes the optimum with a verifier-side dynamic program. The tests check the requested output file only and require exact integer agreement.
