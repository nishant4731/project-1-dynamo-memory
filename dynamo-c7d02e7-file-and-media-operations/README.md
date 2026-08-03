# Timecut Atlas Recovery

This repository contains a single Harbor task in `task/`. The task asks an agent to recover a flattened design-review atlas from visible sprite, palette, manifest, and placement-journal files, and to leave behind a reusable recovery script.

The challenge is bitemporal image reconstruction with a proof-lock overlay stage: each frame has both an artwork time and a publication cutoff, so late corrections, removals, and future-effective records must be applied only when they are authoritative for that frame. The solver also has to solve a modular subset-selection lock, decode custom sprite masks, transform them, and composite them with the stated integer alpha and blend rules.

Verification is deterministic. The pytest verifier recomputes the expected atlas pixels from the visible input files, decodes the submitted PNG, checks the media artifact and JSON audit report, then runs the submitted solver on hidden generated scenes that exercise the same disclosed contract.
