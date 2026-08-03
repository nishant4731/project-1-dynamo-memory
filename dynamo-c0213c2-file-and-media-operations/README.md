# Atlas Repair Dynamo Task

This repository contains a Harbor-format Project Dynamo task in `task/`.

The task asks an agent to implement `/app/atlas_repair.py`, a reusable Python CLI that repairs a crashed sprite-atlas session. The shipped session contains Netpbm image and mask packets, anchor evidence for device-coordinate correction, and tap rows that read and rewrite the current partially recovered atlas before later packets render.

Verification checks the visible `/app/session` outputs and then runs the submitted CLI on protected generated sessions. The verifier compares exact canonical PPM bytes, strict JSON report structure and types, evidence consumption, packet rejection behavior, anchor-offset selection, transforms, alpha blending, clipping, and stateful tap accounting.

The environment uses the approved pinned Python base image and bakes the pytest verifier dependencies at build time. Agent-visible inputs live under `task/environment/data/session`; reference logic and generated hidden fixtures live only under `task/solution` and `task/tests`.
